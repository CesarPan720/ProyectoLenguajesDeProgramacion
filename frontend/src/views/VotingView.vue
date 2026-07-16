<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useCandidatosStore } from '@/stores/candidatos.store'
import BaseAlert from '@/components/common/BaseAlert.vue'

const auth = useAuthStore()
const candidatosStore = useCandidatosStore()
const router = useRouter()

const seleccionado = ref(null)
const errorSeleccion = ref(null)
const votando = ref(false)
const exito = ref(false)

const candidatosReales = computed(() =>
  candidatosStore.candidatos.filter((c) => c.nombre !== 'Voto en Blanco')
)
const votoEnBlanco = computed(() =>
  candidatosStore.candidatos.find((c) => c.nombre === 'Voto en Blanco')
)

onMounted(() => {
  candidatosStore.cargarCandidatos()
})

async function onSubmit() {
  errorSeleccion.value = null

  if (seleccionado.value === null) {
    errorSeleccion.value = 'Selecciona una opción antes de continuar.'
    return
  }

  votando.value = true
  const ok = await candidatosStore.votar(auth.dni, seleccionado.value)
  votando.value = false

  if (ok) {
    exito.value = true
    auth.reiniciar()
    setTimeout(() => router.push({ name: 'login' }), 2000)
  }
}
</script>

<template>
  <main class="max-w-lg mx-auto mt-12 px-4">
    <h2 class="text-2xl font-extrabold text-gray-900">Elección presidencial</h2>
    <p class="text-sm text-gray-500 mb-5">Marca una sola opción</p>

    <BaseAlert v-if="exito" variant="success" class="mb-4">
      ¡Su voto ha sido registrado correctamente!
    </BaseAlert>

    <form v-else class="space-y-3" @submit.prevent="onSubmit">
      <label
        v-for="(candidato, idx) in candidatosReales"
        :key="candidato.id"
        class="flex items-center gap-3 rounded-xl border-2 p-3 cursor-pointer transition-colors"
        :class="seleccionado === candidato.id ? 'border-cyan-600 bg-cyan-50' : 'border-gray-200 bg-white hover:border-gray-300'"
      >
        <input v-model="seleccionado" type="radio" :value="candidato.id" class="w-5 h-5 accent-cyan-700" />
        <span class="w-7 h-7 rounded-md bg-cyan-600 text-white text-sm font-bold flex items-center justify-center shrink-0">
          {{ idx + 1 }}
        </span>
        <span class="w-9 h-9 rounded-lg bg-gray-100 flex items-center justify-center shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5 text-gray-400">
            <circle cx="12" cy="8" r="3.2" />
            <path d="M5 20.5c0-3.6 3.1-6 7-6s7 2.4 7 6" />
          </svg>
        </span>
        <span>
          <p class="font-semibold text-gray-900 leading-tight">{{ candidato.nombre }}</p>
          <p class="text-xs text-gray-500">{{ candidato.partido }}</p>
        </span>
      </label>

      <div v-if="votoEnBlanco" class="border-t border-dashed border-gray-300 !mt-5 !mb-3" />

      <label
        v-if="votoEnBlanco"
        class="flex items-center gap-3 rounded-xl border-2 border-dashed p-3 cursor-pointer transition-colors"
        :class="seleccionado === votoEnBlanco.id ? 'border-cyan-600 bg-cyan-50' : 'border-gray-300 bg-white hover:border-gray-400'"
      >
        <input v-model="seleccionado" type="radio" :value="votoEnBlanco.id" class="w-5 h-5 accent-cyan-700" />
        <span class="w-7 h-7 rounded-md border-2 border-gray-300 shrink-0" />
        <span class="font-medium text-gray-700">Voto en blanco</span>
      </label>

      <BaseAlert v-if="errorSeleccion" variant="error">{{ errorSeleccion }}</BaseAlert>
      <BaseAlert v-if="candidatosStore.error" variant="error">{{ candidatosStore.error }}</BaseAlert>

      <button
        type="submit"
        :disabled="votando"
        class="w-full bg-gray-900 hover:bg-black text-white font-semibold rounded-full py-3 flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ votando ? 'enviando...' : 'continuar' }}
        <span v-if="!votando">→</span>
      </button>
    </form>
  </main>
</template>
