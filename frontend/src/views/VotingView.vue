<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useCandidatosStore } from '@/stores/candidatos.store'
import NavBar from '@/components/layout/NavBar.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseAlert from '@/components/common/BaseAlert.vue'

const auth = useAuthStore()
const candidatosStore = useCandidatosStore()
const router = useRouter()

const votando = ref(false)
const exito = ref(false)

onMounted(() => {
  candidatosStore.cargarCandidatos()
})

async function votarPor(idCandidato) {
  votando.value = true
  const ok = await candidatosStore.votar(auth.dni, idCandidato)
  votando.value = false

  if (ok) {
    exito.value = true
    auth.reiniciar()
    setTimeout(() => router.push({ name: 'login' }), 2000)
  }
}
</script>

<template>
  <NavBar />
  <main class="max-w-2xl mx-auto mt-10 px-4">
    <h2 class="text-xl font-semibold mb-4 text-gray-800">Candidatos Disponibles</h2>

    <BaseAlert v-if="exito" variant="success" class="mb-4">
      ¡Su voto ha sido registrado correctamente!
    </BaseAlert>
    <BaseAlert v-if="candidatosStore.error" variant="error" class="mb-4">
      {{ candidatosStore.error }}
    </BaseAlert>

    <div v-if="!exito" class="grid gap-4 sm:grid-cols-2">
      <div
        v-for="candidato in candidatosStore.candidatos"
        :key="candidato.id"
        class="bg-white rounded-lg shadow-md p-5 flex flex-col justify-between"
      >
        <div>
          <h3 class="font-semibold text-gray-800">{{ candidato.nombre }}</h3>
          <p class="text-sm text-gray-500">{{ candidato.partido }}</p>
        </div>
        <BaseButton
          variant="primary"
          class="mt-4"
          :disabled="votando"
          @click="votarPor(candidato.id)"
        >
          Votar
        </BaseButton>
      </div>
    </div>
  </main>
</template>
