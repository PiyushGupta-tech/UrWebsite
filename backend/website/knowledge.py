"""Build and search a keyword index from site content (Phase 1 bot, no LLM)."""

import re
from dataclasses import dataclass

from . import catalogue, chat_faqs, content, page_content

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
        route = page_content.SLUG_TO_ROUTE.get(slug, f"/{slug}")
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


def answer_query(query: str) -> dict:
    """Return reply text and source links for a user message."""
    message = (query or "").strip()
    if not message:
        return {
            "reply": "Please type a question about Urbanrupee, our products, or services.",
            "sources": [],
        }

    if len(message) > 500:
        message = message[:500]

    hits = search(message, top_k=1)
    if not hits:
        return {
            "reply": (
                "I couldn't find a match for that on our site. Try asking about payment "
                "orchestration, Hyper Checkout, white label solutions, AML, reconciliation, "
                "or security—or contact our team for help."
            ),
            "sources": [
                {"title": "FAQ", "href": "/faq"},
                {"title": "Contact Us", "href": "/contact"},
            ],
        }

    _, best = hits[0]
    sources = [{"title": best.title, "href": best.href}]

    if best.question:
        parts = best.text.split("\n", 1)
        reply = parts[1].strip() if len(parts) > 1 else best.text
    else:
        reply = best.text[:800] + ("…" if len(best.text) > 800 else "")

    return {"reply": reply, "sources": sources}
