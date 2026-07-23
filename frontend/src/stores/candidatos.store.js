import { defineStore } from 'pinia'
import { obtenerCandidatos, emitirVoto, obtenerResultados } from '@/services/candidatos.service'

export const useCandidatosStore = defineStore('candidatos', {
  state: () => ({
    candidatos: [],
    resultados: [],
    totalVotos: 0,
    error: null
  }),
  actions: {
    async cargarCandidatos() {
      this.candidatos = await obtenerCandidatos()
    },
    async votar(dni, fechaNacimiento, idCandidato) {
      this.error = null
      try {
        await emitirVoto(dni, fechaNacimiento, idCandidato)
        return true
      } catch (err) {
        this.error = err.response?.data?.detail ?? 'No se pudo registrar el voto.'
        return false
      }
    },
    async cargarResultados() {
      const data = await obtenerResultados()
      this.resultados = data.reporte
      this.totalVotos = data.total
    }
  }
})
