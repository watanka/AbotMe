import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { qnaAPI } from '../api/service';

export default function ResumeQnA() {
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({}); // { [questionId]: value }
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchQuestions = async () => {
            setLoading(true);
            setError(null);
            try {
                const qs = await qnaAPI.getQuestions();
                setQuestions(qs || []);
                setAnswers({}); // 답변 초기화(필요하다면 답변 조회 API로 불러올 수 있음)
            } catch (e) {
                setError(e.message || "서버 오류");
            } finally {
                setLoading(false);
            }
        };
        fetchQuestions();
    }, []);

    const handleAnswerChange = (qid, value) => {
        setAnswers(a => ({ ...a, [qid]: value }));
    };

    const handleAnswerSubmit = async (qid) => {
        try {
            await qnaAPI.submitAnswer(qid, answers[qid] || "");
            // UX 개선: 제출 성공시 알림 등 추가 가능
        } catch (e) {
            setError(e.message || "답변 제출 실패");
        }
    };

    const navigate = useNavigate();
    return (
        <section className="w-full max-w-2xl mx-auto bg-white rounded-2xl shadow-2xl flex flex-col items-center p-6 border border-gray-200 mt-10">
            <div className="w-full flex justify-end mb-2">
                <button
                    className="px-4 py-2 rounded-lg bg-primary text-black font-semibold shadow hover:bg-primary/90 transition"
                    onClick={() => navigate("/")}
                >
                    이력서로 돌아가기
                </button>
            </div>
            <h2 className="text-xl font-semibold mb-4">이력서 Q&A</h2>
            {loading && <div className="text-gray-400">질문을 불러오는 중입니다...</div>}
            {error && <div className="text-red-500">{error}</div>}
            {!loading && !error && (
                questions.length > 0 ? (
                    <ul className="w-full space-y-4">
                        {questions.map((q, idx) => {
                            const qid = q.question_id;
                            const value = answers[qid] || "";
                            return (
                                <li key={qid} className="p-4 rounded-lg bg-gray-50 border border-gray-200 shadow flex flex-col gap-2">
                                    <span className="font-semibold text-gray-700">Q{idx + 1}.</span> {q.question}
                                    <textarea
                                        className="mt-2 w-full min-h-[60px] border rounded p-2 text-base focus:ring-2 focus:ring-primary/40"
                                        placeholder="답변을 입력하세요"
                                        value={value}
                                        onChange={e => handleAnswerChange(qid, e.target.value)}
                                    />
                                    <div className="flex items-center gap-2 mt-1">
                                        <button
                                            className="px-4 py-1.5 rounded bg-primary text-black font-semibold shadow hover:bg-primary/90 transition"
                                            disabled={value.trim().length === 0}
                                            onClick={() => handleAnswerSubmit(qid)}
                                        >
                                            제출
                                        </button>
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                ) : (
                    <div className="text-gray-500">생성된 질문이 없습니다.</div>
                )
            )}
        </section>
    );
}
