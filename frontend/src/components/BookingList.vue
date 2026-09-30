<script setup lang="ts">
import { onMounted, ref } from "vue"
import { listBookings, type Booking } from "@/lib/api"

const PAGE_SIZE = 6

const query = ref("")
const submittedQuery = ref("")
const page = ref(0)
const items = ref<Booking[]>([])
const total = ref(0)
const status = ref<"loading" | "empty" | "error" | "success">("loading")
const errorMessage = ref("")

const dateFormat = new Intl.DateTimeFormat("id-ID", {
  dateStyle: "medium",
  timeStyle: "short",
})

function formatWhen(value: string) {
  return dateFormat.format(new Date(value))
}

async function load() {
  status.value = "loading"
  errorMessage.value = ""
  try {
    const data = await listBookings(submittedQuery.value, page.value * PAGE_SIZE, PAGE_SIZE)
    items.value = data.items
    total.value = data.total
    status.value = data.total === 0 ? "empty" : "success"
  } catch (error) {
    items.value = []
    total.value = 0
    status.value = "error"
    errorMessage.value =
      error instanceof Error ? error.message : "Gagal memuat daftar pemesanan"
  }
}

function search() {
  submittedQuery.value = query.value.trim()
  page.value = 0
  load()
}

function previousPage() {
  if (page.value === 0) return
  page.value -= 1
  load()
}

function nextPage() {
  if ((page.value + 1) * PAGE_SIZE >= total.value) return
  page.value += 1
  load()
}

const rangeStart = () => (total.value === 0 ? 0 : page.value * PAGE_SIZE + 1)
const rangeEnd = () => Math.min(total.value, (page.value + 1) * PAGE_SIZE)

onMounted(load)
</script>

<template>
  <section aria-labelledby="daftar-heading">
    <div class="mb-4 flex flex-col gap-1">
      <h2 id="daftar-heading" class="text-lg font-semibold">Daftar pemesanan</h2>
      <p class="text-sm text-muted-foreground">Cari berdasarkan nama, NIM, atau rute.</p>
    </div>

    <form class="mb-4 flex flex-col gap-2 sm:flex-row" @submit.prevent="search">
      <label class="sr-only" for="cari">Cari pemesanan</label>
      <input
        id="cari"
        v-model="query"
        type="search"
        placeholder="Nama, NIM, atau rute"
        class="h-10 w-full rounded-md border bg-background px-3 text-sm"
      />
      <button
        type="submit"
        class="h-10 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground"
      >
        Cari
      </button>
    </form>

    <p v-if="status === 'loading'" role="status" class="py-10 text-center text-sm text-muted-foreground">
      Memuat pemesanan…
    </p>

    <div
      v-else-if="status === 'error'"
      role="alert"
      class="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-6 text-center"
    >
      <p class="text-sm">{{ errorMessage }}</p>
      <button
        type="button"
        class="mt-3 h-9 rounded-md border px-3 text-sm"
        @click="load"
      >
        Coba lagi
      </button>
    </div>

    <p
      v-else-if="status === 'empty'"
      class="rounded-lg border border-dashed px-4 py-10 text-center text-sm text-muted-foreground"
    >
      <template v-if="submittedQuery">
        Tidak ada pemesanan untuk “{{ submittedQuery }}”.
      </template>
      <template v-else>Belum ada pemesanan.</template>
    </p>

    <template v-else>
      <ul class="flex flex-col gap-3">
        <li
          v-for="item in items"
          :key="item.id"
          class="rounded-lg border bg-card px-4 py-3"
        >
          <p class="font-medium">{{ item.nama_penumpang }}</p>
          <p class="text-sm text-muted-foreground">NIM {{ item.nim }}</p>
          <p class="mt-2 text-sm">{{ item.rute }}</p>
          <p class="text-sm text-muted-foreground">
            {{ item.titik_jemput }} · {{ formatWhen(item.waktu_berangkat) }} ·
            {{ item.jumlah_kursi }} kursi
          </p>
        </li>
      </ul>

      <nav class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between" aria-label="Halaman">
        <p class="text-sm text-muted-foreground">
          Menampilkan {{ rangeStart() }}–{{ rangeEnd() }} dari {{ total }}
        </p>
        <div class="flex gap-2">
          <button
            type="button"
            class="h-9 rounded-md border px-3 text-sm disabled:opacity-40"
            :disabled="page === 0"
            @click="previousPage"
          >
            Sebelumnya
          </button>
          <button
            type="button"
            class="h-9 rounded-md border px-3 text-sm disabled:opacity-40"
            :disabled="(page + 1) * PAGE_SIZE >= total"
            @click="nextPage"
          >
            Berikutnya
          </button>
        </div>
      </nav>
    </template>
  </section>
</template>
