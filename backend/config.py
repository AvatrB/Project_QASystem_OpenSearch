import os

# 1. Kredensial AI
GROQ_API_KEY = "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"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# 2. Pangkalan Data Vektor
OPENSEARCH_URL = "http://localhost:9200"
INDEX_NAME_VECTOR = "rs_sehat_v4_pure"

# 3. Rute Sumber Data
# PASTIKAN RUTE INI BENAR MENGARAH KE FOLDER JSON ANDA
DATA_FOLDER = r"C:\Tugas Folder\Semester 6\ROBD\Data_RS_OpenSearch"