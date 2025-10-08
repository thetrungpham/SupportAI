// src/services/api.js
const API_BASE = "http://localhost:8000/api";

export const getArchives = async () => {
  const res = await fetch(`${API_BASE}/archives/`);
  if (!res.ok) throw new Error("Failed to fetch archives");
  return res.json();
};

export const getArchiveMessages = async (archiveId) => {
  const res = await fetch(`${API_BASE}/archives/${archiveId}`);
  if (!res.ok) throw new Error("Failed to fetch messages");
  return res.json();
};

export const sendChatMessage = async (archiveId, text) => {
  const res = await fetch(`${API_BASE}/chat/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ archive_id: archiveId, query: text }),
  });

  if (!res.ok) throw new Error("Failed to send message");
  return res.json();
};
