import React from "react";

export default function ChatBot({ messages, loading }) {
  return (
    <div className="chat-messages">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={msg.sender === "user" ? "message-user" : "message-bot"}
        >
          {msg.message}
        </div>
      ))}
      {loading && <div className="italic text-white">Bot đang trả lời...</div>}
    </div>
  );
}
