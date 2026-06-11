import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, Activity, ChevronDown, ChevronRight, Info, MessageSquare, Layers, Hospital } from 'lucide-react';
import './App.css';

const contohPertanyaan = [
  "Berapa total tagihan rumah sakit?",
  "Diagnosa apa yang paling sering?",
  "Berapa jumlah dokter per spesialisasi?",
  "Siapa pasien yang alergi kacang?",
  "Dokter spesialis Pediatri siapa saja?",
  "Berapa tagihan yang belum lunas?",
];

const arsitekturItems = [
  { label: "Frontend", detail: "React + Vite (port 5173)" },
  { label: "Backend API", detail: "FastAPI + Uvicorn (port 8000)" },
  { label: "AI Engine", detail: "LangChain Agent + Llama-3.3-70B (Groq)" },
  { label: "Search Engine", detail: "OpenSearch (KNN Vector + BM25)" },
  { label: "Embedding Model", detail: "paraphrase-multilingual-MiniLM-L12-v2" },
  { label: "Analytics", detail: "OpenSearch Aggregation (Tagihan, Diagnosa, Dokter)" },
];

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Selamat datang di QA System Rumah Sakit Sehat Selalu. Silakan ajukan pertanyaan seputar data rumah sakit.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [openSection, setOpenSection] = useState('tentang');
  const [backendStatus, setBackendStatus] = useState('checking');
  const messagesEndRef = useRef(null);

  // Health check backend setiap 10 detik
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await axios.get('http://127.0.0.1:8000/health', { timeout: 3000 });
        setBackendStatus('online');
      } catch {
        setBackendStatus('offline');
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/chat', {
        message: userMessage
      });
      setMessages((prev) => [...prev, { sender: 'bot', text: response.data.reply }]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Gagal terhubung ke backend. Pastikan server Uvicorn menyala di port 8000.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleContohClick = (pertanyaan) => {
    setInput(pertanyaan);
  };

  const toggleSection = (section) => {
    setOpenSection(openSection === section ? '' : section);
  };

  const statusConfig = {
    online: { label: 'Online', dotClass: 'status-dot-online', badgeClass: 'status-badge-online' },
    offline: { label: 'Offline', dotClass: 'status-dot-offline', badgeClass: 'status-badge-offline' },
    checking: { label: 'Mengecek...', dotClass: 'status-dot-checking', badgeClass: 'status-badge-checking' },
  };

  const status = statusConfig[backendStatus];

  return (
    <div className="app-layout">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <Hospital size={22} className="sidebar-icon" />
          <div>
            <h1 className="sidebar-title">RS Sehat Selalu</h1>
            <p className="sidebar-subtitle">QA System</p>
          </div>
        </div>

        <nav className="sidebar-nav">
          {/* TENTANG */}
          <button className="nav-section-btn" onClick={() => toggleSection('tentang')}>
            <div className="nav-section-left">
              <Info size={16} />
              <span>Tentang</span>
            </div>
            {openSection === 'tentang' ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          </button>
          {openSection === 'tentang' && (
            <div className="nav-section-content">
              <p>
                Sistem tanya jawab berbasis AI untuk mengakses data Rumah Sakit Sehat Selalu.
                Didukung oleh pencarian semantik (KNN Vector) dan pencarian kata kunci (BM25)
                melalui OpenSearch, serta analitik agregasi untuk data tagihan, diagnosa, dan dokter.
              </p>
              <p>
                Sistem ini menggunakan LLM Llama-3.3-70B sebagai reasoning engine
                yang memilih alat pencarian paling tepat untuk setiap pertanyaan.
              </p>
            </div>
          )}

          {/* CONTOH PERTANYAAN */}
          <button className="nav-section-btn" onClick={() => toggleSection('contoh')}>
            <div className="nav-section-left">
              <MessageSquare size={16} />
              <span>Contoh Pertanyaan</span>
            </div>
            {openSection === 'contoh' ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          </button>
          {openSection === 'contoh' && (
            <div className="nav-section-content">
              {contohPertanyaan.map((q, i) => (
                <button
                  key={i}
                  className="contoh-btn"
                  onClick={() => handleContohClick(q)}
                >
                  {q}
                </button>
              ))}
            </div>
          )}

          {/* ARSITEKTUR */}
          <button className="nav-section-btn" onClick={() => toggleSection('arsitektur')}>
            <div className="nav-section-left">
              <Layers size={16} />
              <span>Arsitektur</span>
            </div>
            {openSection === 'arsitektur' ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          </button>
          {openSection === 'arsitektur' && (
            <div className="nav-section-content">
              {arsitekturItems.map((item, i) => (
                <div key={i} className="arsitektur-item">
                  <span className="arsitektur-label">{item.label}</span>
                  <span className="arsitektur-detail">{item.detail}</span>
                </div>
              ))}
            </div>
          )}
        </nav>

        <div className="sidebar-footer">
          <p>Proyek Mata Kuliah ROBD</p>
          <p>Semester 6 - 2025</p>
        </div>
      </aside>

      {/* MAIN CHAT */}
      <main className="chat-main">
        <header className="chat-header">
          <h2 className="chat-header-title">QA System Rumah Sakit Sehat Selalu</h2>
          <div className={`status-badge ${status.badgeClass}`}>
            <div className={`status-dot ${status.dotClass}`}></div>
            <span>{status.label}</span>
          </div>
        </header>

        <div className="chat-area">
          {messages.map((msg, index) => (
            <div key={index} className={`msg-row ${msg.sender === 'user' ? 'msg-row-user' : 'msg-row-bot'}`}>
              <div className={`msg-avatar ${msg.sender === 'user' ? 'avatar-user' : 'avatar-bot'}`}>
                {msg.sender === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div className={`msg-bubble ${msg.sender === 'user' ? 'bubble-user' : 'bubble-bot'}`}>
                <p className="msg-text">{msg.text}</p>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="msg-row msg-row-bot">
              <div className="msg-avatar avatar-bot">
                <Activity size={16} className="loading-icon" />
              </div>
              <div className="msg-bubble bubble-bot bubble-loading">
                <p className="msg-text">Memproses pertanyaan...</p>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSend} className="chat-input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ketik pertanyaan tentang data rumah sakit..."
            className="chat-input"
            disabled={isLoading}
          />
          <button type="submit" className="send-btn" disabled={isLoading}>
            <Send size={18} />
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;