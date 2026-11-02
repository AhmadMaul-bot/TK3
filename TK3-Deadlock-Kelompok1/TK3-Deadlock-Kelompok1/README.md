# TK-3: Analisis dan Penanganan Deadlock

Tugas Kelompok K-3, mata kuliah Sistem Operasi (USA-WP2260110), Kelas D, tema Cloud dan Layanan Digital UMKM.
Kasus: lock tabel stok, lock transaksi pembayaran, dan slot kurir pada proses checkout.

**Kelompok 1**
- Ahmad Maulana
- Anggara Muzaky Bahtiar
- Padli Badzara Hanurbara

## Isi repositori

| Berkas | Keterangan |
|---|---|
| `banker.py` | Algoritma Banker (safety) dan pemeriksaan permintaan sumber daya (`--req`) |
| `data/data.json` | Matriks Allocation, Max, Available (5 proses, 3 sumber daya) |
| `data/data_unsafe.json` | Skenario uji: Available dikosongkan sehingga sistem unsafe |
| `rag/rag_matriks.dot`, `.png` | RAG keadaan saat ini dari matriks Allocation |
| `rag/rag_deadlock.dot`, `.png` | RAG ilustrasi deadlock (siklus tiga proses) pada checkout |
| `hasil/` | Keluaran program: `hasil_banker.txt`, `hasil_unsafe.txt`, `hasil_permintaan.txt` |

## Pemetaan kasus

| Kode | Entitas | Total unit |
|---|---|---|
| R1 | Lock tabel stok | 10 |
| R2 | Lock transaksi pembayaran | 5 |
| R3 | Slot kurir | 7 |

P0 checkout reguler, P1 checkout flash sale, P2 worker pembayaran, P3 penjadwal kurir, P4 job sinkronisasi stok.

Catatan data: lembar tugas tidak melampirkan matriks khusus kelas, sehingga dipakai matriks contoh baku
(Silberschatz dkk., 2018) yang dipetakan ke kasus checkout. Untuk memakai matriks lain, ganti isi `data/data.json`.

## Cara menjalankan

Kebutuhan: Python 3 (diuji pada 3.13) dan, untuk gambar RAG, Graphviz (`dot`).

```bash
# Algoritma Banker pada matriks
python3 banker.py data/data.json

# Skenario unsafe
python3 banker.py data/data_unsafe.json

# Periksa permintaan: --req <nomor_proses> <R1> <R2> <R3>
python3 banker.py data/data.json --req 1 1 0 2     # P1 meminta (1,0,2): diberikan
python3 banker.py data/data.json --req 4 3 3 0     # P4 meminta (3,3,0): ditolak

# Render ulang gambar RAG
dot -Tpng rag/rag_matriks.dot -o rag/rag_matriks.png
dot -Tpng rag/rag_deadlock.dot -o rag/rag_deadlock.png
```

## Ringkasan hasil

- Sistem berada pada **safe state**, urutan aman `P1 -> P3 -> P0 -> P2 -> P4`.
- Available `[0, 0, 0]` menghasilkan **UNSAFE**.
- Permintaan P1 `(1, 0, 2)` diberikan; permintaan P4 `(3, 3, 0)` ditolak karena hasil alokasinya unsafe.
- Strategi pencegahan yang direkomendasikan: urutan lock global (stok, pembayaran, kurir), batas waktu lock dengan rollback dan retry, serta pembatasan jumlah checkout bersamaan. Penjelasan lengkap ada pada laporan.

## Rujukan

Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating system concepts* (10th ed.). Wiley.
