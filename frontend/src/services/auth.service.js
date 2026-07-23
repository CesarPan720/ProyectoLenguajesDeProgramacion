import api from './api'

export function verificarIdentidad(dni, fechaNacimiento) {
  return api
    .post('/auth/verificar', { dni, fecha_nacimiento: fechaNacimiento })
    .then((res) => res.data)
}
