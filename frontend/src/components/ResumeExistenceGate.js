import { useEffect, useState } from "react";

/**
 * ResumeExistenceGate (render prop 패턴)
 * - 이력서(PDF) 존재 여부를 비동기 fetch(HEAD)로 확인하고,
 *   존재하면 children(pdfUrl)로 전달, 미존재/로딩/에러시 fallback 또는 안내 UI 렌더링
 *
 * @param {(pdfUrl: string) => React.ReactNode} children - PDF가 존재할 때 렌더링할 함수(children)
 * @param {ReactNode} fallback - PDF가 없을 때 보여줄 컴포넌트/문구
 */
export default function ResumeExistenceGate({ children, fallback }) {
    const [status, setStatus] = useState("loading"); // 'loading' | 'exists' | 'notfound' | 'error'
    const [pdfUrl, setPdfUrl] = useState(null);

    useEffect(() => {
        const url = "http://localhost:8000/resume"; // 실제 PDF API 엔드포인트로 교체
        fetch(url)
            .then(async res => {
                if (res.status === 404) setStatus("notfound");
                else if (res.ok) {
                    const data = await res.json();
                    setStatus("exists");
                    setPdfUrl(data.pdf_url);
                } else setStatus("error");
            })
            .catch(() => setStatus("error"));
    }, []);

    if (status === "loading") return <div className="text-gray-400 mt-16">이력서 확인 중...</div>;
    if (status === "error") return <div className="text-red-500 mt-16">이력서 정보를 불러올 수 없습니다.</div>;
    if (status === "notfound") return fallback;
    // exists
    return children(pdfUrl);
}
