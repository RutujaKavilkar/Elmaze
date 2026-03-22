import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";

function App() {
  const [messages, setMessages] = useState([]);

  const sendMessage = (text) => {
    setMessages(prev => [...prev, { text, sender: "user" }]);

    setMessages(prev => [
      ...prev,
      { text: "Generating...", sender: "bot", loading: true }
    ]);

    setTimeout(() => {
      setMessages(prev => [
        ...prev.slice(0, -1),
        {
          text: "✅ PCB generated with optimized routing, component placement, and signal integrity checks.",
          sender: "bot",
          fileUrl: "#"
        }
      ]);
    }, 2000);
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>

      {/* HEADER */}
      <div style={{ position: "relative" }}>

        <button
          onClick={() => setMessages([])}
          style={{
            position: "absolute",
            left: "10px",
            top: "10px",
            background: "#22c55e",
            border: "none",
            padding: "8px",
            borderRadius: "6px",
            cursor: "pointer"
          }}
        >
          + New Chat
        </button>

        <h2 style={{
          textAlign: "center",
          color: "#22c55e",
          padding: "10px",
          borderBottom: "1px solid #22c55e",
          textShadow: "0 0 10px #22c55e"
        }}>
          ⚡ PCB AI Designer
          <div style={{ fontSize: "12px", color: "#94a3b8" }}>
            Generate PCB designs using AI ⚙️
          </div>
        </h2>

      </div>

      {/* CHAT */}
      <div style={{ flex: 1 }}>
        <ChatWindow messages={messages} />
      </div>

      {/* INPUT FIX */}
      <div style={{
        position: "sticky",
        bottom: 0,
        background: "#020617",
        zIndex: 10,
        padding: "5px"
      }}>
        <InputBox sendMessage={sendMessage} />
      </div>

    </div>
  );
}

export default App;