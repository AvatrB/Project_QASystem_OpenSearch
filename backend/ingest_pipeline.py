import json
import os
from opensearchpy import OpenSearch, helpers
from sentence_transformers import SentenceTransformer

# --- KONFIGURASI ABSOLUT ---
DATA_FOLDER = r"C:\Tugas Folder\Semester 6\ROBD\Data_RS_OpenSearch"
OPENSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "rs_sehat_v4_pure"

print("[INFO] Menginisialisasi Klien OpenSearch Murni (Enterprise Mode)...")
client = OpenSearch(
    hosts=[OPENSEARCH_URL],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    ssl_show_warn=False,
    timeout=120,          
    max_retries=5,        
    retry_on_timeout=True 
)

print("[INFO] Memuat Model Vektor (paraphrase-multilingual)...")
encoder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Konfigurasi Index dengan Skema Metadata Ekstensif
index_body = {
    "settings": {
        "index": {"knn": True}
    },
    "mappings": {
        "properties": {
            "vector_field": {
                "type": "knn_vector",
                "dimension": 384,
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "lucene"
                }
            },
            "text": {"type": "text"},
            "metadata": {
                "properties": {
                    "source": {"type": "keyword"},
                    "kategori": {"type": "keyword"},
                    "nama": {"type": "keyword"},
                    "spesialisasi": {"type": "keyword"},
                    "diagnosis": {"type": "keyword"},
                    "keluhan": {"type": "text"}
                }
            }
        }
    }
}

# Hapus index lama untuk sterilisasi
if client.indices.exists(index=INDEX_NAME):
    print(f"[INFO] Menghapus indeks lama '{INDEX_NAME}'...")
    client.indices.delete(index=INDEX_NAME)
client.indices.create(index=INDEX_NAME, body=index_body)

print(f"[INFO] Memindai direktori data: {DATA_FOLDER}")
documents_batch = []

for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".json"):
        file_path = os.path.join(DATA_FOLDER, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                data = [data]
            
            for item in data:
                metadata = {"source": filename}
                
                # --- LOGIKA KLASIFIKASI METADATA PRESISI ---
                
                # 1. Klasifikasi Dokter
                if "spesialisasi" in item and "nama_dokter" in item:
                    metadata["kategori"] = "dokter"
                    metadata["nama"] = str(item.get("nama_dokter", ""))
                    metadata["spesialisasi"] = str(item.get("spesialisasi", ""))
                
                # 2. Klasifikasi Rekam Medis
                elif "diagnosa" in item or "keluhan_utama" in item:
                    metadata["kategori"] = "rekam_medis"
                    metadata["diagnosis"] = str(item.get("diagnosa", ""))
                    metadata["keluhan"] = str(item.get("keluhan_utama", ""))
                
                # 3. Klasifikasi Pasien
                elif "nama_pasien" in item and "golongan_darah" in item:
                    metadata["kategori"] = "pasien"
                    metadata["nama"] = str(item.get("nama_pasien", ""))
                
                # 4. Klasifikasi Departemen
                elif "nama_departemen" in item:
                    metadata["kategori"] = "departemen"
                    metadata["nama"] = str(item.get("nama_departemen", ""))
                
                # 5. Klasifikasi Tim Medis
                elif "nama_tim" in item:
                    metadata["kategori"] = "tim_medis"
                    metadata["nama"] = str(item.get("nama_tim", ""))
                
                # 6. Klasifikasi Tagihan
                elif "total_biaya" in item and "status_pembayaran" in item:
                    metadata["kategori"] = "tagihan"
                
                # 7. Fallback untuk data lainnya
                else:
                    metadata["kategori"] = "operasional"
                
                # Merakit konten teks (mengabaikan ID MongoDB agar tidak membuang token)
                content_lines = [f"{k}: {v}" for k, v in item.items() if k != "_id"]
                clean_content = "\n".join(content_lines)
                
                documents_batch.append({
                    "text": clean_content,
                    "metadata": metadata
                })

total_docs = len(documents_batch)
print(f"[INFO] {total_docs} dokumen dengan skema tervalidasi siap diproses.")

# ==========================================
# EKSEKUSI MASSAL (BULK API)
# ==========================================
actions = []
batch_size = 500

print("[INFO] Memulai injeksi massal ke OpenSearch...")
for i, doc in enumerate(documents_batch):
    # Enkode teks menjadi vektor
    vector = encoder.encode(doc["text"]).tolist()
    
    # Rakit peluru Bulk
    action = {
        "_index": INDEX_NAME,
        "_source": {
            "vector_field": vector,
            "text": doc["text"],
            "metadata": doc["metadata"]
        }
    }
    actions.append(action)
    
    # Eksekusi blok
    if len(actions) >= batch_size or (i + 1) == total_docs:
        try:
            helpers.bulk(client, actions)
            print(f"  -> Progress Injeksi Massal: {i + 1}/{total_docs} dokumen tereksekusi.")
            actions = [] 
        except Exception as e:
            print(f"[FATAL] Kegagalan pada injeksi massal blok {i+1}: {e}")

print("[INFO] Operasi pipa data selesai secara mutlak. Pangkalan Data terstruktur dengan sempurna.")