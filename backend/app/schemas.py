"""Pydantic models for shuttle bookings."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Rute = Literal[
    "Kampus Pusat → Stasiun Sudirman",
    "Kampus Pusat → Halte Blok M",
    "Asrama → Kampus Pusat",
    "Kampus Pusat → Terminal Lebak Bulus",
]


class BookingCreate(BaseModel):
    nama_penumpang: str = Field(min_length=2, max_length=80)
    nim: str = Field(pattern=r"^\d{8,12}$")
    rute: Rute
    titik_jemput: str = Field(min_length=2, max_length=80)
    waktu_berangkat: datetime
    jumlah_kursi: int = Field(ge=1, le=4)


class BookingOut(BaseModel):
    id: int
    nama_penumpang: str
    nim: str
    rute: str
    titik_jemput: str
    waktu_berangkat: datetime
    jumlah_kursi: int


class BookingList(BaseModel):
    items: list[BookingOut]
    total: int
    skip: int
    limit: int
