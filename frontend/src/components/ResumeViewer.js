import React, { useCallback, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import ChatBot from "./ChatBot";
pdfjs.GlobalWorkerOptions.workerSrc = `${process.env.PUBLIC_URL}/pdf.worker.min.js`;


const PAGE_MAX_WIDTH = 600;
const PAGE_MIN_WIDTH = 280;

// PDF 문서 렌더링 컴포넌트
function PdfDocument({ file, pageNumber, pageWidth, maxWidth, minWidth, onLoadSuccess, onLoadError, loading, error }) {
    return (
        <Document
            file={file}
            onLoadSuccess={onLoadSuccess}
            onLoadError={onLoadError}
            loading={loading}
            error={error}
        >
            <div className="flex justify-center items-center border border-gray-200 rounded-2xl shadow-2xl bg-white overflow-hidden transition-all p-2 sm:p-4"
                style={{ maxWidth, minWidth }}>
                <Page
                    pageNumber={pageNumber}
                    width={pageWidth}
                    renderAnnotationLayer={false}
                    renderTextLayer={false}
                />
            </div>
        </Document>
    );
}

// 페이지 네비게이션 컴포넌트
function PageNavigation({ pageNumber, numPages, onPrev, onNext, prevLabel = "이전", nextLabel = "다음", className = "" }) {
    return (
        <div className={`flex flex-row gap-2 items-center justify-center mb-2 ${className}`}>
            <button
                className="flex items-center justify-center rounded-md border border-gray-300 bg-white px-3 py-1.5 text-base font-medium text-gray-700 shadow hover:bg-gray-100 active:bg-gray-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 transition-colors duration-150 disabled:opacity-40 disabled:cursor-not-allowed"
                onClick={onPrev} disabled={pageNumber <= 1} aria-label={prevLabel}
            >
                {prevLabel}
            </button>
            <span className="inline-flex items-center rounded-full bg-gray-100 text-gray-800 border border-gray-300 px-4 py-1 text-base font-semibold shadow select-none">
                {pageNumber} / {numPages || "-"}
            </span>
            <button
                className="flex items-center justify-center rounded-md border border-gray-300 bg-white px-3 py-1.5 text-base font-medium text-gray-700 shadow hover:bg-gray-100 active:bg-gray-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 transition-colors duration-150 disabled:opacity-40 disabled:cursor-not-allowed"
                onClick={onNext} disabled={pageNumber >= numPages} aria-label={nextLabel}
            >
                {nextLabel}
            </button>
        </div>
    );
}

// 에러 배너 컴포넌트
function ErrorBanner({ message }) {
    if (!message) return null;
    return (
        <div className="fixed bottom-16 left-1/2 -translate-x-1/2 bg-red-500 text-white text-base rounded-lg px-4 py-2 shadow-lg z-50 animate-fade-in">
            {message}
        </div>
    );
}

// ResumeViewer 컨테이너
export default function ResumeViewer({ pdfUrl }) {
    // Ensure PDF URL is properly prefixed with PUBLIC_URL
    const resolvedPdfUrl = `${process.env.PUBLIC_URL}/${pdfUrl}`;
    // 상수 및 상태
    const maxWidth = PAGE_MAX_WIDTH;
    const minWidth = PAGE_MIN_WIDTH;
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);
    const [error, setError] = useState(null);

    // PDF 로드 성공/실패 핸들러
    const onDocumentLoadSuccess = useCallback(({ numPages }) => {
        setNumPages(numPages);
        setPageNumber(1);
        setError(null);
    }, []);
    const onDocumentLoadError = useCallback((err) => {
        setError(err?.message || "PDF 로드 실패");
    }, []);

    // 페이지 이동
    const goToPrevPage = () => setPageNumber((prev) => Math.max(prev - 1, 1));
    const goToNextPage = () => setPageNumber((prev) => Math.min(prev + 1, numPages));

    // 반응형 페이지 너비
    const pageWidth = Math.min(window.innerWidth - 48, maxWidth);

    return (
        <>
            <section className="w-full max-w-3xl mx-auto bg-white rounded-2xl shadow-2xl flex flex-col items-center p-6 border border-gray-200 mt-10">
                {/* Q&A로 이동 버튼 - 우측 상단 고정 */}
                {/* <button
                    className="absolute top-4 right-4 px-4 py-2 rounded-lg bg-primary text-black font-semibold shadow hover:bg-primary/90 transition"
                    onClick={() => navigate("/resume/qna")}
                    aria-label="Q&A로 이동"
                >
                    Q&A로 이동
                </button> */}
                <h2 className="text-xl font-semibold tracking-tight text-slate-700 mb-2 mt-4 sm:mt-0">이력서 미리보기</h2>
                <div className="relative flex flex-col items-center w-full">
                    <div className="flex-1 flex justify-center items-center w-full min-h-[420px]">
                        <PdfDocument
                            file={resolvedPdfUrl}
                            pageNumber={pageNumber}
                            pageWidth={pageWidth}
                            maxWidth={maxWidth}
                            minWidth={minWidth}
                            onLoadSuccess={onDocumentLoadSuccess}
                            onLoadError={onDocumentLoadError}
                            loading={<div className="text-gray-400 text-lg font-medium p-8 animate-pulse flex items-center justify-center">PDF 불러오는 중...</div>}
                            error={<div className="inline-flex items-center rounded-full bg-gray-100 text-gray-800 border border-gray-300 px-3 py-1 text-xs font-semibold shadow-sm select-none">PDF를 불러올 수 없습니다.</div>}
                        />
                    </div>
                    {/* Controls: sticky bottom for mobile UX */}
                    <div className="sticky bottom-0 left-0 w-full flex flex-col items-center z-10 bg-gradient-to-t from-white via-white/80 to-transparent pt-3 pb-2 mt-2">
                        <PageNavigation
                            pageNumber={pageNumber}
                            numPages={numPages}
                            onPrev={goToPrevPage}
                            onNext={goToNextPage}
                            prevLabel="이전"
                            nextLabel="다음"
                        />
                    </div>
                    <ErrorBanner message={error} />
                </div>
            </section>
            {/* 챗봇 위젯: 오른쪽 하단 고정 */}
            <ChatBot />
        </>
    );
}
