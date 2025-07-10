import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ResumeFlowContainer from './components/ResumeFlowContainer';
import ResumeQnA from './components/ResumeQnA';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ResumeFlowContainer />} />
        <Route path="/resume/qna" element={<ResumeQnA />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
