import React, { useState } from 'react';
import './ChatArea.css';

const FAQS = [
    { label: 'FAQ', question: '자주 묻는 질문을 알려줘' },
    { label: '경력', question: '주요 경력을 알려줘' },
    { label: '기타', question: '기타 궁금한 점이 있어' },
];

export default function ChatArea() {
    const [messages, setMessages] = useState([
        { from: 'bot', text: '무엇을 도와드릴까요?' },
    ]);
    const [input, setInput] = useState('');

    const handleSend = (msg) => {
        if (!msg.trim()) return;
        setMessages((prev) => [...prev, { from: 'user', text: msg }]);
        setTimeout(() => {
            setMessages((prev) => [...prev, { from: 'bot', text: '챗봇 더미 답변: ' + msg }]);
        }, 500);
        setInput('');
    };

    const handleFAQ = (q) => {
        setInput(q);
    };

    return (
        <div className="chat-area">
            <div className="faq-buttons">
                {FAQS.map((faq) => (
                    <button key={faq.label} onClick={() => handleFAQ(faq.question)}>{faq.label}</button>
                ))}
            </div>
            <div className="chat-messages">
                {messages.map((msg, i) => (
                    <div key={i} className={msg.from === 'user' ? 'msg-user' : 'msg-bot'}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className="chat-input-row">
                <input
                    type="text"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    placeholder="메시지를 입력하세요..."
                    onKeyDown={e => { if (e.key === 'Enter') handleSend(input); }}
                />
                <button className="send-btn" onClick={() => handleSend(input)}>전송</button>
            </div>
        </div>
    );
} 