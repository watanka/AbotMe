import React, { useState, useRef, useEffect } from "react";

export default function ChatbotWidget() {
  const [messages, setMessages] = useState([
    { role: "bot", content: "안녕하세요! 궁금한 점을 물어보세요." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", content: input };
    setMessages(msgs => [...msgs, userMsg]);
    setInput("");
    setLoading(true);
    // TODO: API 연동 (임시 답변)
    setTimeout(() => {
      setMessages(msgs => [
        ...msgs,
        { role: "bot", content: "(예시 답변) 이 부분은 곧 API와 연동됩니다." }
      ]);
      setLoading(false);
    }, 900);
  };

  const handleKeyDown = e => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="fixed bottom-6 right-6 w-80 max-w-[92vw] bg-white border border-gray-200 rounded-2xl shadow-2xl flex flex-col z-50">
      <div className="p-4 border-b bg-primary/10 rounded-t-2xl">
        <span className="font-bold text-lg text-primary">이력서 챗봇</span>
      </div>
      <div className="flex-1 overflow-y-auto px-4 py-2 h-72">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} mb-2`}
          >
            <div
              className={`px-3 py-2 rounded-xl max-w-[85%] text-sm break-words shadow-sm "
                ${msg.role === "user"
                  ? "bg-primary text-black"
                  : "bg-gray-100 text-gray-700"}
              `}
            >
              {msg.content}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form
        className="flex items-end gap-2 p-4 border-t bg-white rounded-b-2xl"
        onSubmit={e => {
          e.preventDefault();
          handleSend();
        }}
      >
        <textarea
          className="flex-1 resize-none rounded-lg border border-gray-200 p-2 text-sm focus:ring-2 focus:ring-primary/40 min-h-[36px] max-h-24"
          placeholder="질문을 입력하세요..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          rows={1}
        />
        <button
          type="submit"
          className="px-3 py-2 rounded-lg bg-primary text-black font-semibold shadow hover:bg-primary/90 transition disabled:opacity-60 disabled:cursor-not-allowed"
          disabled={loading || !input.trim()}
        >
          전송
        </button>
      </form>
    </div>
  );
}
