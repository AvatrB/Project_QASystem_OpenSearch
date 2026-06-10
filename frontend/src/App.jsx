import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, Activity, ShieldAlert } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'nexus', text: 'Sistem Kognisi NEXUS Medis Aktif. Ada yang bisa saya bantu terkait data pangkalan data Rumah Sakit, Sir?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Protokol otomatis gulir ke bawah saat pesan baru masuk
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: userMessage }]);
    setIsLoading(true);

    try {
      // Menembak Endpoint API Uvicorn di Port 8000
      const response = await axios.post('http://127.0.0.1:8000/chat', {
        message: userMessage
      });
      
      setMessages((prev) => [...prev, { sender: 'nexus', text: response.data.reply }]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev, 
        { sender: 'nexus', text: 'Error: Gagal terhubung ke saraf pusat backend. Pastikan server Uvicorn Anda menyala di port 8000.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* HEADER UTAMA */}
      <header style={styles.header}>
        <div style={styles.headerLeft}>
          <Activity size={24} color="#00ffcc" style={{ marginRight: '10px' }} />
          <h1 style={styles.title}>NEXUS <span style={{ color: '#00ffcc' }}>MEDIS V4</span></h1>
        </div>
        <div style={styles.statusBadge}>
          <div style={styles.pulseDot}></div>
          <span style={styles.statusText}>BACKEND ONLINE</span>
        </div>
      </header>

      {/* RUANG CHAT */}
      <div style={styles.chatArea}>
        {messages.map((msg, index) => (
          <div key={index} style={msg.sender === 'user' ? styles.userRow : styles.nexusRow}>
            <div style={msg.sender === 'user' ? styles.userIconBox : styles.nexusIconBox}>
              {msg.sender === 'user' ? <User size={18} /> : <Bot size={18} />}
            </div>
            <div style={msg.sender === 'user' ? styles.userBubble : styles.nexusBubble}>
              <p style={styles.messageText}>{msg.text}</p>
            </div>
          </div>
        ))}
        
        {/* INDIKATOR AI BERPIKIR */}
        {isLoading && (
          <div style={styles.nexusRow}>
            <div style={styles.nexusIconBox}>
              <Activity size={18} className="animate-pulse" color="#00ffcc" />
            </div>
            <div style={{ ...styles.nexusBubble, backgroundColor: '#1a2436' }}>
              <p style={{ ...styles.messageText, color: '#00ffcc', fontStyle: 'italic' }}>
                NEXUS sedang mengonstruksi kueri dan memindai OpenSearch...
              </p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* PANEL INPUT */}
      <form onSubmit={handleSend} style={styles.inputForm}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Tanyakan rekam medis, alergi, profil dokter, atau jadwal..."
          style={styles.inputField}
          disabled={isLoading}
        />
        <button type="submit" style={styles.sendButton} disabled={isLoading}>
          <Send size={18} color="#ffffff" />
        </button>
      </form>
    </div>
  );
}

// STYLING ENGINE (BUILT-IN AGAR BEBAS HUMAN ERROR KONFIGURASI CSS)
const styles = {
  container: { display: 'flex', flexDirection: 'column', height: '100vh', backgroundColor: '#0f172a', fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif', color: '#f8fafc' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '15px 25px', backgroundColor: '#1e293b', borderBottom: '1px solid #334155', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' },
  headerLeft: { display: 'flex', alignItems: 'center' },
  title: { fontSize: '1.2rem', fontWeight: 'bold', letterSpacing: '1px', margin: 0 },
  statusBadge: { display: 'flex', alignItems: 'center', backgroundColor: '#022c22', border: '1px solid #064e3b', padding: '6px 12px', borderRadius: '20px' },
  pulseDot: { width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%', marginRight: '8px', boxShadow: '0 0 8px #10b981' },
  statusText: { fontSize: '0.75rem', fontWeight: '600', color: '#a7f3d0' },
  chatArea: { flex: 1, overflowY: 'auto', padding: '20px 25px', display: 'flex', flexDirection: 'column', gap: '15px' },
  userRow: { display: 'flex', flexDirection: 'row-reverse', alignItems: 'flex-start', gap: '12px', marginLeft: '20%' },
  nexusRow: { display: 'flex', flexDirection: 'row', alignItems: 'flex-start', gap: '12px', marginRight: '20%' },
  userIconBox: { backgroundColor: '#3b82f6', padding: '8px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' },
  nexusIconBox: { backgroundColor: '#0f766e', padding: '8px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid #00ffcc' },
  userBubble: { backgroundColor: '#2563eb', padding: '12px 16px', borderRadius: '16px 4px 16px 16px', maxWidth: '100%' },
  nexusBubble: { backgroundColor: '#1e293b', padding: '12px 16px', borderRadius: '4px 16px 16px 16px', maxWidth: '100%', border: '1px solid #334155' },
  messageText: { margin: 0, fontSize: '0.95rem', lineHeight: '1.5', whiteSpace: 'pre-wrap' },
  inputForm: { display: 'flex', padding: '20px 25px', backgroundColor: '#1e293b', borderTop: '1px solid #334155', gap: '12px' },
  inputField: { flex: 1, backgroundColor: '#0f172a', border: '1px solid #475569', borderRadius: '8px', padding: '12px 16px', color: '#f8fafc', fontSize: '0.95rem', outline: 'none' },
  sendButton: { backgroundColor: '#0d9488', border: 'none', borderRadius: '8px', padding: '0 20px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', transition: 'background-color 0.2s' }
};

export default App;