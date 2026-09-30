<script setup lang="ts">
import { onMounted, ref, watch } from "vue"
import { describeError, getBooking, type Booking } from "@/lib/api"

const props = defineProps<{ id: number }>()
const emit = defineEmits<{
  back: []
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

watch(() => props.id, () => load())
onMounted(load)
</script>

<template>
  <section aria-labelledby="detail-heading">
    <button type="button" class="mb-4 text-sm text-muted-foreground underline" @click="emit('back')">
      Kembali ke daftar
    </button>

    <p v-if="status === 'loading'" role="status" class="py-10 text-center text-sm text-muted-foreground">
      Memuat detail pemesanan…
    </p>

    <div
      v-else-if="status === 'error'"
      role="alert"
      class="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-6 text-center"
    >
      <p class="text-sm">{{ errorMessage }}</p>
      <button type="button" class="mt-3 h-9 rounded-md border px-3 text-sm" @click="load">
        Coba lagi
      </button>
    </div>

    <template v-else-if="booking">
      <h2 id="detail-heading" class="text-lg font-semibold">{{ booking.nama_penumpang }}</h2>
      <dl class="mt-4 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
        <div>
          <dt class="text-muted-foreground">NIM</dt>
          <dd>{{ booking.nim }}</dd>
        </div>
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
      <button
        type="button"
        class="mt-6 h-10 rounded-md border border-destructive/40 px-4 text-sm text-destructive"
        @click="emit('remove', booking)"
      >
        Hapus pemesanan
      </button>
    </template>
  </section>
</template>
