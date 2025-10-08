import React from "react";

export default function ArchiveBar({ archives, onSelectArchive, onNewChat }) {
  const uniqueArchives = Array.from(new Set(archives.map((a) => a.archive_id)));

  return (
    <div className="archive-bar">
      {/* Nút tạo đoạn chat mới - cố định ở trên */}
      <div className="archive-header">
        <button
          onClick={onNewChat}
          className="new-chat-btn"
        >
          + Đoạn chat mới
        </button>
      </div>

      {/* Danh sách các đoạn chat */}
      <div className="archive-list">
        <h2 className="archive-title">Đoạn chat</h2>
        {uniqueArchives.map((id) => (
        <div
          key={id}
          onClick={() => onSelectArchive(id)}
          className="archive-item"
        >
          Cuộc trò chuyện #{id}
        </div>
      ))}
      </div>
    </div>
  );
}
