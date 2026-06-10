import os
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# IMPORT KEDUA SENJATA BARU KITA
from tools_vector import cari_makna_medis, cari_keyword_eksak 
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

print("[INFO] Membangkitkan Kognisi Llama-3.3-70B...")
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

# BERIKAN KEDUA SENJATA KE DALAM INVENTARIS AGEN
tools = [cari_makna_medis, cari_keyword_eksak] 

system_prompt = """Anda adalah 'NEXUS', AI Analitik tingkat lanjut.
Anda memiliki DUA alat pencarian. 
Jika pengguna mencari NAMA ORANG atau ISTILAH SPESIFIK (seperti "alergi kacang"), WAJIB gunakan alat 'cari_keyword_eksak'.
Jika alat pertama gagal, Anda diizinkan menggunakan alat kedua sebelum menyerah.

ATURAN MUTLAK:
1. JANGAN PERNAH MENGARANG DATA.
2. Abaikan teks Latin acak (Lorem Ipsum). Fokus pada entitas data medisnya.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    print("\n[NEXUS ONLINE] Kognisi Siap.")
    pertanyaan = "Siapa pasien yang memiliki alergi kacang?"
    print(f"\nUser: {pertanyaan}")
    hasil = agent_executor.invoke({"input": pertanyaan})
    print(f"\nNEXUS: {hasil['output']}")