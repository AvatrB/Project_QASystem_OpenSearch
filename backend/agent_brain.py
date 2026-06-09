import os
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from tools_vector import cari_rekam_medis
from config import GROQ_API_KEY

# 1. Autentikasi
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# 2. Inisiasi Otak Analitik Llama-3
print("[INFO] Membangkitkan Kognisi Llama-3...")
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

# 3. Rakit Persenjataan
tools = [cari_rekam_medis]

# 4. Instruksi Inti (System Prompt)
system_prompt = """Anda adalah 'NEXUS', AI Analitik tingkat lanjut untuk Rumah Sakit Sehat Selalu.
Tugas Anda adalah menjawab pertanyaan pengguna secara presisi berdasarkan alat pencarian yang Anda miliki.

ATURAN MUTLAK:
1. JANGAN PERNAH MENGARANG DATA. Jika alat pencari mengembalikan data yang salah, tidak nyambung, atau hanya berisi diagnosis yang tidak relevan dengan pertanyaan, Anda WAJIB menjawab: "Maaf, data spesifik tersebut tidak ditemukan di dalam pangkalan data."
2. Jawab dengan bahasa Indonesia yang profesional, dingin, dan langsung pada intinya.
3. Sebagian besar data rekam medis mengandung teks acak/dummy (seperti bahasa Latin). ABAIKAN teks Latin tersebut. Fokus HANYA pada entitas terstruktur seperti nama, diagnosis, tanggal, atau tindakan medis.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 5. Kompilasi Agen
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    print("\n[NEXUS ONLINE] Kognisi Siap.")
    
    # Kita berikan pertanyaan yang sama persis
    pertanyaan = "Siapa pasien yang memiliki alergi kacang?"
    
    print(f"\nUser: {pertanyaan}")
    hasil = agent_executor.invoke({"input": pertanyaan})
    print(f"\nNEXUS: {hasil['output']}")