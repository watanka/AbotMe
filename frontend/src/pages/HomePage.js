import React from "react";

// 단계별로 각 영역을 조건부 렌더링(업로드, 질문/답변, 이력서+챗봇)
export default function HomePage() {
  // TODO: 단계/상태 관리 및 각 영역 연결
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
    </main>
  );
}
