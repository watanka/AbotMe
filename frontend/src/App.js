import './App.css';
import ChatArea from './ChatArea';
import ProfileSidebar from './ProfileSidebar';

function App() {
  return (
    <div className="main-layout">
      <ProfileSidebar />
      <ChatArea />
    </div>
  );
}

export default App;
