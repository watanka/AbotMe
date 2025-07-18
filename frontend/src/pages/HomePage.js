import React, { useState } from "react";
import AdminLoginModal from "../components/AdminLoginModal";
import ChatBot from "../components/ChatBot";
import ResumeExistenceGate from "../components/ResumeExistenceGate";
import ResumeQnA from "../components/ResumeQnA";
import ResumeUpload from "../components/ResumeUpload";
import ResumeViewer from "../components/ResumeViewer";

export default function HomePage() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [showAdminModal, setShowAdminModal] = useState(false);
  const [adminPage, setAdminPage] = useState('home'); // 'home' | 'upload' | 'qna'
  const [highlights, setHighlights] = useState([]);
  const handleAdminLogin = (token) => {
    if (token && token.length > 0) setIsAdmin(true);
    setShowAdminModal(false);
    localStorage.setItem('adminToken', token);
  };

  // 메인 페이지(일반 사용자)
  if (!isAdmin) {
    return (
      <main className="min-h-screen bg-slate-50 flex flex-col items-center justify-center relative">
        <header className="absolute top-4 right-8">
          <button
            className="px-3 py-1 rounded bg-gray-200 text-black text-sm font-semibold border border-gray-400 shadow"
            onClick={() => setShowAdminModal(true)}
          >
            관리자 페이지
          </button>
        </header>
        <ResumeExistenceGate fallback={
          <div className="text-gray-500 text-lg mt-20">업로드된 이력서가 없습니다</div>
        }>
          {pdfUrl => (
            <>
              <ResumeViewer pdfUrl={pdfUrl} highlights={highlights} />
              <ChatBot onMetadata={setHighlights} />
            </>
          )}
        </ResumeExistenceGate>
        {showAdminModal && (
          <AdminLoginModal
            onSubmit={handleAdminLogin}
            onClose={() => setShowAdminModal(false)}
          />
        )}
      </main>
    );
  }

  // 관리자 모드 페이지
  return (
    <main className="min-h-screen bg-slate-50 flex flex-col items-center justify-center relative">
      <header className="absolute top-4 right-8 flex gap-2">
        <button
          className="px-3 py-1 rounded bg-gray-200 text-black text-sm font-semibold border border-gray-400 shadow"
          onClick={() => setAdminPage('upload')}
        >이력서 업로드</button>
        <button
          className="px-3 py-1 rounded bg-gray-200 text-black text-sm font-semibold border border-gray-400 shadow"
          onClick={() => setAdminPage('qna')}
        >QnA 관리</button>
        <button
          className="px-3 py-1 rounded bg-gray-200 text-black text-sm font-semibold border border-gray-400 shadow"
          onClick={() => { setIsAdmin(false); setAdminPage('home'); }}
        >일반모드로</button>
      </header>
      {adminPage === 'upload' && (
        <div className="w-full flex flex-col items-center mt-16">
          <h3 className="font-bold mb-4">이력서 업로드</h3>
          <ResumeUpload />
        </div>
      )}
      {adminPage === 'qna' && (
        <div className="w-full flex flex-col items-center mt-16">
          <h3 className="font-bold mb-4">QnA 관리</h3>
          <ResumeQnA onGoResume={() => setAdminPage('home')} />
        </div>
      )}
      {adminPage === 'home' && (
        <div className="w-full flex flex-col items-center mt-16">
          <ResumeExistenceGate fallback={<div className="text-gray-500 text-lg">이력서를 업로드하세요</div>}>
            {pdfUrl => <ResumeViewer pdfUrl={pdfUrl} />}
          </ResumeExistenceGate>
        </div>
      )}
    </main>
  );
}

