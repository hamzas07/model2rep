import React, { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState({ predicted_diseases: [], explanation: "" });
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", { message });

      console.log("API Response:", res.data); // Debugging

      // Ensure the response has the expected structure
      setResponse({
        predicted_diseases: res.data.predicted_diseases || [],
        explanation: res.data.explanation || "No explanation available.",
      });
    } catch (error) {
      console.error("API Error:", error);
      setResponse({
        predicted_diseases: [],
        explanation: "Error fetching response!",
      });
    }

    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Medical Chatbot</h1>
      <textarea
        rows="3"
        cols="50"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask about a disease..."
      />
      <br />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? "Loading..." : "Ask"}
      </button>

      {response.predicted_diseases.length > 0 ? (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <h3>Predicted Diseases:</h3>
          <ul>
            {response.predicted_diseases.map((disease, index) => (
              <li key={index}>{disease}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No disease predictions available.</p>
      )}

      {response.explanation && (
        <div>
          <h3>Explanation:</h3>
          <p>{response.explanation}</p>
        </div>
      )}
    </div>
  );
}

export default App;
