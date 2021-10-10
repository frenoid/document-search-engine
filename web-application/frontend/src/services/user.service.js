import { authHeader } from '../helpers'

export const userService = {
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

function getUser () {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
  }

  return fetch(`${config.apiUrl}auth/users/me/`, requestOptions)
    .then(handleResponse)
    .then(user => {
      if (user.id) {
        localStorage.setItem('user', JSON.stringify(user))
      }
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
    }).then(() => getUser())
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
        localStorage.setItem('token', JSON.stringify(otp))
      }
      return otp
    }).then(() => getUser())
}

function logout () {
  // remove user from local storage to log user out
  localStorage.removeItem('user')
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
