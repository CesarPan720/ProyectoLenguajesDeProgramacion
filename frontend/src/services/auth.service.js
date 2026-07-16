import api from './api'

export function verificarIdentidad(dni) {
  return api.post('/auth/verificar', { dni }).then((res) => res.data)
}
