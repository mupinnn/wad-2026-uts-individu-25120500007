const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

export const RUTE_OPTIONS = [
  "Kampus Pusat → Stasiun Sudirman",
  "Kampus Pusat → Halte Blok M",
  "Asrama → Kampus Pusat",
  "Kampus Pusat → Terminal Lebak Bulus",
] as const

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

export type BookingInput = {
  nama_penumpang: string
  nim: string
  rute: string
  titik_jemput: string
  waktu_berangkat: string
  jumlah_kursi: number
}

export function describeError(error: unknown, fallback: string) {
  if (error instanceof TypeError) return "Tidak dapat menghubungi server."
  if (error instanceof Error && error.message) return error.message
  return fallback
}

export class ApiError extends Error {
  status: number
  fields: Record<string, string>

  constructor(message: string, status: number, fields: Record<string, string> = {}) {
    super(message)
    this.status = status
    this.fields = fields
  }
}

async function readError(response: Response, fallback: string): Promise<ApiError> {
  try {
    const body = await response.json()
    if (typeof body.detail === "string") {
      return new ApiError(body.detail, response.status)
    }
    if (Array.isArray(body.detail)) {
      const fields: Record<string, string> = {}
      for (const item of body.detail) {
        const loc = Array.isArray(item.loc) ? item.loc : []
        const field = String(loc[loc.length - 1] ?? "")
        if (field && field !== "body") fields[field] = String(item.msg ?? "Isian tidak valid")
      }
      return new ApiError("Periksa kembali isian formulir.", response.status, fields)
    }
  } catch {
    // The body was not JSON.
  }
  return new ApiError(fallback, response.status)
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
    throw await readError(response, "Gagal memuat daftar pemesanan")
  }
  return response.json()
}

export async function getBooking(id: number): Promise<Booking> {
  const response = await fetch(`${API_URL}/bookings/${id}`)
  if (!response.ok) {
    throw await readError(response, "Gagal memuat detail pemesanan")
  }
  return response.json()
}

export async function createBooking(input: BookingInput): Promise<Booking> {
  const response = await fetch(`${API_URL}/bookings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw await readError(response, "Gagal menyimpan pemesanan")
  }
  return response.json()
}

export async function deleteBooking(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/bookings/${id}`, { method: "DELETE" })
  if (!response.ok) {
    throw await readError(response, "Gagal menghapus pemesanan")
  }
}
