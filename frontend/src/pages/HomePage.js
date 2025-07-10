import React from "react";
import ResumeViewer from "../components/ResumeViewer";

export default function HomePage() {
  // 테스트: ResumeViewer만 렌더링
  return (
    <main className="min-h-screen bg-slate-50 flex flex-col items-center justify-center">
      {/* 이력서 업로드 영역 */}
      {/* <ResumeUpload /> */}
      {/* 질문 생성/답변 영역 */}
      {/* <QuestionsForm /> */}
      {/* 이력서+챗봇 뷰 영역 */}
      {/* <ResumeViewer /> */}
      {/* <ChatBot /> */}
      <div className="text-gray-500">AbotMe UI 구조 세팅 중...</div>
      <ResumeViewer />
    </main>
  );
}
