import os
from dotenv import load_dotenv

load_dotenv()

# 1. Kredensial AI
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Pangkalan Data Vektor
OPENSEARCH_URL = "http://localhost:9200"
INDEX_NAME_VECTOR = "rs_sehat_v4_pure"

# 3. Rute Sumber Data
DATA_FOLDER = r"C:\Tugas Folder\Semester 6\ROBD\Data_RS_OpenSearch"