import api from './api'

export function obtenerCandidatos() {
  return api.get('/candidatos').then((res) => res.data)
}

export function emitirVoto(dni, fechaNacimiento, idCandidato) {
  return api
    .post('/votos', { dni, fecha_nacimiento: fechaNacimiento, id_candidato: idCandidato })
    .then((res) => res.data)
}

export function obtenerResultados() {
  return api.get('/resultados').then((res) => res.data)
}
