"""Pydantic models for shuttle bookings."""

from datetime import datetime

from pydantic import BaseModel, Field


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
