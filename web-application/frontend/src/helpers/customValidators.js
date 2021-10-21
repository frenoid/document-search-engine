export const containsUppercase = value => {
  return /[A-Z]/.test(value)
}

export const containsLowercase = value => {
  return /[a-z]/.test(value)
}

export const containsNumber = value => {
  return /[0-9]/.test(value)
}

export const containsSpecial = value => {
  return /[#?!@$%^&*-]/.test(value)
}

export const passwordComplexity = value => {
  return (
    containsUppercase(value) &&
    containsLowercase(value) &&
    containsNumber(value) &&
    containsSpecial(value)
  )
}
