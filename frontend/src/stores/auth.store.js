import { defineStore } from 'pinia'
import { verificarIdentidad } from '@/services/auth.service'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    dni: null,
    verificado: false,
    error: null
  }),
  actions: {
    async verificar(dni) {
      this.error = null
      try {
        await verificarIdentidad(dni)
        this.dni = dni
        this.verificado = true
        return true
      } catch (err) {
        this.error = err.response?.data?.detail ?? 'Error al verificar identidad.'
        this.verificado = false
        return false
      }
    },
    reiniciar() {
      this.dni = null
      this.verificado = false
      this.error = null
    }
  }
})
