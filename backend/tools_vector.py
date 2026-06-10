from langchain_core.tools import tool
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer
from config import OPENSEARCH_URL, INDEX_NAME_VECTOR as INDEX_NAME


client = OpenSearch(
    hosts=[OPENSEARCH_URL],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    ssl_show_warn=False
)

print("[INFO] Memuat model ekstraksi untuk Senjata Semantik...")
encoder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# ==========================================
# SENJATA 1: PENCARIAN MAKNA (VEKTOR/K-NN)
# ==========================================
@tool
def cari_makna_medis(kueri: str) -> str:
    """
    GUNAKAN ALAT INI UNTUK: Mencari konsep, makna, atau gejala secara luas.
    Contoh: "Pasien dengan keluhan sakit perut", "Dokter yang menangani anak-anak".
    JANGAN GUNAKAN UNTUK: Mencari nama orang eksak atau istilah spesifik yang butuh kecocokan kata persis.
    """
    vektor_kueri = encoder.encode(kueri).tolist()
    body = {
        "size": 5,
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
        if not hits: return "Tidak ada data relevan dari pencarian vektor."
        return "\n\n---\n\n".join([f"[Sumber: {h['_source']['metadata'].get('source')}]\n{h['_source']['text']}" for h in hits])
    except Exception as e:
        return f"Error OpenSearch: {str(e)}"

# ==========================================
# SENJATA 2: PENCARIAN KATA KUNCI EKSAK (BM25)
# ==========================================
@tool
def cari_keyword_eksak(kata_kunci: str) -> str:
    """
    GUNAKAN ALAT INI UNTUK: Mencari kata yang spesifik, nama orang persis, atau istilah mutlak.
    Contoh: "Kacang", "Lalita", "Ifa Wasita", "Tim Hijau 42".
    Alat ini sangat mematikan dan presisi untuk mencari data yang gagal ditemukan oleh pencarian makna.
    """
    body = {
        "size": 5,
        "query": {
            "multi_match": {
                "query": kata_kunci,
                "fields": ["text", "metadata.nama", "metadata.diagnosis", "metadata.spesialisasi", "metadata.kategori"]
            }
        }
    }
    try:
        response = client.search(index=INDEX_NAME, body=body)
        hits = response["hits"]["hits"]
        if not hits: return "Tidak ada data relevan dari pencarian kata kunci eksak."
        return "\n\n---\n\n".join([f"[Sumber: {h['_source']['metadata'].get('source')}]\n{h['_source']['text']}" for h in hits])
    except Exception as e:
        return f"Error OpenSearch: {str(e)}"