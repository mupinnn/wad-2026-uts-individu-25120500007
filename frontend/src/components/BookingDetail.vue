<script setup lang="ts">
import { ref, watch } from "vue"
import { describeError, getBooking, type Booking } from "@/lib/api"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

const props = defineProps<{ id: number }>()
const open = defineModel<boolean>("open", { required: true })

const emit = defineEmits<{
  remove: [booking: Booking]
}>()

const booking = ref<Booking | null>(null)
const status = ref<"loading" | "error" | "success">("loading")
const errorMessage = ref("")

const dateFormat = new Intl.DateTimeFormat("id-ID", {
  dateStyle: "full",
  timeStyle: "short",
})

async function load() {
  status.value = "loading"
  errorMessage.value = ""
  booking.value = null
  try {
    booking.value = await getBooking(props.id)
    status.value = "success"
  } catch (error) {
    status.value = "error"
    errorMessage.value = describeError(error, "Gagal memuat detail pemesanan")
  }
}

watch(
  () => [open.value, props.id] as const,
  ([isOpen]) => {
    if (isOpen) load()
  },
  { immediate: true },
)
</script>

<template>
  <Dialog v-model:open="open">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>
          {{ status === "success" && booking ? booking.nama_penumpang : "Detail pemesanan" }}
        </DialogTitle>
        <DialogDescription v-if="status === 'loading'">Memuat detail pemesanan…</DialogDescription>
        <DialogDescription v-else-if="status === 'error'">{{ errorMessage }}</DialogDescription>
        <DialogDescription v-else-if="booking">NIM {{ booking.nim }}</DialogDescription>
      </DialogHeader>

      <p v-if="status === 'loading'" role="status" class="text-sm text-muted-foreground">
        Memuat detail pemesanan…
      </p>

      <div v-else-if="status === 'error'" role="alert" class="flex flex-col gap-3">
        <Button type="button" variant="outline" @click="load">Coba lagi</Button>
      </div>

      <template v-else-if="booking">
        <dl class="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
          <div>
            <dt class="text-muted-foreground">Rute</dt>
            <dd>{{ booking.rute }}</dd>
          </div>
          <div>
            <dt class="text-muted-foreground">Titik jemput</dt>
            <dd>{{ booking.titik_jemput }}</dd>
          </div>
          <div>
            <dt class="text-muted-foreground">Waktu berangkat</dt>
            <dd>{{ dateFormat.format(new Date(booking.waktu_berangkat)) }}</dd>
          </div>
          <div>
            <dt class="text-muted-foreground">Jumlah kursi</dt>
            <dd>{{ booking.jumlah_kursi }}</dd>
          </div>
        </dl>
        <DialogFooter>
          <Button type="button" variant="destructive" @click="emit('remove', booking)">
            Hapus pemesanan
          </Button>
        </DialogFooter>
      </template>
    </DialogContent>
  </Dialog>
</template>
