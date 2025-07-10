import { useEffect, useState } from 'react';
import ResumeUpload from './ResumeUpload';
import ResumeViewer from './ResumeViewer';

export default function ResumeFlowContainer() {
    // 컴포넌트 마운트 시 backend에서 이력서 정보 요청
    const [resumeInfo, setResumeInfo] = useState(null);
    const [_loading, setLoading] = useState(true);
    const [_error, setError] = useState(null);

    useEffect(() => {
        const fetchResumeInfo = async () => {
            setLoading(true);
            setError(null);
            try {
                const res = await fetch('http://localhost:8000/resume');
                if (res.status === 404) {
                    setResumeInfo(null);
                } else if (res.ok) {
                    const data = await res.json();

                    setResumeInfo(data);
                } else {
                    setError('이력서 정보를 불러오지 못했습니다.');
                }
            } catch (e) {
                setError('서버 연결 오류');
            } finally {
                setLoading(false);
            }
        };
        fetchResumeInfo();
    }, []);
    const [showUpload, setShowUpload] = useState(false);

    // 업로드 성공 시 localStorage에도 저장
    const handleUploadSuccess = (info) => {
        setResumeInfo(info);
        localStorage.setItem('resumeInfo', JSON.stringify(info));
    };

    if (resumeInfo && resumeInfo.pdf_url) {
        console.log("resumeinfo: {pdf_url: " + resumeInfo.pdf_url + "}")
        return (
            <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
                <ResumeViewer pdfUrl={resumeInfo.pdf_url} />
                <button
                    className="mt-6 px-4 py-2 rounded bg-primary text-black font-semibold shadow hover:bg-primary/90"
                    onClick={() => { setResumeInfo(null); setShowUpload(true); }}
                    aria-label="다른 이력서 업로드하기"
                >
                    다른 이력서 업로드하기
                </button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
            {!showUpload ? (
                <button
                    className="w-full max-w-xs px-8 py-4 rounded-3xl bg-primary-700 text-black font-extrabold text-2xl shadow-2xl hover:bg-primary-800 active:bg-primary-900 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-primary-300 transition"
                    onClick={() => setShowUpload(true)}
                    aria-label="이력서 업로드"
                >
                    이력서 업로드
                </button>
            ) : (
                <ResumeUpload onUploadSuccess={handleUploadSuccess} />
            )}
        </div>
    );
}
