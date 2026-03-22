import Message from "./Message";

function ChatWindow({ messages }) {
  return (
    <div style={{ height: "80vh", overflowY: "auto", padding: "10px" }}>

      {messages.length === 0 && (
        <div style={{
          textAlign: "center",
          marginTop: "100px",
          color: "#22c55e"
        }}>
          <h2>⚡ Welcome to PCB AI Designer</h2>
          <p>Describe your PCB requirements to generate designs instantly</p>
        </div>
      )}

      {messages.map((msg, i) => (
        <Message key={i} msg={msg} />
      ))}
    </div>
  );
}

export default ChatWindow;