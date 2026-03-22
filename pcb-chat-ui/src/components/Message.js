function Message({ msg }) {
  return (
    <div
      className="message-animate"
      style={{
        textAlign: msg.sender === "user" ? "right" : "left",
        margin: "10px"
      }}
    >
      <div className={msg.sender === "user" ? "user" : "bot"}>

        {msg.loading ? (
          <>
            <p className="typing">
              ⚙️ Generating PCB<span>.</span><span>.</span><span>.</span>
            </p>
            <p>📡 Routing connections...</p>
            <p>🧠 Optimizing layout...</p>

            <div style={{
              height: "5px",
              background: "#22c55e",
              width: "100%",
              animation: "load 2s linear"
            }}></div>
          </>
        ) : (
          <p>{msg.text}</p>
        )}

        {msg.fileUrl && (
          <a href={msg.fileUrl} download style={{ color: "#60a5fa" }}>
            📥 Download PCB File
          </a>
        )}
      </div>
    </div>
  );
}

export default Message;