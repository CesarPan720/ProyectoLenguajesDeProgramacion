<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useCandidatosStore } from '@/stores/candidatos.store'
import { API_ORIGIN } from '@/services/api'
import BaseAlert from '@/components/common/BaseAlert.vue'

const auth = useAuthStore()
const candidatosStore = useCandidatosStore()
const router = useRouter()

const paso = ref('seleccion') // 'seleccion' | 'confirmacion'
const seleccionado = ref(null)
const errorSeleccion = ref(null)
const confirmado = ref(false)
const votando = ref(false)
const exito = ref(false)

const candidatosReales = computed(() =>
  candidatosStore.candidatos.filter((c) => c.nombre !== 'Voto en Blanco')
)
const votoEnBlanco = computed(() =>
  candidatosStore.candidatos.find((c) => c.nombre === 'Voto en Blanco')
)

const candidatoSeleccionado = computed(() =>
  candidatosStore.candidatos.find((c) => c.id === seleccionado.value)
)
const numeroSeleccionado = computed(() => {
  const idx = candidatosReales.value.findIndex((c) => c.id === seleccionado.value)
  return idx === -1 ? null : idx + 1
})

onMounted(() => {
  candidatosStore.cargarCandidatos()
})

function irAConfirmacion() {
  errorSeleccion.value = null

  if (seleccionado.value === null) {
    errorSeleccion.value = 'Selecciona una opción antes de continuar.'
    return
  }

  paso.value = 'confirmacion'
}

function volverAElegir() {
  paso.value = 'seleccion'
  confirmado.value = false
}

async function confirmarVoto() {
  votando.value = true
  const ok = await candidatosStore.votar(auth.dni, auth.fechaNacimiento, seleccionado.value)
  votando.value = false

  if (ok) {
    exito.value = true
    auth.reiniciar()
    setTimeout(() => router.push({ name: 'login' }), 2000)
  }
}
</script>

<template>
  <main class="max-w-3xl mx-auto mt-12 px-4">
    <BaseAlert v-if="exito" variant="success" class="mb-4">
      ¡Su voto ha sido registrado correctamente!
    </BaseAlert>

    <template v-else-if="paso === 'confirmacion'">
      <h2 class="text-3xl font-extrabold text-gray-900">Confirma tu voto</h2>
      <p class="text-base text-gray-500 mb-6">Revisa que la selección sea correcta</p>

      <div class="flex items-center gap-4 rounded-2xl bg-[#6fcde8] p-5 mb-4">
        <span
          v-if="numeroSeleccionado"
          class="w-9 h-9 rounded-lg bg-gray-900 text-white text-lg font-bold flex items-center justify-center shrink-0"
        >
          {{ numeroSeleccionado }}
        </span>
        <span v-else class="w-9 h-9 rounded-lg border-2 border-gray-900 shrink-0" />
        <span v-if="candidatoSeleccionado?.foto" class="relative w-20 h-20 shrink-0">
          <img
            :src="`${API_ORIGIN}${candidatoSeleccionado.foto}`"
            :alt="candidatoSeleccionado.nombre"
            class="w-20 h-20 rounded-xl object-cover"
          />
          <img
            v-if="candidatoSeleccionado.simbolo"
            :src="`${API_ORIGIN}${candidatoSeleccionado.simbolo}`"
            :alt="`Símbolo de ${candidatoSeleccionado.nombre}`"
            class="absolute -bottom-1.5 -right-1.5 w-8 h-8 rounded-full ring-2 ring-white bg-white object-cover"
          />
        </span>
        <span v-else class="w-20 h-20 rounded-xl bg-white flex items-center justify-center shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="w-10 h-10 text-cyan-700">
            <circle cx="12" cy="8" r="3.2" />
            <path d="M5 20.5c0-3.6 3.1-6 7-6s7 2.4 7 6" />
          </svg>
        </span>
        <span>
          <p class="font-semibold text-gray-900 leading-tight text-xl">{{ candidatoSeleccionado?.nombre }}</p>
          <p class="text-sm text-gray-700">{{ candidatoSeleccionado?.partido }}</p>
        </span>
      </div>

      <div class="flex items-start gap-2 rounded-xl border border-amber-200 bg-white p-3 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 text-amber-500 shrink-0 mt-0.5">
          <path d="M12 2 1 21h22L12 2Zm0 6.5a1 1 0 0 1 1 1V14a1 1 0 1 1-2 0V9.5a1 1 0 0 1 1-1ZM12 18a1.25 1.25 0 1 1 0-2.5A1.25 1.25 0 0 1 12 18Z" />
        </svg>
        <p class="text-sm text-gray-700">
          Una vez confirmado, tu voto no podrá modificarse ni anularse. Verifica que sea tu elección definitiva.
        </p>
      </div>

      <label class="flex items-center gap-2 mb-4 cursor-pointer select-none">
        <input v-model="confirmado" type="checkbox" class="w-4 h-4 accent-gray-900" />
        <span class="text-sm text-gray-700">Confirmo que esta es mi elección definitiva</span>
      </label>

      <BaseAlert v-if="candidatosStore.error" variant="error" class="mb-4">
        {{ candidatosStore.error }}
      </BaseAlert>

      <div class="space-y-2">
        <button
          type="button"
          :disabled="!confirmado || votando"
          class="w-full bg-gray-900 hover:bg-black text-white font-semibold rounded-full py-3 flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          @click="confirmarVoto"
        >
          {{ votando ? 'enviando...' : 'confirmar voto' }}
          <span v-if="!votando">✓</span>
        </button>
        <button
          type="button"
          :disabled="votando"
          class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-full py-3 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          @click="volverAElegir"
        >
          volver a elegir
        </button>
      </div>
    </template>

    <template v-else>
      <h2 class="text-3xl font-extrabold text-gray-900">Elección presidencial</h2>
      <p class="text-base text-gray-500 mb-6">Marca una sola opción</p>

      <form class="space-y-4" @submit.prevent="irAConfirmacion">
        <label
          v-for="(candidato, idx) in candidatosReales"
          :key="candidato.id"
          class="flex items-center gap-4 rounded-2xl border-2 p-4 cursor-pointer transition-colors"
          :class="seleccionado === candidato.id ? 'border-cyan-600 bg-cyan-50' : 'border-gray-200 bg-white hover:border-gray-300'"
        >
          <input v-model="seleccionado" type="radio" :value="candidato.id" class="w-6 h-6 accent-cyan-700" />
          <span class="w-9 h-9 rounded-lg bg-cyan-600 text-white text-lg font-bold flex items-center justify-center shrink-0">
            {{ idx + 1 }}
          </span>
          <span v-if="candidato.foto" class="relative w-20 h-20 shrink-0">
            <img
              :src="`${API_ORIGIN}${candidato.foto}`"
              :alt="candidato.nombre"
              class="w-20 h-20 rounded-xl object-cover"
            />
            <img
              v-if="candidato.simbolo"
              :src="`${API_ORIGIN}${candidato.simbolo}`"
              :alt="`Símbolo de ${candidato.nombre}`"
              class="absolute -bottom-1.5 -right-1.5 w-8 h-8 rounded-full ring-2 ring-white bg-white object-cover"
            />
          </span>
          <span v-else class="w-20 h-20 rounded-xl bg-gray-100 flex items-center justify-center shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="w-10 h-10 text-gray-400">
              <circle cx="12" cy="8" r="3.2" />
              <path d="M5 20.5c0-3.6 3.1-6 7-6s7 2.4 7 6" />
            </svg>
          </span>
          <span>
            <p class="font-semibold text-gray-900 leading-tight text-lg">{{ candidato.nombre }}</p>
            <p class="text-sm text-gray-500">{{ candidato.partido }}</p>
          </span>
        </label>

        <div v-if="votoEnBlanco" class="border-t border-dashed border-gray-300 !mt-6 !mb-4" />

        <label
          v-if="votoEnBlanco"
          class="flex items-center gap-4 rounded-2xl border-2 border-dashed p-4 cursor-pointer transition-colors"
          :class="seleccionado === votoEnBlanco.id ? 'border-cyan-600 bg-cyan-50' : 'border-gray-300 bg-white hover:border-gray-400'"
        >
          <input v-model="seleccionado" type="radio" :value="votoEnBlanco.id" class="w-6 h-6 accent-cyan-700" />
          <span class="w-9 h-9 rounded-lg border-2 border-gray-300 shrink-0" />
          <span class="font-medium text-gray-700 text-lg">Voto en blanco</span>
        </label>

        <BaseAlert v-if="errorSeleccion" variant="error">{{ errorSeleccion }}</BaseAlert>

        <button
          type="submit"
          class="w-full bg-gray-900 hover:bg-black text-white font-semibold rounded-full py-3 flex items-center justify-center gap-2 transition-colors"
        >
          continuar
          <span>→</span>
        </button>
      </form>
    </template>
  </main>
</template>
