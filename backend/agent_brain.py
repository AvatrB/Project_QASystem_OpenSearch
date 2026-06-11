import os
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from tools_vector import cari_makna_medis, cari_keyword_eksak
from tools_analytics import hitung_statistik_tagihan, hitung_statistik_diagnosa, hitung_statistik_dokter
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

print("[INFO] Membangkitkan Kognisi Llama-3.3-70B...")
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

tools = [
    cari_makna_medis,
    cari_keyword_eksak,
    hitung_statistik_tagihan,
    hitung_statistik_diagnosa,
    hitung_statistik_dokter,
]

system_prompt = """Anda adalah asisten AI untuk sistem QA Rumah Sakit Sehat Selalu.
Anda memiliki 5 alat pencarian dan analitik.

PANDUAN PEMILIHAN ALAT:
1. Pertanyaan tentang UANG, BIAYA, TAGIHAN, PEMBAYARAN -> gunakan 'hitung_statistik_tagihan'
2. Pertanyaan tentang DIAGNOSA, PENYAKIT, TREN MEDIS -> gunakan 'hitung_statistik_diagnosa'
3. Pertanyaan tentang JUMLAH DOKTER, DISTRIBUSI SPESIALISASI -> gunakan 'hitung_statistik_dokter'
4. Pertanyaan tentang NAMA ORANG spesifik atau ISTILAH EKSAK -> gunakan 'cari_keyword_eksak'
5. Pertanyaan UMUM tentang konsep, gejala, atau pencarian luas -> gunakan 'cari_makna_medis'

ATURAN RESOLUSI DATA:
- Jika hasil pencarian mengandung 'pasien_id' berupa ObjectId tapi pengguna bertanya tentang NAMA PASIEN, WAJIB lakukan pencarian lanjutan menggunakan 'cari_keyword_eksak' atau 'cari_makna_medis' untuk menemukan nama pasien yang terkait.
- Jika hasil pencarian mengandung 'dokter_id' atau 'departemen_id' berupa ObjectId, lakukan pencarian lanjutan untuk menemukan nama dokter atau departemen yang terkait.
- Jika alat pertama gagal menemukan jawaban, coba alat lain yang relevan sebelum menyerah.
- SELALU berusaha menjawab dengan NAMA, bukan dengan ID. Pengguna tidak mengerti ObjectId.

ATURAN MUTLAK:
1. JANGAN PERNAH MENGARANG DATA. Jawab hanya berdasarkan hasil alat.
2. Abaikan teks Lorem Ipsum. Fokus pada entitas data medis yang valid.
3. Untuk pertanyaan angka/statistik, selalu gunakan alat analitik, JANGAN menghitung sendiri.
4. Jawab dalam Bahasa Indonesia yang jelas dan ringkas.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

if __name__ == "__main__":
    print("\n[QA System ONLINE] Siap.")
    pertanyaan = "Berapa total tagihan rumah sakit?"
    print(f"\nUser: {pertanyaan}")
    hasil = agent_executor.invoke({"input": pertanyaan})
    print(f"\nJawaban: {hasil['output']}")