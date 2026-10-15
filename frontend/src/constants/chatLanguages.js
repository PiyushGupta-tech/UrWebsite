/**
 * Chat assistant reply languages. Codes other than "auto" must match CHAT_LANGUAGES in
 * backend/website/chatbot.py; "auto" is never sent, so the AI follows the visitor's own language.
 */
export const DEFAULT_CHAT_LANGUAGE = "auto";

export const CHAT_LANGUAGES = [
  {
    code: "auto",
    label: "Auto",
    english: "Match my language",
    greeting:
      "Hi! I'm the Urbanrupee Assistant. Ask me anything about our products, payments, UPI, payouts, or getting started, in English, Hindi, or your own language.",
    placeholder: "Ask a question…",
    tryAsking: "You could ask",
    suggestions: [
      "What is Urbanrupee?",
      "How does payment orchestration improve success rates?",
      "Can I get a demo?",
    ],
  },
  {
    code: "en",
    label: "English",
    english: "Always English",
    greeting:
      "Hi! I'm the Urbanrupee Assistant. Ask me anything about our products, payments, UPI, payouts, or getting started.",
    placeholder: "Ask a question…",
    tryAsking: "You could ask",
    suggestions: [
      "What is Urbanrupee?",
      "How does payment orchestration improve success rates?",
      "Can I get a demo?",
    ],
  },
  {
    code: "hi",
    label: "हिन्दी",
    english: "Hindi",
    greeting:
      "नमस्ते! मैं Urbanrupee असिस्टेंट हूँ। हमारे प्रोडक्ट्स, पेमेंट्स, UPI, पेआउट्स या शुरुआत करने के बारे में कुछ भी पूछिए।",
    placeholder: "अपना सवाल लिखें…",
    tryAsking: "आप यह पूछ सकते हैं",
    suggestions: [
      "Urbanrupee क्या है?",
      "पेमेंट ऑर्केस्ट्रेशन से सक्सेस रेट कैसे बढ़ता है?",
      "क्या मुझे डेमो मिल सकता है?",
    ],
  },
  {
    code: "hinglish",
    label: "Hinglish",
    english: "Hindi in English letters",
    greeting:
      "Namaste! Main Urbanrupee Assistant hoon. Hamare products, payments, UPI, payouts ya shuruaat ke baare mein kuch bhi poochiye.",
    placeholder: "Apna sawaal likhiye…",
    tryAsking: "Aap yeh pooch sakte hain",
    suggestions: [
      "Urbanrupee kya hai?",
      "Payment orchestration se success rate kaise badhta hai?",
      "Kya mujhe demo mil sakta hai?",
    ],
  },
];

export function findChatLanguage(code) {
  return CHAT_LANGUAGES.find((lang) => lang.code === code) || CHAT_LANGUAGES[0];
}
