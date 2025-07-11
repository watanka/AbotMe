import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { resumeAPI } from '../api/service';

export default function ResumeQnA() {
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [answers, setAnswers] = useState({}); // { [questionId]: { value, original } }

    useEffect(() => {
        const fetchQuestions = async () => {
            setLoading(true);
            setError(null);
            try {
                const res = await resumeAPI.generateQuestions();
                if (!res.ok) throw new Error("질문을 받아오지 못했습니다.");
                const data = await res.json();
                setQuestions(data.questions || []);
                // 질문을 받은 후, 각 질문별 답변도 fetch
                if (data.questions && data.questions.length > 0) {
                    const entries = await Promise.all(
                        data.questions.map(async (q) => {
                            const [id] = Object.entries(q)[0];
                            try {
                                const res = await resumeAPI.getAnswer(id);
                                if (!res.ok) throw new Error();
                                const answer = await res.text();
                                return [id, { value: answer || "", original: answer || "" }];
                            } catch {
                                return [id, { value: "", original: "" }];
                            }
                        })
                    );
                    setAnswers(Object.fromEntries(entries));
                } else {
                    setAnswers({});
                }
            } catch (e) {
                setError(e.message || "서버 오류");
            } finally {
                setLoading(false);
            }
        };
        fetchQuestions();
    }, []);

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
            {loading && <div className="text-gray-400">질문을 생성 중입니다...</div>}
            {error && <div className="text-red-500">{error}</div>}
            {!loading && !error && (
                questions.length > 0 ? (
                    <ul className="w-full space-y-4">
                        {questions.map((q, idx) => {
                            const [id, text] = Object.entries(q)[0];
                            const answerObj = answers[id] || { value: "", original: "" };
                            const value = answerObj.value;
                            const original = answerObj.original;
                            const changed = value.trim() !== original.trim() && value.trim().length > 0;
                            return (
                                <li key={id} className="p-4 rounded-lg bg-gray-50 border border-gray-200 shadow flex flex-col gap-2">
                                    <span className="font-semibold text-gray-700">Q{idx + 1}.</span> {text}
                                    <textarea
                                        className="mt-2 w-full min-h-[60px] border rounded p-2 text-base focus:ring-2 focus:ring-primary/40"
                                        placeholder="답변을 입력하세요"
                                        value={value}
                                        onChange={e => setAnswers(a => ({ ...a, [id]: { ...a[id], value: e.target.value } }))}
                                    />
                                    <div className="flex items-center gap-2 mt-1">
                                        <button
                                            className={`px-4 py-1.5 rounded bg-primary text-black font-semibold shadow hover:bg-primary/90 transition disabled:opacity-60 disabled:cursor-not-allowed`}
                                            disabled={!changed}
                                            onClick={async () => {
                                                try {
                                                    const res = await resumeAPI.saveAnswer(id, value);
                                                    if (!res.ok) throw new Error("제출에 실패했습니다");
                                                    setAnswers(a => ({ ...a, [id]: { value, original: value } }));
                                                } catch (e) {
                                                    setError(e.message);
                                                }
                                            }}
                                        >
                                            제출
                                        </button>
                                        {value.trim().length > 0 && value.trim() === original.trim() && (
                                            <span className="text-green-600 ml-2">제출 완료!</span>
                                        )}
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
