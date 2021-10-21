import { authHeader } from '../helpers'

export const userService = {
  confirmOTP,
  getQRCode,
  verifyOTP,
  login,
  logout,
  register,
  getAll,
  getById,
  update,
  delete: _delete,
}
const config = {
  apiUrl: `http://${location.hostname}:8000/api/v1/`,
}

function confirmOTP (user) {
  const requestOptions = {
    method: 'PATCH',
    headers: authHeader(),
  }
  let loggedUser
  if (user) {
    loggedUser = user
  } else {
    loggedUser = localStorage.getItem('user')
  }
  console.log('loggedUser', loggedUser)
  let id = 1
  if (loggedUser && loggedUser.id) {
    id = loggedUser.id
  }
  return fetch(`${config.apiUrl}current-user/${id}`, requestOptions)
  .then(handleResponse)
  .then(result => console.log(result))
}

function getUser () {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  }

  return fetch(`${config.apiUrl}auth/users/me/`, requestOptions)
    .then(handleResponse)
    .then(user => {
      user.qrcode = null
      if (user.id) {
        localStorage.setItem('user', JSON.stringify(user))
      }
      console.log(localStorage.getItem('user'))
      console.log('callleddddd ', user)
      return user
    })
}

function login (email, password) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  }

  return fetch(`${config.apiUrl}auth/token/login/`, requestOptions)
    .then(handleResponse)
    .then(token => {
      if (token.auth_token) {
        localStorage.setItem('token', JSON.stringify(token))
      }
      return token
    }).then(() => getUser()).then((user) => getQRCode(user))
}

function verifyOTP (otp) {
  const requestOptions = {
    method: 'POST',
    headers: authHeader(),
    body: JSON.stringify({}),
  }

  return fetch(`${config.apiUrl}totp/login/${otp}/`, requestOptions)
    .then(handleResponse)
    .then(otp => {
      if (otp) {
        console.log('OTP response', otp)
        localStorage.setItem('token', JSON.stringify(otp))
      }
      return otp
    })
}

function logout () {
  // remove user from local storage to log user out
  console.log('loccccc')
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  localStorage.removeItem('access_token')
}

function register (user) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  }

  return fetch(`${config.apiUrl}auth/users/`, requestOptions).then(handleResponse)
}

function getAll () {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  }

  return fetch(`${config.apiUrl}/users`, requestOptions).then(handleResponse)
}

function getById (id) {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  }

  return fetch(`${config.apiUrl}/users/${id}`, requestOptions).then(handleResponse)
}

function getQRCode (user) {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  }

  return fetch(`${config.apiUrl}totp/create/`, requestOptions).then(handleResponse).then((data) => {
    localStorage.setItem('qrcode', JSON.stringify(data))
    return user
  })
}

function update (user) {
  const requestOptions = {
    method: 'PUT',
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  }

  return fetch(`${config.apiUrl}/users/${user.id}`, requestOptions).then(handleResponse)
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete (id) {
  const requestOptions = {
    method: 'DELETE',
    headers: authHeader(),
  }

  return fetch(`${config.apiUrl}/users/${id}`, requestOptions).then(handleResponse)
}

function handleResponse (response) {
  return response.text().then(text => {
    const data = text && JSON.parse(text)
    if (!response.ok) {
      if (response.status === 401) {
        // auto logout if 401 response returned from api
        logout()
        location.reload(true)
      }

      const error = (data && data.message) || response.statusText
      return Promise.reject(error)
    }

    return data
  })
}
