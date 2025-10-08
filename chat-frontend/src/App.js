import React, { useEffect, useState } from "react";
import ArchiveBar from "./components/ArchiveBar";
import ChatBot from "./components/ChatBot";
import MessageInput from "./components/MessageInput";
import "./index.css";
import { getArchives, getArchiveMessages, sendChatMessage } from "./service/api.js";

function App() {
  const [archives, setArchives] = useState([]);
  const [currentArchiveId, setCurrentArchiveId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // Lấy toàn bộ lịch sử
  useEffect(() => {
    getArchives()
      .then(setArchives)
      .catch((err) => console.error("Error fetching archives:", err));
  }, []);

  // Khi chọn 1 archive
  const loadMessages = (archiveId) => {
    getArchiveMessages(archiveId)
      .then((data) => {
        setMessages(data);
        setCurrentArchiveId(archiveId);
      })
      .catch((err) => console.error("Error fetching messages:", err));
  };

  const createNewChat = () => {
    setCurrentArchiveId(null);
    setMessages([]);
  }

  // Gửi tin nhắn
  const sendMessage = async (text) => {
    if (!text || text.trim() === "") return;
    const tempID = Date.now();

    setMessages((prev) => [...prev, { id: tempID, sender: "user", message: text }]);
    setLoading(true);

    try {
      const data = await sendChatMessage(currentArchiveId, text);

      if (!currentArchiveId) setCurrentArchiveId(data.archive_id);

      setMessages((prev) => [...prev, { message: data.answer }]);
    } catch (err) {
      console.error("Error sending message:", err);
    }

    setLoading(false);
  };

  return (
    <div className="app-container">
      {/* Sidebar lịch sử hội thoại */}
      <ArchiveBar archives={archives} onSelectArchive={loadMessages} onNewChat={createNewChat} />

      {/* Khu vực chat chính */}
      <div className="chat-main">
        {/* Thanh header */}
        <div className = "chat-header">
          <h1 className="chat-title">SupportAI</h1>
        </div>
        <div className="chat-messages">
          <ChatBot messages={messages} loading={loading} />
        </div>
          <MessageInput onSend={sendMessage} />
      </div>
    </div>
  );
}

export default App;
