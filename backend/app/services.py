"""In-memory shuttle booking store."""

from datetime import datetime

RUTE_OPTIONS = (
    "Kampus Pusat → Stasiun Sudirman",
    "Kampus Pusat → Halte Blok M",
    "Asrama → Kampus Pusat",
    "Kampus Pusat → Terminal Lebak Bulus",
)

_BOOKINGS: list[dict] = [
    {
        "id": 1,
        "nama_penumpang": "Sari Wulandari",
        "nim": "25120500011",
        "rute": "Kampus Pusat → Stasiun Sudirman",
        "titik_jemput": "Gerbang utama",
        "waktu_berangkat": datetime(2026, 10, 1, 7, 0),
        "jumlah_kursi": 1,
    },
    {
        "id": 2,
        "nama_penumpang": "Bima Pratama",
        "nim": "25120500022",
        "rute": "Asrama → Kampus Pusat",
        "titik_jemput": "Asrama putra",
        "waktu_berangkat": datetime(2026, 10, 1, 7, 30),
        "jumlah_kursi": 1,
    },
    {
        "id": 3,
        "nama_penumpang": "Lestari Anindya",
        "nim": "25120500033",
        "rute": "Kampus Pusat → Halte Blok M",
        "titik_jemput": "Parkiran selatan",
        "waktu_berangkat": datetime(2026, 10, 1, 12, 15),
        "jumlah_kursi": 2,
    },
    {
        "id": 4,
        "nama_penumpang": "Dimas Nugraha",
        "nim": "25120500044",
        "rute": "Kampus Pusat → Terminal Lebak Bulus",
        "titik_jemput": "Halte depan kampus",
        "waktu_berangkat": datetime(2026, 10, 1, 16, 0),
        "jumlah_kursi": 1,
    },
    {
        "id": 5,
        "nama_penumpang": "Putri Rahayu",
        "nim": "25120500055",
        "rute": "Asrama → Kampus Pusat",
        "titik_jemput": "Asrama putri",
        "waktu_berangkat": datetime(2026, 10, 2, 6, 45),
        "jumlah_kursi": 1,
    },
    {
        "id": 6,
        "nama_penumpang": "Andi Saputra",
        "nim": "25120500066",
        "rute": "Kampus Pusat → Stasiun Sudirman",
        "titik_jemput": "Gerbang utama",
        "waktu_berangkat": datetime(2026, 10, 2, 8, 0),
        "jumlah_kursi": 3,
    },
    {
        "id": 7,
        "nama_penumpang": "Maya Kusuma",
        "nim": "25120500077",
        "rute": "Kampus Pusat → Halte Blok M",
        "titik_jemput": "Parkiran selatan",
        "waktu_berangkat": datetime(2026, 10, 2, 13, 30),
        "jumlah_kursi": 1,
    },
    {
        "id": 8,
        "nama_penumpang": "Reza Firmansyah",
        "nim": "25120500088",
        "rute": "Kampus Pusat → Terminal Lebak Bulus",
        "titik_jemput": "Halte depan kampus",
        "waktu_berangkat": datetime(2026, 10, 2, 17, 15),
        "jumlah_kursi": 2,
    },
    {
        "id": 9,
        "nama_penumpang": "Intan Maharani",
        "nim": "25120500099",
        "rute": "Asrama → Kampus Pusat",
        "titik_jemput": "Asrama putri",
        "waktu_berangkat": datetime(2026, 10, 3, 7, 0),
        "jumlah_kursi": 1,
    },
    {
        "id": 10,
        "nama_penumpang": "Fajar Hidayat",
        "nim": "25120500101",
        "rute": "Kampus Pusat → Stasiun Sudirman",
        "titik_jemput": "Gerbang utama",
        "waktu_berangkat": datetime(2026, 10, 3, 9, 30),
        "jumlah_kursi": 4,
    },
    {
        "id": 11,
        "nama_penumpang": "Nadia Permata",
        "nim": "25120500112",
        "rute": "Kampus Pusat → Halte Blok M",
        "titik_jemput": "Parkiran selatan",
        "waktu_berangkat": datetime(2026, 10, 3, 15, 0),
        "jumlah_kursi": 1,
    },
    {
        "id": 12,
        "nama_penumpang": "Yoga Setiawan",
        "nim": "25120500123",
        "rute": "Kampus Pusat → Terminal Lebak Bulus",
        "titik_jemput": "Halte depan kampus",
        "waktu_berangkat": datetime(2026, 10, 3, 18, 0),
        "jumlah_kursi": 2,
    },
]


def list_bookings(q: str, skip: int, limit: int) -> tuple[list[dict], int]:
    needle = q.strip().lower()
    matched = [
        booking
        for booking in _BOOKINGS
        if not needle
        or needle in booking["nama_penumpang"].lower()
        or needle in booking["nim"]
        or needle in booking["rute"].lower()
    ]
    return matched[skip : skip + limit], len(matched)


def get_booking(booking_id: int) -> dict | None:
    return next((booking for booking in _BOOKINGS if booking["id"] == booking_id), None)


def create_booking(data: dict) -> dict:
    next_id = max((booking["id"] for booking in _BOOKINGS), default=0) + 1
    booking = {"id": next_id, **data}
    _BOOKINGS.append(booking)
    return booking


def delete_booking(booking_id: int) -> bool:
    for index, booking in enumerate(_BOOKINGS):
        if booking["id"] == booking_id:
            del _BOOKINGS[index]
            return True
    return False
