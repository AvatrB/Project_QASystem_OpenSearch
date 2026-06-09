from langchain_core.tools import tool
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

# --- KONFIGURASI ABSOLUT ---
OPENSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "rs_sehat_v4_pure"

# Inisiasi koneksi global agar mesin tidak perlu memuat model berulang kali setiap kali AI bertanya
client = OpenSearch(
    hosts=[OPENSEARCH_URL],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    ssl_show_warn=False
)

print("[INFO] Memuat model ekstraksi untuk Senjata Semantik...")
encoder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

@tool
def cari_rekam_medis(kueri: str) -> str:
    """
    GUNAKAN ALAT INI UNTUK: Mencari data spesifik terkait riwayat pasien, profil dokter, departemen, tim medis, atau jadwal.
    Contoh: "Siapa dokter spesialis anak?", "Apa diagnosis dari Lalita?", "Sebutkan anggota Tim Hijau 42".
    DILARANG MENGGUNAKAN ALAT INI UNTUK: Menghitung total biaya atau kalkulasi matematika.
    """
    # Mengubah pertanyaan AI menjadi vektor matematika
    vektor_kueri = encoder.encode(kueri).tolist()
    
    # Eksekusi pencarian K-NN Murni
    body = {
        "size": 5, # Mengambil 5 dokumen paling relevan untuk menghemat token
        "query": {
            "knn": {
                "vector_field": {
                    "vector": vektor_kueri,
                    "k": 5
                }
            }
        }
    }
    
    try:
        response = client.search(index=INDEX_NAME, body=body)
        hits = response["hits"]["hits"]
        
        if not hits:
            return "Pencarian gagal. Tidak ada data yang relevan di pangkalan data."
        
        # Merakit dokumen yang ditemukan menjadi teks yang bisa dibaca oleh Llama-3
        hasil_format = []
        for hit in hits:
            sumber = hit["_source"]["metadata"].get("source", "Entitas Tidak Diketahui")
            teks = hit["_source"]["text"]
            hasil_format.append(f"[Sumber Berkas: {sumber}]\n{teks}")
            
        return "\n\n---\n\n".join(hasil_format)
    
    except Exception as e:
        return f"Terjadi kesalahan sistemik pada OpenSearch: {str(e)}"

# Protokol Uji Coba Mandiri
if __name__ == "__main__":
    print("\n[INFO] Menguji tembakan Senjata Semantik ke OpenSearch...")
    # Kita uji dengan mencari pasien yang alergi kacang berdasarkan data Anda
    hasil_tes = cari_rekam_medis.invoke("Siapa pasien yang memiliki alergi kacang?")
    print("\n=== HASIL EKSTRAKSI ===")
    print(hasil_tes)
    print("=======================\n")