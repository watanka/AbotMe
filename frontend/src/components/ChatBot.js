import React, { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

export default function ChatBot({ onMetadata }) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "bot", content: "안녕하세요! 궁금한 점을 물어보세요." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  // 패널 사이즈 상태
  const [panelWidth, setPanelWidth] = useState(420);
  const [panelHeight, setPanelHeight] = useState(600);
  const resizingRef = useRef(false);
  const startPosRef = useRef({ x: 0, y: 0, w: 0, h: 0 });

  // 리사이즈 시작
  const startResize = (e) => {
    e.preventDefault();
    resizingRef.current = true;
    startPosRef.current = {
      x: e.clientX,
      y: e.clientY,
      w: panelWidth,
      h: panelHeight,
    };
    document.body.style.userSelect = 'none';
    window.addEventListener('mousemove', onResize);
    window.addEventListener('mouseup', stopResize);
  };

  // 리사이즈 진행
  const onResize = (e) => {
    if (!resizingRef.current) return;
    const dx = e.clientX - startPosRef.current.x;
    const dy = e.clientY - startPosRef.current.y;
    setPanelWidth(Math.max(320, Math.min(700, startPosRef.current.w + dx)));
    setPanelHeight(Math.max(400, Math.min(1000, startPosRef.current.h + dy)));
  };

  // 리사이즈 종료
  const stopResize = () => {
    resizingRef.current = false;
    document.body.style.userSelect = '';
    window.removeEventListener('mousemove', onResize);
    window.removeEventListener('mouseup', stopResize);
  };


  useEffect(() => {
    if (open) messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", content: input };
    setMessages(msgs => [...msgs, userMsg]);
    setInput("");
    setLoading(true);

    // 스트리밍 메시지 추가
    let botMsg = { role: "bot", content: "" };
    setMessages(msgs => [...msgs, botMsg]);

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/chat/graph/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });
      if (!res.ok || !res.body) throw new Error("답변을 받아오지 못했습니다.");

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;

      let metadata = null;
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const line = decoder.decode(value).trim();
          if (!line) continue;
          let parsed;
          try {
            parsed = JSON.parse(line);
          } catch (e) {
            continue;
          }
          if (parsed.type === "chunk") {
            botMsg.content += parsed.data;
            setMessages(prev => {
              const updated = [...prev];
              updated[updated.length - 1] = { ...botMsg };
              return updated;
            });
          } else if (parsed.type === "metadata" && metadata === null) {
            metadata = parsed.data;
            if (onMetadata) onMetadata(metadata);
          } else if (parsed.type === "error") {
            setMessages(prev => [
              ...prev.slice(0, -1),
              { role: "bot", content: parsed.data || "서버 오류" }
            ]);
          }
        }
      }
    } catch (e) {
      setMessages(prev => [
        ...prev.slice(0, -1),
        { role: "bot", content: e.message || "서버 오류" }
      ]);
    } finally {

      setLoading(false);
    }
  };



  const handleKeyDown = e => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {/* 최소화/확장 버튼 */}
      {!open && (
        <button
          className="bg-primary text-black rounded-full px-6 py-3 shadow-lg font-semibold hover:bg-primary/90 transition"
          onClick={() => setOpen(true)}
        >
          챗봇 열기
        </button>
      )}
      {/* 챗봇 패널 */}
      {open && (
        <div
          className="bg-white border border-gray-200 rounded-2xl shadow-2xl flex flex-col animate-fade-in"
          style={{
            width: panelWidth,
            height: panelHeight,
            minWidth: 320,
            minHeight: 400,
            maxWidth: 700,
            maxHeight: 1000,
            position: 'relative',
            overflow: 'hidden',
            zIndex: 50
          }}
        >
          <div className="p-4 border-b bg-primary/10 rounded-t-2xl flex items-center justify-between">
            <span className="font-bold text-lg text-primary">이력서 챗봇</span>
            <button
              className="ml-2 text-gray-500 hover:text-gray-700 text-xl font-bold px-2"
              onClick={() => setOpen(false)}
              aria-label="챗봇 닫기"
            >
              ×
            </button>
          </div>
          <div className="flex-1 overflow-y-auto px-4 py-2" style={{ height: `calc(${panelHeight - 140}px)` }}>
            {messages.map((msg, i) => {
              const isLast = i === messages.length - 1;
              const isBot = msg.role === "bot";
              const showLoadingDots = isLast && isBot && loading && !msg.content;
              return (
                <div
                  key={i}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} mb-2`}
                >
                  <div
                    className={`px-3 py-2 rounded-xl max-w-[85%] text-sm break-words shadow-sm
                      ${msg.role === "user"
                        ? "bg-primary text-black"
                        : "bg-gray-100 text-gray-700"}
                    `}
                  >
                    {(showLoadingDots || (isLast && isBot && loading && !msg.content)) ? (
                      <span className="flex gap-1 items-center h-5">
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                      </span>
                    ) : (
                      msg.role === "bot"
                        ? <div className="prose prose-sm max-w-none whitespace-pre-wrap"><ReactMarkdown>{msg.content}</ReactMarkdown></div>
                        : msg.content
                    )}
                  </div>
                </div>
              );
            })}
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
          {/* 사이즈 조절 핸들 */}
          <div
            onMouseDown={e => { e.stopPropagation(); startResize(e); }}
            className="absolute right-1 bottom-1 w-5 h-5 cursor-nwse-resize z-20 bg-transparent"
            style={{ userSelect: 'none', pointerEvents: 'auto' }}
          >
            <svg width="20" height="20"><polyline points="4,20 20,20 20,4" fill="none" stroke="#bbb" strokeWidth="2" /></svg>
          </div>
        </div>
      )}
    </div>
  );
}
