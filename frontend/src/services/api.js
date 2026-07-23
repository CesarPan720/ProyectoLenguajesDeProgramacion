import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Origen del backend (sin el sufijo /api) para armar URLs de archivos estáticos (fotos/símbolos).
export const API_ORIGIN = import.meta.env.VITE_API_URL.replace(/\/api\/?$/, '')

export default api
