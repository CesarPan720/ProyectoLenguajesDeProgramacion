<script setup>
import { onMounted } from 'vue'
import { useCandidatosStore } from '@/stores/candidatos.store'
import NavBar from '@/components/layout/NavBar.vue'

const candidatosStore = useCandidatosStore()

onMounted(() => {
  candidatosStore.cargarResultados()
})
</script>

<template>
  <NavBar />
  <main class="max-w-2xl mx-auto mt-10 px-4">
    <h2 class="text-xl font-semibold mb-2 text-gray-800">Reporte de Resultados</h2>
    <p class="text-gray-600 mb-6">Total de votos emitidos: {{ candidatosStore.totalVotos }}</p>

    <div class="space-y-3">
      <div
        v-for="item in candidatosStore.resultados"
        :key="item.nombre"
        class="bg-white rounded-lg shadow-md p-4"
      >
        <div class="flex justify-between mb-1">
          <span class="font-medium text-gray-800">{{ item.nombre }}</span>
          <span class="text-sm text-gray-500">{{ item.votos }} votos ({{ item.porcentaje }}%)</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: item.porcentaje + '%' }" />
        </div>
      </div>
    </div>
  </main>
</template>
