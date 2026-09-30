const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

export type Booking = {
  id: number
  nama_penumpang: string
  nim: string
  rute: string
  titik_jemput: string
  waktu_berangkat: string
  jumlah_kursi: number
}

export type BookingListResponse = {
  items: Booking[]
  total: number
  skip: number
  limit: number
}

export async function listBookings(
  q: string,
  skip: number,
  limit: number,
): Promise<BookingListResponse> {
  const params = new URLSearchParams({
    q,
    skip: String(skip),
    limit: String(limit),
  })
  const response = await fetch(`${API_URL}/bookings?${params}`)
  if (!response.ok) {
    throw new Error("Gagal memuat daftar pemesanan")
  }
  return response.json()
}
