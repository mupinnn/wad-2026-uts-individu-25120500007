<script setup lang="ts">
import { ref } from "vue"
import BookingDetail from "@/components/BookingDetail.vue"
import BookingForm from "@/components/BookingForm.vue"
import BookingList from "@/components/BookingList.vue"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"
import { deleteBooking, describeError, type Booking } from "@/lib/api"

const formOpen = ref(false)
const detailOpen = ref(false)
const selectedId = ref<number | null>(null)
const revision = ref(0)
const pendingDelete = ref<Booking | null>(null)
const deleteError = ref("")
const deleting = ref(false)

function openDetail(id: number) {
  selectedId.value = id
  detailOpen.value = true
}

function showList() {
  formOpen.value = false
  detailOpen.value = false
}

function askDelete(booking: Booking) {
  deleteError.value = ""
  pendingDelete.value = booking
}

function onDeleteOpen(open: boolean) {
  if (open || deleting.value) return
  pendingDelete.value = null
  deleteError.value = ""
}

function onConfirmDelete(event: Event) {
  event.preventDefault()
  const booking = pendingDelete.value
  if (!booking || deleting.value) return
  deleting.value = true
  deleteError.value = ""
  deleteBooking(booking.id)
    .then(() => {
      pendingDelete.value = null
      detailOpen.value = false
      revision.value += 1
    })
    .catch((error: unknown) => {
      deleteError.value = describeError(error, "Gagal menghapus pemesanan")
    })
    .finally(() => {
      deleting.value = false
    })
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
          <Button type="button" variant="outline" @click="showList">Daftar</Button>
          <Button type="button" variant="outline" @click="formOpen = true">Pesan</Button>
        </nav>
      </div>
    </header>

    <main class="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
      <BookingList
        :revision="revision"
        @create="formOpen = true"
        @open="openDetail"
        @remove="askDelete"
      />
      <BookingForm v-model:open="formOpen" @created="revision += 1" />
      <BookingDetail
        v-if="selectedId !== null"
        :id="selectedId"
        v-model:open="detailOpen"
        @remove="askDelete"
      />
    </main>

    <AlertDialog :open="pendingDelete !== null" @update:open="onDeleteOpen">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Hapus pemesanan?</AlertDialogTitle>
          <AlertDialogDescription>
            Pemesanan {{ pendingDelete?.nama_penumpang }} (NIM {{ pendingDelete?.nim }}) akan dihapus.
            Tindakan ini tidak dapat dibatalkan.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <p v-if="deleteError" role="alert" class="text-sm text-destructive">{{ deleteError }}</p>
        <AlertDialogFooter>
          <AlertDialogCancel :disabled="deleting">Batal</AlertDialogCancel>
          <AlertDialogAction variant="destructive" :disabled="deleting" @click.capture="onConfirmDelete">
            {{ deleting ? "Menghapus…" : "Hapus" }}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  </div>
</template>
