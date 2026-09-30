<script setup lang="ts">
import { reactive, ref } from "vue"
import { ApiError, describeError, RUTE_OPTIONS, createBooking } from "@/lib/api"

const emit = defineEmits<{
  cancel: []
  created: []
}>()

const form = reactive({
  nama_penumpang: "",
  nim: "",
  rute: "",
  titik_jemput: "",
  waktu_berangkat: "",
  jumlah_kursi: "1",
})

const errors = ref<Record<string, string>>({})
const formError = ref("")
const submitting = ref(false)

function validate() {
  const next: Record<string, string> = {}
  if (form.nama_penumpang.trim().length < 2) {
    next.nama_penumpang = "Nama minimal 2 karakter."
  }
  if (!/^\d{8,12}$/.test(form.nim.trim())) {
    next.nim = "NIM harus 8–12 digit."
  }
  if (!RUTE_OPTIONS.includes(form.rute as (typeof RUTE_OPTIONS)[number])) {
    next.rute = "Pilih salah satu rute."
  }
  if (form.titik_jemput.trim().length < 2) {
    next.titik_jemput = "Titik jemput minimal 2 karakter."
  }
  if (!form.waktu_berangkat) {
    next.waktu_berangkat = "Isi waktu berangkat."
  }
  const seats = Number(form.jumlah_kursi)
  if (!Number.isInteger(seats) || seats < 1 || seats > 4) {
    next.jumlah_kursi = "Jumlah kursi antara 1 dan 4."
  }
  errors.value = next
  return Object.keys(next).length === 0
}

async function submit() {
  formError.value = ""
  if (!validate()) return
  submitting.value = true
  try {
    await createBooking({
      nama_penumpang: form.nama_penumpang.trim(),
      nim: form.nim.trim(),
      rute: form.rute,
      titik_jemput: form.titik_jemput.trim(),
      waktu_berangkat: form.waktu_berangkat,
      jumlah_kursi: Number(form.jumlah_kursi),
    })
    emit("created")
  } catch (error) {
    if (error instanceof ApiError && Object.keys(error.fields).length > 0) {
      errors.value = error.fields
      formError.value = error.message
    } else {
      formError.value = describeError(error, "Gagal menyimpan pemesanan")
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section aria-labelledby="form-heading">
    <h2 id="form-heading" class="text-lg font-semibold">Pesan shuttle</h2>
    <p class="mt-1 text-sm text-muted-foreground">Isi data penumpang. Semua kolom wajib.</p>

    <form class="mt-4 flex flex-col gap-4" novalidate @submit.prevent="submit">
      <p v-if="formError" role="alert" class="text-sm text-destructive">{{ formError }}</p>

      <div class="flex flex-col gap-1">
        <label for="nama" class="text-sm font-medium">Nama penumpang</label>
        <input
          id="nama"
          v-model="form.nama_penumpang"
          type="text"
          autocomplete="name"
          class="h-10 rounded-md border bg-background px-3 text-sm"
          :aria-invalid="Boolean(errors.nama_penumpang)"
          aria-describedby="nama-error"
        />
        <p v-if="errors.nama_penumpang" id="nama-error" class="text-sm text-destructive">
          {{ errors.nama_penumpang }}
        </p>
      </div>

      <div class="flex flex-col gap-1">
        <label for="nim" class="text-sm font-medium">NIM</label>
        <input
          id="nim"
          v-model="form.nim"
          type="text"
          inputmode="numeric"
          class="h-10 rounded-md border bg-background px-3 text-sm"
          :aria-invalid="Boolean(errors.nim)"
          aria-describedby="nim-error"
        />
        <p v-if="errors.nim" id="nim-error" class="text-sm text-destructive">{{ errors.nim }}</p>
      </div>

      <div class="flex flex-col gap-1">
        <label for="rute" class="text-sm font-medium">Rute</label>
        <select
          id="rute"
          v-model="form.rute"
          class="h-10 rounded-md border bg-background px-3 text-sm"
          :aria-invalid="Boolean(errors.rute)"
          aria-describedby="rute-error"
        >
          <option value="">Pilih rute</option>
          <option v-for="rute in RUTE_OPTIONS" :key="rute" :value="rute">{{ rute }}</option>
        </select>
        <p v-if="errors.rute" id="rute-error" class="text-sm text-destructive">{{ errors.rute }}</p>
      </div>

      <div class="flex flex-col gap-1">
        <label for="jemput" class="text-sm font-medium">Titik jemput</label>
        <input
          id="jemput"
          v-model="form.titik_jemput"
          type="text"
          class="h-10 rounded-md border bg-background px-3 text-sm"
          :aria-invalid="Boolean(errors.titik_jemput)"
          aria-describedby="jemput-error"
        />
        <p v-if="errors.titik_jemput" id="jemput-error" class="text-sm text-destructive">
          {{ errors.titik_jemput }}
        </p>
      </div>

      <div class="flex flex-col gap-1 sm:flex-row sm:gap-4">
        <div class="flex flex-1 flex-col gap-1">
          <label for="waktu" class="text-sm font-medium">Waktu berangkat</label>
          <input
            id="waktu"
            v-model="form.waktu_berangkat"
            type="datetime-local"
            class="h-10 rounded-md border bg-background px-3 text-sm"
            :aria-invalid="Boolean(errors.waktu_berangkat)"
            aria-describedby="waktu-error"
          />
          <p v-if="errors.waktu_berangkat" id="waktu-error" class="text-sm text-destructive">
            {{ errors.waktu_berangkat }}
          </p>
        </div>
        <div class="flex w-full flex-col gap-1 sm:w-32">
          <label for="kursi" class="text-sm font-medium">Jumlah kursi</label>
          <input
            id="kursi"
            v-model="form.jumlah_kursi"
            type="number"
            min="1"
            max="4"
            class="h-10 rounded-md border bg-background px-3 text-sm"
            :aria-invalid="Boolean(errors.jumlah_kursi)"
            aria-describedby="kursi-error"
          />
          <p v-if="errors.jumlah_kursi" id="kursi-error" class="text-sm text-destructive">
            {{ errors.jumlah_kursi }}
          </p>
        </div>
      </div>

      <div class="flex flex-col gap-2 sm:flex-row">
        <button
          type="submit"
          class="h-10 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground disabled:opacity-50"
          :disabled="submitting"
        >
          {{ submitting ? "Menyimpan…" : "Simpan pemesanan" }}
        </button>
        <button type="button" class="h-10 rounded-md border px-4 text-sm" @click="emit('cancel')">
          Batal
        </button>
      </div>
    </form>
  </section>
</template>
