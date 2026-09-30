# Kontrak API

## Ringkasan

API ini melayani pemesanan kursi shuttle kampus untuk mahasiswa. Klien dapat mencari daftar
pemesanan, membuka satu pemesanan, membuat pemesanan baru, dan menghapusnya. Data adalah 12
contoh sintetis yang disimpan di memori proses. Tidak ada basis data. Server yang diulang
mengembalikan data contoh semula, dan pemesanan yang baru dibuat hilang.

Base URL lokal: `http://localhost:8000`
Base URL produksi: belum ada.

## Model data

Satu koleksi, `pemesanan`, bukan tiga tabel. Tidak ada `users` dan tidak ada entitas anak.

| Kolom | Tipe | Wajib | Keterangan |
|---|---|---|---|
| id | integer | ya | Dibuat server. Pemesanan baru memakai `max(id) + 1`. |
| nama_penumpang | string | ya | 2–80 karakter. |
| nim | string | ya | 8–12 digit, tanpa spasi. |
| rute | string | ya | Salah satu dari empat rute di bawah. |
| titik_jemput | string | ya | 2–80 karakter. |
| waktu_berangkat | datetime | ya | ISO 8601, contoh `2026-10-01T07:00:00`. |
| jumlah_kursi | integer | ya | 1 sampai 4. |

Rute yang diterima:

- Kampus Pusat → Stasiun Sudirman
- Kampus Pusat → Halte Blok M
- Asrama → Kampus Pusat
- Kampus Pusat → Terminal Lebak Bulus

## Autentikasi

Semua endpoint publik. Belum ada token. Tidak ada header `Authorization`.

## Endpoint

### `GET /health`

| Bagian | Isi |
|---|---|
| Tujuan | Memeriksa bahwa proses API hidup. |
| Auth | Publik. |
| Query params | Tidak ada. |
| Body permintaan | Tidak ada. |
| Balasan 2xx | `200` — `{"status":"ok"}` |
| Balasan error | Tidak ada kasus error yang disengaja. |

### `GET /bookings`

| Bagian | Isi |
|---|---|
| Tujuan | Daftar pemesanan, dengan pencarian dan paginasi offset. |
| Auth | Publik. |
| Query params | `q` string, opsional, default kosong. Cocokkan tanpa memedulikan huruf besar pada nama, NIM, atau rute. `skip` integer, default `0`, minimum `0`. `limit` integer, default `6`, minimum `1`, maksimum `100`. |
| Body permintaan | Tidak ada. |
| Balasan 2xx | `200`. Contoh: `{"items":[{"id":1,"nama_penumpang":"Sari Wulandari","nim":"25120500011","rute":"Kampus Pusat → Stasiun Sudirman","titik_jemput":"Gerbang utama","waktu_berangkat":"2026-10-01T07:00:00","jumlah_kursi":1}],"total":12,"skip":0,"limit":6}` |
| Balasan error | `422` bila `skip` negatif atau `limit` di luar 1–100. Pencarian yang tidak cocok tetap `200` dengan `items: []` dan `total: 0`. |

### `GET /bookings/{id}`

| Bagian | Isi |
|---|---|
| Tujuan | Satu pemesanan. |
| Auth | Publik. |
| Query params | Tidak ada. `id` ada di path dan harus integer. |
| Body permintaan | Tidak ada. |
| Balasan 2xx | `200` — `{"id":1,"nama_penumpang":"Sari Wulandari","nim":"25120500011","rute":"Kampus Pusat → Stasiun Sudirman","titik_jemput":"Gerbang utama","waktu_berangkat":"2026-10-01T07:00:00","jumlah_kursi":1}` |
| Balasan error | `404` — `{"detail":"Pemesanan tidak ditemukan"}`. `422` bila `id` bukan integer. |

### `POST /bookings`

| Bagian | Isi |
|---|---|
| Tujuan | Membuat satu pemesanan. |
| Auth | Publik. |
| Query params | Tidak ada. |
| Body permintaan | JSON tanpa `id`. Contoh: `{"nama_penumpang":"Citra Lestari","nim":"25120500999","rute":"Asrama → Kampus Pusat","titik_jemput":"Asrama putri","waktu_berangkat":"2026-10-04T08:00:00","jumlah_kursi":2}` |
| Balasan 2xx | `201` dengan objek pemesanan yang sama bentuknya seperti detail, termasuk `id` baru. |
| Balasan error | `422` bila nama, NIM, rute, titik jemput, waktu, atau jumlah kursi tidak memenuhi aturan di model data. Badan mengikuti bentuk validasi FastAPI (`detail` berupa daftar). |

### `DELETE /bookings/{id}`

| Bagian | Isi |
|---|---|
| Tujuan | Menghapus satu pemesanan. |
| Auth | Publik. |
| Query params | Tidak ada. `id` ada di path. |
| Body permintaan | Tidak ada. |
| Balasan 2xx | `204` tanpa badan. |
| Balasan error | `404` — `{"detail":"Pemesanan tidak ditemukan"}`. |

## Status code yang dipakai

| Kode | Kapan dipakai di API ini |
|---|---|
| 200 | Daftar pemesanan, detail pemesanan, dan `/health`. |
| 201 | `POST /bookings` berhasil. |
| 204 | `DELETE /bookings/{id}` berhasil. Badan kosong. |
| 400 | Tidak dipakai. Isian yang gagal divalidasi membalas 422, bukan 400. |
| 422 | Query tidak valid, path `id` bukan integer, atau badan JSON gagal validasi Pydantic. |
| 401 vs 403 | Tidak dipakai. Tidak ada login, jadi tidak ada pembedaan "belum masuk" dan "tidak berhak". |
| 404 | `id` pemesanan tidak ada pada GET detail atau DELETE. |

## CORS

Origin yang diizinkan dibaca dari variabel lingkungan `CORS_ORIGINS`, dipisah koma. Bila tidak
diset, yang diizinkan hanya `http://localhost:5173`.

## Versioning

Kontrak ini mengikuti kode di repo. Belum ada klien di luar aplikasi Vue ini. Perubahan bentuk
JSON atau nama field dilakukan di dokumen ini pada commit yang sama dengan perubahan kodenya.
Tidak ada prefix versi seperti `/v1`.
