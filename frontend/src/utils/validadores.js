const PATRON_DNI = /^\d{8}$/

export function esDniValido(dni) {
  return PATRON_DNI.test(dni)
}
