import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { qnaAPI } from '../api/service';
function PopupAlert({ show, onClose, message }) {
    return (
        <div
            className={`fixed top-8 left-1/2 z-50 transform -translate-x-1/2 transition-all duration-500 ${show ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
        >
            <div className="flex items-center gap-3 px-6 py-4 rounded-xl shadow-xl bg-gradient-to-r from-primary/90 to-indigo-200 border border-primary text-black font-semibold text-base animate-pop">
                <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                <span>{message}</span>
                <button
                    onClick={onClose}
                    className="ml-4 px-2 py-1 rounded bg-primary/20 hover:bg-primary/40 transition text-xs"
                >
                    닫기
                </button>
            </div>
        </div>
    );
}

export default function ResumeQnA(props) {
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({}); // { [questionId]: value }
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [popup, setPopup] = useState(false);
    const [submitting, setSubmitting] = useState({}); // { [questionId]: boolean }

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
        if (submitting[qid]) return; // prevent double submit
        setSubmitting(s => ({ ...s, [qid]: true }));
        try {
            await qnaAPI.submitAnswer(qid, answers[qid] || "");
            setPopup(true);
            setTimeout(() => setPopup(false), 3500);
        } catch (e) {
            setError(e.message || "답변 제출 실패");
        } finally {
            setSubmitting(s => ({ ...s, [qid]: false }));
        }
    };


    const navigate = useNavigate();
    return (
        <>
            <PopupAlert
                show={popup}
                onClose={() => setPopup(false)}
                message={"답변 내용이 제출되었습니다. 챗봇 반영까지는 시간이 조금 걸릴 수 있습니다."}
            />
            <section className="w-full max-w-2xl mx-auto bg-white rounded-2xl shadow-2xl flex flex-col items-center p-6 border border-gray-200 mt-10">
                <div className="w-full flex justify-end mb-2">
                    <button
                        className="px-4 py-2 rounded-lg bg-primary text-black font-semibold shadow hover:bg-primary/90 transition"
                        onClick={props.onGoResume ? props.onGoResume : () => navigate("/")}
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
                                                className="px-4 py-1.5 rounded bg-primary text-black font-semibold shadow hover:bg-primary/90 transition flex items-center justify-center min-w-[64px]"
                                                disabled={value.trim().length === 0 || submitting[qid]}
                                                onClick={() => handleAnswerSubmit(qid)}
                                            >
                                                {submitting[qid] ? (
                                                    <span className="flex items-center">
                                                        <svg className="animate-spin h-5 w-5 mr-1 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                            <circle className="opacity-20" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                                            <path className="opacity-80" fill="currentColor" d="M12 2a10 10 0 0 1 10 10h-4a6 6 0 0 0-6-6V2z" />
                                                        </svg>
                                                        제출 중...
                                                    </span>
                                                ) : (
                                                    "제출"
                                                )}
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
        </>
    );
}
