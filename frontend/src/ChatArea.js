import React, { useEffect, useState } from 'react';
import './ChatArea.css';

const FAQS = [
    { label: 'FAQ', question: '자주 묻는 질문을 알려줘' },
    { label: '경력', question: '주요 경력을 알려줘' },
    { label: '기타', question: '기타 궁금한 점이 있어' },
];

export default function ChatArea({ chatAPI }) {
    const [messages, setMessages] = useState([
        { from: 'bot', text: '무엇을 도와드릴까요?' },
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSend = async (msg) => {
        if (!msg.trim()) return;

        setIsLoading(true);
        const userMessage = { from: 'user', text: msg };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');

        // 스트리밍 응답 처리
        let botMsg = { from: 'bot', text: '' };
        setMessages((prev) => [...prev, botMsg]);
        try {
            await chatAPI.sendMessageStream(
                msg,
                (chunk) => {
                    botMsg.text += chunk;
                    setMessages((prev) => {
                        const updated = [...prev];
                        updated[updated.length - 1] = { ...botMsg };
                        return updated;
                    });
                }
            );
        } catch (error) {
            setMessages((prev) => [
                ...prev.slice(0, -1),
                { from: 'bot', text: '죄송합니다. 서버와의 통신에 문제가 발생했습니다.' }
            ]);
        } finally {
            setIsLoading(false);
        }
    };


    const handleFAQ = async (question) => {
        if (!chatAPI) return;
        try {
            setIsLoading(true);
            const response = await chatAPI.getFAQ();
            const faq = response.faqs.find(f => f.question === question);
            if (faq) {
                setMessages(prev => [...prev, { from: 'bot', text: faq.answer }]);
            }
        } catch (error) {
            console.error('Error loading FAQ:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Load chat history on component mount
    useEffect(() => {
        if (!chatAPI) return;

        const loadHistory = async () => {
            try {
                const history = await chatAPI.getHistory();
                setMessages(history.messages || []);
            } catch (error) {
                console.error('Error loading history:', error);
            }
        };

        loadHistory();
    }, [chatAPI]);

    return (
        <div className="chat-area">
            <div className="faq-buttons">
                {FAQS.map((faq) => (
                    <button key={faq.label} onClick={() => handleFAQ(faq.question)}>{faq.label}</button>
                ))}
            </div>
            <div className="chat-messages">
                {isLoading && <div className="loading-spinner"></div>}
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
                    disabled={isLoading}
                />
                <button onClick={() => handleSend(input)}>전송</button>
            </div>
        </div>
    );
} 