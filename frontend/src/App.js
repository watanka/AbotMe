import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';

function App() {
  return (
    <BrowserRouter basename="/AbotMe">
      <Routes>
        <Route path="" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
