<script setup>
import { computed, onMounted } from 'vue'
import { useCandidatosStore } from '@/stores/candidatos.store'

const candidatosStore = useCandidatosStore()

const ranking = computed(() =>
  candidatosStore.resultados
    .filter((r) => r.nombre !== 'Voto en Blanco')
    .slice()
    .sort((a, b) => b.porcentaje - a.porcentaje)
)
const votoEnBlanco = computed(() =>
  candidatosStore.resultados.find((r) => r.nombre === 'Voto en Blanco')
)

onMounted(() => {
  candidatosStore.cargarResultados()
})
</script>

<template>
  <main class="max-w-lg mx-auto mt-12 px-4">
    <h2 class="text-2xl font-extrabold text-gray-900">Resultados</h2>
    <p class="text-sm text-gray-500 mb-5">Elección presidencial</p>

    <div class="bg-white rounded-2xl shadow-md divide-y divide-gray-100 overflow-hidden">
      <div
        v-for="(item, idx) in ranking"
        :key="item.nombre"
        class="px-5 py-4"
      >
        <div class="flex items-baseline justify-between mb-2">
          <span class="font-semibold text-gray-900">{{ idx + 1 }} · {{ item.nombre }}</span>
          <span class="font-bold text-gray-900">{{ item.porcentaje }}%</span>
        </div>
        <div class="w-full bg-gray-100 rounded-full h-2">
          <div class="bg-cyan-600 h-2 rounded-full" :style="{ width: item.porcentaje + '%' }" />
        </div>
      </div>

      <div v-if="votoEnBlanco" class="px-5 py-4">
        <div class="flex items-baseline justify-between mb-2">
          <span class="text-gray-500">Voto en blanco</span>
          <span class="font-medium text-gray-500">{{ votoEnBlanco.porcentaje }}%</span>
        </div>
        <div class="w-full bg-gray-100 rounded-full h-2">
          <div class="bg-gray-400 h-2 rounded-full" :style="{ width: votoEnBlanco.porcentaje + '%' }" />
        </div>
      </div>

      <div class="px-5 py-3 text-xs text-gray-400">
        Total de votos emitidos: {{ candidatosStore.totalVotos }}
      </div>
    </div>
  </main>
</template>
