from langchain_core.tools import tool
from opensearchpy import OpenSearch
from config import OPENSEARCH_URL, INDEX_NAME_VECTOR as INDEX_NAME

client = OpenSearch(
    hosts=[OPENSEARCH_URL],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    ssl_show_warn=False
)


@tool
def hitung_statistik_tagihan(pertanyaan: str) -> str:
    """
    GUNAKAN ALAT INI UNTUK: Pertanyaan tentang uang, biaya, tagihan, pembayaran, atau statistik keuangan.
    Contoh: "Berapa total tagihan?", "Rata-rata biaya pasien", "Berapa tagihan yang belum lunas?",
    "Total pendapatan rumah sakit", "Statistik pembayaran".
    Parameter pertanyaan: masukkan pertanyaan pengguna apa adanya.
    """
    try:
        must_clauses = [
            {"match": {"metadata.kategori": "tagihan"}}
        ]

        body_fetch = {
            "size": 500,
            "query": {"bool": {"must": must_clauses}}
        }

        response = client.search(index=INDEX_NAME, body=body_fetch)
        hits = response["hits"]["hits"]

        if not hits:
            return "Tidak ditemukan data tagihan."

        total = 0
        count = 0
        lunas = 0
        belum_lunas = 0
        tunai = 0
        transfer = 0
        asuransi = 0

        for h in hits:
            text = h["_source"]["text"]
            lines = text.split("\n")
            record = {}
            for line in lines:
                if ": " in line:
                    key, val = line.split(": ", 1)
                    record[key.strip()] = val.strip()

            biaya = record.get("total_biaya", "0")
            try:
                biaya_num = int(float(biaya))
                total += biaya_num
                count += 1
            except ValueError:
                continue

            status = record.get("status_pembayaran", "").lower()
            if "lunas" in status and "belum" not in status:
                lunas += 1
            elif "belum" in status:
                belum_lunas += 1

            metode = record.get("metode_pembayaran", "").lower()
            if "tunai" in metode:
                tunai += 1
            elif "transfer" in metode:
                transfer += 1
            elif "asuransi" in metode:
                asuransi += 1

        rata_rata = total // count if count > 0 else 0

        hasil = f"""=== STATISTIK TAGIHAN RUMAH SAKIT ===
Jumlah tagihan ditemukan: {count}
Total seluruh tagihan: Rp {total:,}
Rata-rata per tagihan: Rp {rata_rata:,}

Status Pembayaran:
- Lunas: {lunas}
- Belum Lunas: {belum_lunas}

Metode Pembayaran:
- Tunai: {tunai}
- Transfer: {transfer}
- Asuransi: {asuransi}"""

        return hasil

    except Exception as e:
        return f"Error saat menghitung statistik tagihan: {str(e)}"


@tool
def hitung_statistik_diagnosa(pertanyaan: str) -> str:
    """
    GUNAKAN ALAT INI UNTUK: Pertanyaan tentang diagnosa terbanyak, penyakit paling umum,
    distribusi penyakit, atau tren diagnosa di rumah sakit.
    Contoh: "Diagnosa apa yang paling sering?", "Penyakit terbanyak apa?",
    "Berapa pasien yang didiagnosa Diabetes?".
    Parameter pertanyaan: masukkan pertanyaan pengguna apa adanya.
    """
    try:
        body = {
            "size": 500,
            "query": {"match": {"metadata.kategori": "rekam_medis"}}
        }

        response = client.search(index=INDEX_NAME, body=body)
        hits = response["hits"]["hits"]

        if not hits:
            return "Tidak ditemukan data rekam medis."

        diagnosa_count = {}
        total_records = 0

        for h in hits:
            text = h["_source"]["text"]
            lines = text.split("\n")
            for line in lines:
                if line.strip().startswith("diagnosa:"):
                    diag = line.split(": ", 1)[1].strip()
                    if diag and diag.lower() != "none":
                        diagnosa_count[diag] = diagnosa_count.get(diag, 0) + 1
                        total_records += 1

        if not diagnosa_count:
            return "Tidak ditemukan data diagnosa dalam rekam medis."

        sorted_diag = sorted(diagnosa_count.items(), key=lambda x: x[1], reverse=True)

        hasil = f"=== DISTRIBUSI DIAGNOSA ({total_records} rekam medis) ===\n"
        for i, (diag, count) in enumerate(sorted_diag, 1):
            persen = round(count / total_records * 100, 1)
            hasil += f"{i}. {diag}: {count} kasus ({persen}%)\n"

        return hasil

    except Exception as e:
        return f"Error saat menghitung statistik diagnosa: {str(e)}"


@tool
def hitung_statistik_dokter(pertanyaan: str) -> str:
    """
    GUNAKAN ALAT INI UNTUK: Pertanyaan tentang jumlah dokter, distribusi spesialisasi,
    atau statistik tenaga medis.
    Contoh: "Berapa jumlah dokter?", "Spesialisasi apa yang paling banyak?",
    "Distribusi dokter per spesialisasi".
    Parameter pertanyaan: masukkan pertanyaan pengguna apa adanya.
    """
    try:
        body = {
            "size": 500,
            "query": {"match": {"metadata.kategori": "dokter"}}
        }

        response = client.search(index=INDEX_NAME, body=body)
        hits = response["hits"]["hits"]

        if not hits:
            return "Tidak ditemukan data dokter."

        spesialis_count = {}
        total_dokter = 0

        for h in hits:
            text = h["_source"]["text"]
            lines = text.split("\n")
            for line in lines:
                if line.strip().startswith("spesialisasi:"):
                    spec = line.split(": ", 1)[1].strip()
                    if spec and spec.lower() != "none":
                        spesialis_count[spec] = spesialis_count.get(spec, 0) + 1
                        total_dokter += 1

        if not spesialis_count:
            return "Tidak ditemukan data spesialisasi dokter."

        sorted_spec = sorted(spesialis_count.items(), key=lambda x: x[1], reverse=True)

        hasil = f"=== DISTRIBUSI DOKTER ({total_dokter} dokter) ===\n"
        for i, (spec, count) in enumerate(sorted_spec, 1):
            hasil += f"{i}. {spec}: {count} dokter\n"

        return hasil

    except Exception as e:
        return f"Error saat menghitung statistik dokter: {str(e)}"