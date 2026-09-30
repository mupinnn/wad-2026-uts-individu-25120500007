import os

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import BookingCreate, BookingList, BookingOut
from app.services import create_booking, delete_booking, get_booking, list_bookings

app = FastAPI(title="Shuttle Booking")

_origins = [
    origin.strip()
    for origin in os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/bookings", status_code=201, response_model=BookingOut)
def add_booking(body: BookingCreate):
    return create_booking(body.model_dump())


@app.delete("/bookings/{booking_id}", status_code=204)
def remove_booking(booking_id: int):
    if not delete_booking(booking_id):
        raise HTTPException(status_code=404, detail="Pemesanan tidak ditemukan")
    return Response(status_code=204)
