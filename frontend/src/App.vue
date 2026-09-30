<script setup lang="ts">
import BookingList from "@/components/BookingList.vue"
</script>

<template>
  <div class="min-h-svh bg-background text-foreground">
    <header class="border-b px-4 py-4 sm:px-6">
      <h1 class="text-xl font-semibold">Shuttle Kampus</h1>
      <p class="text-sm text-muted-foreground">Pemesanan transportasi mahasiswa</p>
    </header>
    <main class="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
      <BookingList />
    </main>
  </div>
</template>
