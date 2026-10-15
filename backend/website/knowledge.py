"""Build and search a keyword index from site content (Phase 1 bot, no LLM)."""

import difflib
import re
from dataclasses import dataclass

from . import catalogue, chat_faqs, content, page_content, page_faqs

STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "shall",
        "can",
        "need",
        "to",
        "of",
        "in",
        "for",
        "on",
        "with",
        "at",
        "by",
        "from",
        "as",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "between",
        "under",
        "again",
        "further",
        "then",
        "once",
        "here",
        "there",
        "when",
        "where",
        "why",
        "how",
        "all",
        "each",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "no",
        "nor",
        "not",
        "only",
        "own",
        "same",
        "so",
        "than",
        "too",
        "very",
        "just",
        "and",
        "but",
        "if",
        "or",
        "because",
        "until",
        "while",
        "about",
        "what",
        "which",
        "who",
        "whom",
        "this",
        "that",
        "these",
        "those",
        "am",
        "it",
        "its",
        "my",
        "your",
        "our",
        "their",
        "me",
        "you",
        "we",
        "they",
        "i",
    }
)

MIN_MATCH_SCORE = 3.0


@dataclass(frozen=True)
class Chunk:
    text: str
    title: str
    href: str
    question: str = ""

    @property
    def tokens(self) -> set[str]:
        return set(_tokenize(self.text))


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def _join_parts(*parts: str) -> str:
    return "\n".join(p.strip() for p in parts if p and str(p).strip())


def _as_text(value) -> str:
    """Normalize page fields that may be a string or list of paragraphs."""
    if isinstance(value, list):
        return "\n".join(str(p).strip() for p in value if p and str(p).strip())
    return str(value).strip() if value else ""


# Content pages without their own SPA route link to the closest live page instead.
UNROUTED_SLUG_ROUTES = {
    "aml-detector": "/services/risk-fraud-management",
    "automatic-reconciliation": "/services/reconciliation",
    "payout-portal": "/services/payouts",
}


def page_route(slug: str) -> str:
    return page_content.SLUG_TO_ROUTE.get(slug) or UNROUTED_SLUG_ROUTES.get(slug, "/")


def valid_routes() -> frozenset[str]:
    return frozenset(page_content.ROUTE_SLUGS) | {"/"}


def _iter_chunks():
    for item in chat_faqs.CHAT_FAQS:
        q = item["question"]
        a = item["answer"]
        yield Chunk(
            question=q,
            text=_join_parts(q, a),
            title=q,
            href=item.get("href", "/faq"),
        )

    for item in content.FAQS.get("items", []):
        q = item["question"]
        a = item["answer"]
        yield Chunk(
            question=q,
            text=_join_parts(q, a),
            title=q,
            href="/faq",
        )

    for slug, page in page_content.PAGES.items():
        route = page_route(slug)
        title = page.get("title", slug.replace("-", " ").title())
        intro = _as_text(page.get("intro", ""))
        if intro:
            yield Chunk(
                text=_join_parts(title, intro),
                title=title,
                href=route,
            )
        for block in page.get("blocks", []):
            heading = block.get("heading", "")
            body = block.get("body", "")
            bullets = " ".join(block.get("bullets", []))
            yield Chunk(
                text=_join_parts(heading, body, bullets),
                title=heading or title,
                href=route,
            )

    suite = catalogue.PRODUCT_SUITE
    for item in suite.get("items", []):
        title = item.get("title", "")
        body = item.get("body", "")
        highlights = " ".join(item.get("highlights", []))
        yield Chunk(
            text=_join_parts(title, body, highlights),
            title=title,
            href=item.get("href", "/"),
        )

    ps = content.PAYMENT_SOLUTION
    yield Chunk(
        text=_join_parts(
            ps.get("title", ""),
            ps.get("feature_body", ""),
            " ".join(ps.get("bullets", [])),
        ),
        title=ps.get("title", "Payment Solutions"),
        href="/services/collections",
    )

    for feat in content.FEATURES.get("items", []):
        yield Chunk(
            text=_join_parts(feat.get("title", ""), feat.get("body", "")),
            title=feat.get("title", "Features"),
            href="/",
        )


def build_index() -> list[Chunk]:
    return list(_iter_chunks())


def faq_anchor(question: str) -> str:
    """Element id of a question in the FAQ accordions; mirrors faqAnchor() in the frontend."""
    return "faq-" + re.sub(r"[^a-z0-9]+", "-", question.lower()).strip("-")[:80]


def _faq_routes() -> dict[str, list[str]]:
    """Anchor -> routes whose page shows that question in an FAQ accordion (see PageView.vue)."""
    shown: list[tuple[str, list[dict]]] = [
        ("/faq", page_content.PAGES.get("faq", {}).get("items", [])),
        ("/", content.HOME_CLOSING.get("faq_items", [])),
    ]
    for slug, route in page_content.SLUG_TO_ROUTE.items():
        if slug != "faq" and slug in page_content.PAGES:
            shown.append((route, page_faqs.closing_for_slug(slug).get("faq_items", [])))

    routes: dict[str, list[str]] = {}
    for route, items in shown:
        for item in items:
            question = item.get("question", "")
            if not question:
                continue
            pages = routes.setdefault(faq_anchor(question), [])
            if route not in pages:
                pages.append(route)
    return routes


FAQ_ROUTES: dict[str, list[str]] = _faq_routes()


def source_link(title: str, href: str) -> str:
    """Link a source to the exact FAQ question when a page shows it, else to the page itself."""
    anchor = faq_anchor(title)
    pages = FAQ_ROUTES.get(anchor)
    if not pages:
        return href
    if href in pages:
        route = href
    elif "/faq" in pages:
        route = "/faq"
    else:
        route = pages[0]
    return f"{route}#{anchor}"


def route_of(href: str) -> str:
    return href.split("#", 1)[0]


INDEX: list[Chunk] = build_index()


def _score(query_tokens: list[str], chunk: Chunk) -> float:
    if not query_tokens:
        return 0.0

    question_tokens = set(_tokenize(chunk.question)) if chunk.question else set()
    chunk_tokens = chunk.tokens

    score = 0.0
    for token in query_tokens:
        if token in question_tokens:
            score += 3.0
        elif token in chunk_tokens:
            score += 1.0

    q_lower = " ".join(query_tokens)
    text_lower = chunk.text.lower()
    if len(q_lower) >= 8 and q_lower in text_lower:
        score += 5.0
    if chunk.question and chunk.question.lower() in " ".join(query_tokens):
        score += 4.0

    return score


def search(query: str, top_k: int = 3) -> list[tuple[float, Chunk]]:
    query_tokens = _tokenize(query.strip())
    if not query_tokens:
        return []

    scored: list[tuple[float, Chunk]] = []
    for chunk in INDEX:
        s = _score(query_tokens, chunk)
        if s >= MIN_MATCH_SCORE:
            scored.append((s, chunk))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored[:top_k]


DEFAULT_SUGGESTIONS = (
    "What services does Urbanrupee offer?",
    "What is Payment Orchestration?",
    "How do I contact support?",
)
SUGGESTION_COUNT = 3


def _question_chunks() -> list[Chunk]:
    seen: set[str] = set()
    chunks = []
    for chunk in INDEX:
        key = chunk.question.casefold()
        if chunk.question and key not in seen:
            seen.add(key)
            chunks.append(chunk)
    return chunks


QUESTION_CHUNKS: list[Chunk] = _question_chunks()
QUESTION_VOCABULARY: list[str] = sorted({t for c in QUESTION_CHUNKS for t in _tokenize(c.text)})
QUESTION_VOCABULARY_SET = frozenset(QUESTION_VOCABULARY)
# Fuzzy matching is the slow part, so only the start of a long message is spell-matched.
MAX_FUZZY_TOKENS = 12


def suggest_questions(query: str, count: int = SUGGESTION_COUNT) -> list[str]:
    """FAQ questions closest to an unmatched message, topped up with popular questions.

    Misspelled words are matched to the nearest FAQ word, so "pyment gatway" still finds
    payment gateway questions.
    """
    tokens = _tokenize(query or "")[:MAX_FUZZY_TOKENS]
    for token in list(tokens):
        if token not in QUESTION_VOCABULARY_SET:
            tokens.extend(difflib.get_close_matches(token, QUESTION_VOCABULARY, n=2, cutoff=0.8))

    scored = [(_score(tokens, chunk), chunk.question) for chunk in QUESTION_CHUNKS]
    ranked = [question for score, question in sorted(scored, key=lambda pair: -pair[0]) if score > 0]

    suggestions: list[str] = []
    for question in [*ranked, *DEFAULT_SUGGESTIONS]:
        if question not in suggestions:
            suggestions.append(question)
        if len(suggestions) == count:
            break
    return suggestions


def answer_query(query: str) -> dict:
    """Return reply text, source links, and (when nothing matched) questions to try instead."""
    message = (query or "").strip()
    if not message:
        return {
            "reply": "Please type a question about Urbanrupee, our products, or services.",
            "sources": [],
            "suggestions": list(DEFAULT_SUGGESTIONS),
        }

    if len(message) > 500:
        message = message[:500]

    hits = search(message, top_k=1)
    if not hits:
        return {
            "reply": (
                "I'm not sure I understood that. Try one of these questions, or contact our "
                "team for help."
            ),
            "sources": [{"title": "Contact Us", "href": "/contact"}],
            "suggestions": suggest_questions(message),
        }

    _, best = hits[0]
    sources = [{"title": best.title, "href": source_link(best.title, best.href)}]

    if best.question:
        parts = best.text.split("\n", 1)
        reply = parts[1].strip() if len(parts) > 1 else best.text
    else:
        reply = best.text[:800] + ("…" if len(best.text) > 800 else "")

    return {"reply": reply, "sources": sources, "suggestions": []}
