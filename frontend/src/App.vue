<script setup lang="ts">
import { ref } from "vue"
import BookingDetail from "@/components/BookingDetail.vue"
import BookingForm from "@/components/BookingForm.vue"
import BookingList from "@/components/BookingList.vue"
import { deleteBooking, describeError, type Booking } from "@/lib/api"

type View = "list" | "form" | "detail"

const view = ref<View>("list")
const selectedId = ref<number | null>(null)
const revision = ref(0)
const pendingDelete = ref<Booking | null>(null)
const deleteError = ref("")
const deleting = ref(false)

function openDetail(id: number) {
  selectedId.value = id
  view.value = "detail"
}

function askDelete(booking: Booking) {
  deleteError.value = ""
  pendingDelete.value = booking
}

function cancelDelete() {
  if (deleting.value) return
  pendingDelete.value = null
  deleteError.value = ""
}

async function confirmDelete() {
  if (!pendingDelete.value) return
  deleting.value = true
  deleteError.value = ""
  try {
    await deleteBooking(pendingDelete.value.id)
    pendingDelete.value = null
    selectedId.value = null
    view.value = "list"
    revision.value += 1
  } catch (error) {
    deleteError.value = describeError(error, "Gagal menghapus pemesanan")
  } finally {
    deleting.value = false
  }
}

function onCreated() {
  view.value = "list"
  revision.value += 1
}
</script>

<template>
  <div class="min-h-svh bg-background text-foreground">
    <header class="border-b px-4 py-4 sm:px-6">
      <div class="mx-auto flex w-full max-w-3xl flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 class="text-xl font-semibold">Shuttle Kampus</h1>
          <p class="text-sm text-muted-foreground">Pemesanan transportasi mahasiswa</p>
        </div>
        <nav class="flex gap-2" aria-label="Utama">
          <button
            type="button"
            class="h-9 rounded-md border px-3 text-sm"
            @click="view = 'list'"
          >
            Daftar
          </button>
          <button
            type="button"
            class="h-9 rounded-md border px-3 text-sm"
            @click="view = 'form'"
          >
            Pesan
          </button>
        </nav>
      </div>
    </header>

    <main class="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
      <BookingList
        v-if="view === 'list'"
        :revision="revision"
        @create="view = 'form'"
        @open="openDetail"
        @remove="askDelete"
      />
      <BookingForm v-else-if="view === 'form'" @cancel="view = 'list'" @created="onCreated" />
      <BookingDetail
        v-else-if="selectedId !== null"
        :id="selectedId"
        @back="view = 'list'"
        @remove="askDelete"
      />
    </main>

    <div
      v-if="pendingDelete"
      class="fixed inset-0 z-10 flex items-end justify-center bg-foreground/40 p-4 sm:items-center"
      @click.self="cancelDelete"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-title"
        class="w-full max-w-md rounded-lg border bg-background p-4 shadow-lg"
      >
        <h2 id="confirm-title" class="text-lg font-semibold">Hapus pemesanan?</h2>
        <p class="mt-2 text-sm text-muted-foreground">
          Pemesanan {{ pendingDelete.nama_penumpang }} (NIM {{ pendingDelete.nim }}) akan dihapus.
          Tindakan ini tidak dapat dibatalkan.
        </p>
        <p v-if="deleteError" role="alert" class="mt-2 text-sm text-destructive">{{ deleteError }}</p>
        <div class="mt-4 flex flex-col gap-2 sm:flex-row sm:justify-end">
          <button
            type="button"
            class="h-10 rounded-md border px-4 text-sm"
            :disabled="deleting"
            @click="cancelDelete"
          >
            Batal
          </button>
          <button
            type="button"
            class="h-10 rounded-md bg-destructive px-4 text-sm font-medium text-white"
            :disabled="deleting"
            @click="confirmDelete"
          >
            {{ deleting ? "Menghapus…" : "Hapus" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
