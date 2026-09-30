<script setup lang="ts">
import { reactive, ref, watch } from "vue"
import { ApiError, describeError, RUTE_OPTIONS, createBooking } from "@/lib/api"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const open = defineModel<boolean>("open", { required: true })

const emit = defineEmits<{
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

function reset() {
  form.nama_penumpang = ""
  form.nim = ""
  form.rute = ""
  form.titik_jemput = ""
  form.waktu_berangkat = ""
  form.jumlah_kursi = "1"
  errors.value = {}
  formError.value = ""
}

watch(open, (isOpen) => {
  if (isOpen) reset()
})

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
    open.value = false
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
  <Dialog v-model:open="open">
    <DialogContent class="max-h-[90svh] overflow-y-auto sm:max-w-md">
      <DialogHeader>
        <DialogTitle>Pesan shuttle</DialogTitle>
        <DialogDescription>Isi data penumpang. Semua kolom wajib.</DialogDescription>
      </DialogHeader>

      <form class="flex flex-col gap-4" novalidate @submit.prevent="submit">
        <p v-if="formError" role="alert" class="text-sm text-destructive">{{ formError }}</p>

        <div class="flex flex-col gap-1.5">
          <Label for="nama">Nama penumpang</Label>
          <Input
            id="nama"
            v-model="form.nama_penumpang"
            type="text"
            autocomplete="name"
            :aria-invalid="Boolean(errors.nama_penumpang)"
            aria-describedby="nama-error"
          />
          <p v-if="errors.nama_penumpang" id="nama-error" class="text-sm text-destructive">
            {{ errors.nama_penumpang }}
          </p>
        </div>

        <div class="flex flex-col gap-1.5">
          <Label for="nim">NIM</Label>
          <Input
            id="nim"
            v-model="form.nim"
            type="text"
            inputmode="numeric"
            :aria-invalid="Boolean(errors.nim)"
            aria-describedby="nim-error"
          />
          <p v-if="errors.nim" id="nim-error" class="text-sm text-destructive">{{ errors.nim }}</p>
        </div>

        <div class="flex flex-col gap-1.5">
          <Label for="rute">Rute</Label>
          <Select v-model="form.rute">
            <SelectTrigger
              id="rute"
              class="w-full"
              :aria-invalid="Boolean(errors.rute)"
              aria-describedby="rute-error"
            >
              <SelectValue placeholder="Pilih rute" />
            </SelectTrigger>
            <SelectContent class="z-[60]" position="popper">
              <SelectItem v-for="rute in RUTE_OPTIONS" :key="rute" :value="rute">
                {{ rute }}
              </SelectItem>
            </SelectContent>
          </Select>
          <p v-if="errors.rute" id="rute-error" class="text-sm text-destructive">{{ errors.rute }}</p>
        </div>

        <div class="flex flex-col gap-1.5">
          <Label for="jemput">Titik jemput</Label>
          <Input
            id="jemput"
            v-model="form.titik_jemput"
            type="text"
            :aria-invalid="Boolean(errors.titik_jemput)"
            aria-describedby="jemput-error"
          />
          <p v-if="errors.titik_jemput" id="jemput-error" class="text-sm text-destructive">
            {{ errors.titik_jemput }}
          </p>
        </div>

        <div class="flex flex-col gap-4 sm:flex-row">
          <div class="flex flex-1 flex-col gap-1.5">
            <Label for="waktu">Waktu berangkat</Label>
            <Input
              id="waktu"
              v-model="form.waktu_berangkat"
              type="datetime-local"
              :aria-invalid="Boolean(errors.waktu_berangkat)"
              aria-describedby="waktu-error"
            />
            <p v-if="errors.waktu_berangkat" id="waktu-error" class="text-sm text-destructive">
              {{ errors.waktu_berangkat }}
            </p>
          </div>
          <div class="flex w-full flex-col gap-1.5 sm:w-28">
            <Label for="kursi">Jumlah kursi</Label>
            <Input
              id="kursi"
              v-model="form.jumlah_kursi"
              type="number"
              min="1"
              max="4"
              :aria-invalid="Boolean(errors.jumlah_kursi)"
              aria-describedby="kursi-error"
            />
            <p v-if="errors.jumlah_kursi" id="kursi-error" class="text-sm text-destructive">
              {{ errors.jumlah_kursi }}
            </p>
          </div>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" @click="open = false">Batal</Button>
          <Button type="submit" :disabled="submitting">
            {{ submitting ? "Menyimpan…" : "Simpan pemesanan" }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
