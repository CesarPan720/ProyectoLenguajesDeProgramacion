<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { esDniValido } from '@/utils/validadores'
import BaseAlert from '@/components/common/BaseAlert.vue'

const dni = ref('')
const fechaNacimiento = ref('')

const cargando = ref(false)
const errorFormato = ref(null)
const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  errorFormato.value = null

  if (!esDniValido(dni.value)) {
    errorFormato.value = 'El DNI debe tener estrictamente 8 dígitos numéricos.'
    return
  }

  if (!fechaNacimiento.value) {
    errorFormato.value = 'Debe ingresar su fecha de nacimiento.'
    return
  }

  cargando.value = true
  const ok = await auth.verificar(dni.value, fechaNacimiento.value)
  cargando.value = false

  if (ok) {
    router.push({ name: 'votacion' })
  }
}
</script>

<template>
  <main class="max-w-md mx-auto mt-16">
    <div class="text-center mb-6">
      <p class="text-sm text-gray-500 tracking-wide">Sistema de votación</p>
      <h1 class="text-3xl font-extrabold text-gray-900 mt-1">Elecciones presidenciales</h1>
    </div>

    <div class="rounded-2xl shadow-xl overflow-hidden">
      <div class="bg-cyan-700 text-white px-5 py-3 flex items-center justify-between">
        <div class="text-xs font-bold leading-tight">
          REPÚBLICA<br />DEL PERÚ
        </div>
        <div class="text-[10px] font-bold text-right leading-tight opacity-90">
          SISTEMA DE<br />VOTACIÓN ELECTRÓNICA
        </div>
      </div>

      <div class="bg-[#6fcde8] px-6 pt-6 pb-8">
        <form class="space-y-4" @submit.prevent="onSubmit">
          <div class="flex items-start gap-4">
            <div class="shrink-0 w-20 h-[6rem] rounded-xl bg-white flex items-center justify-center shadow">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" class="w-10 h-10 text-cyan-700" viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.2"/><path d="M5 20.5c0-3.6 3.1-6 7-6s7 2.4 7 6"/></svg>
            </div>

            <div class="flex-1 space-y-4">
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">número de dni</label>
                <input
                  v-model="dni"
                  type="text"
                  maxlength="8"
                  inputmode="numeric"
                  placeholder="12345678"
                  class="w-full rounded-lg border-0 px-4 py-2.5 text-gray-800 shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-800 placeholder-gray-400"
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">fecha de nacimiento</label>
                <input
                  v-model="fechaNacimiento"
                  type="date"
                  required
                  class="w-full rounded-lg border-0 px-4 py-2.5 text-gray-800 shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-800"
                />
              </div>
            </div>
          </div>

          <div class="select-none pointer-events-none text-cyan-100/70 overflow-hidden leading-tight">
            <p class="whitespace-nowrap text-sm font-bold tracking-widest">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</p>
            <p class="whitespace-nowrap text-sm font-bold tracking-widest">&lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt;</p>
          </div>

          <BaseAlert v-if="errorFormato" variant="error">{{ errorFormato }}</BaseAlert>
          <BaseAlert v-if="auth.error" variant="error">{{ auth.error }}</BaseAlert>

          <button
            type="submit"
            :disabled="cargando"
            class="w-full bg-gray-900 hover:bg-black text-white font-semibold rounded-full py-3 flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ cargando ? 'verificando...' : 'continuar' }}
            <span v-if="!cargando">→</span>
          </button>
        </form>
      </div>
    </div>

    <p class="text-center text-xs text-gray-400 mt-4 flex items-center justify-center gap-1">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5">
        <path d="M12 1a5 5 0 0 0-5 5v3H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2h-1V6a5 5 0 0 0-5-5Zm0 2a3 3 0 0 1 3 3v3H9V6a3 3 0 0 1 3-3Z" />
      </svg>
      tus datos están protegidos y tu voto es secreto
    </p>
  </main>
</template>
