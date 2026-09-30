<script setup lang="ts">
import { onMounted, ref, watch } from "vue"
import { describeError, listBookings, type Booking } from "@/lib/api"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

const props = defineProps<{ revision: number }>()
const emit = defineEmits<{
  create: []
  open: [id: number]
  remove: [booking: Booking]
}>()

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
    if (data.items.length === 0 && data.total > 0 && page.value > 0) {
      page.value -= 1
      return load()
    }
    items.value = data.items
    total.value = data.total
    status.value = data.total === 0 ? "empty" : "success"
  } catch (error) {
    items.value = []
    total.value = 0
    status.value = "error"
    errorMessage.value = describeError(error, "Gagal memuat daftar pemesanan")
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

watch(() => props.revision, () => load())
onMounted(load)
</script>

<template>
  <section aria-labelledby="daftar-heading">
    <div class="mb-4 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div class="flex flex-col gap-1">
        <h2 id="daftar-heading" class="text-lg font-semibold">Daftar pemesanan</h2>
        <p class="text-sm text-muted-foreground">Cari berdasarkan nama, NIM, atau rute.</p>
      </div>
      <Button type="button" @click="emit('create')">Pesan shuttle</Button>
    </div>

    <form class="mb-4 flex flex-col gap-2 sm:flex-row" @submit.prevent="search">
      <Label class="sr-only" for="cari">Cari pemesanan</Label>
      <Input
        id="cari"
        v-model="query"
        type="search"
        placeholder="Nama, NIM, atau rute"
        class="sm:flex-1"
      />
      <Button type="submit">Cari</Button>
    </form>

    <p v-if="status === 'loading'" role="status" class="py-10 text-center text-sm text-muted-foreground">
      Memuat pemesanan…
    </p>

    <Card v-else-if="status === 'error'" role="alert">
      <CardContent class="flex flex-col items-center gap-3 py-6 text-center">
        <p class="text-sm">{{ errorMessage }}</p>
        <Button type="button" variant="outline" @click="load">Coba lagi</Button>
      </CardContent>
    </Card>

    <Card v-else-if="status === 'empty'">
      <CardContent class="py-10 text-center text-sm text-muted-foreground">
        <template v-if="submittedQuery">
          Tidak ada pemesanan untuk “{{ submittedQuery }}”.
        </template>
        <template v-else>Belum ada pemesanan.</template>
      </CardContent>
    </Card>

    <template v-else>
      <ul class="flex flex-col gap-3">
        <li v-for="item in items" :key="item.id">
          <Card size="sm">
            <CardHeader>
              <CardTitle>{{ item.nama_penumpang }}</CardTitle>
              <CardDescription>NIM {{ item.nim }}</CardDescription>
            </CardHeader>
            <CardContent>
              <p>{{ item.rute }}</p>
              <p class="text-muted-foreground">
                {{ item.titik_jemput }} · {{ formatWhen(item.waktu_berangkat) }} ·
                {{ item.jumlah_kursi }} kursi
              </p>
            </CardContent>
            <CardFooter class="gap-2">
              <Button type="button" variant="outline" @click="emit('open', item.id)">
                Detail
              </Button>
              <Button type="button" variant="destructive" @click="emit('remove', item)">
                Hapus
              </Button>
            </CardFooter>
          </Card>
        </li>
      </ul>

      <nav class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between" aria-label="Halaman">
        <p class="text-sm text-muted-foreground">
          Menampilkan {{ rangeStart() }}–{{ rangeEnd() }} dari {{ total }}
        </p>
        <div class="flex gap-2">
          <Button type="button" variant="outline" :disabled="page === 0" @click="previousPage">
            Sebelumnya
          </Button>
          <Button
            type="button"
            variant="outline"
            :disabled="(page + 1) * PAGE_SIZE >= total"
            @click="nextPage"
          >
            Berikutnya
          </Button>
        </div>
      </nav>
    </template>
  </section>
</template>
