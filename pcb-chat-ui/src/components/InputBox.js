import { useState } from "react";

function InputBox({ sendMessage }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    sendMessage(text);
    setText("");
  };

  return (
    <div style={{
      display: "flex",
      padding: "10px",
      background: "#020617",
      borderTop: "1px solid #22c55e"
    }}>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Describe your PCB..."
        style={{
          flex: 1,
          padding: "10px",
          background: "#0f172a",
          color: "white",
          border: "1px solid #22c55e",
          borderRadius: "8px"
        }}
      />
      <button
        onClick={handleSend}
        className="glow"
        style={{
          marginLeft: "10px",
          padding: "10px 20px",
          background: "#22c55e",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer"
        }}
      >
        Send
      </button>
    </div>
  );
}

export default InputBox;