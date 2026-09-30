from fastapi import FastAPI, HTTPException, Query

from app.schemas import BookingList, BookingOut
from app.services import get_booking, list_bookings

app = FastAPI(title="Shuttle Booking")


@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.get("/bookings", response_model=BookingList)
def read_bookings(
    q: str = Query(default=""),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=6, ge=1, le=100),
):
    items, total = list_bookings(q, skip, limit)
    return BookingList(items=items, total=total, skip=skip, limit=limit)


@app.get("/bookings/{booking_id}", response_model=BookingOut)
def read_booking(booking_id: int):
    booking = get_booking(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Pemesanan tidak ditemukan")
    return booking
