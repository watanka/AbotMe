import React from 'react';
import './App.css';
import ChatArea from './ChatArea';
import { chatAPI } from './api/service';

function App() {
  return (
    <div className="App">
      <ChatArea chatAPI={chatAPI} />
    </div>
  );
}

export default App;
