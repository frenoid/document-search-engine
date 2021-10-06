export function authHeader () {
    // return authorization header with jwt token
    const token = JSON.parse(localStorage.getItem('token'))

    if (token && token.auth_token) {
        return { Authorization: 'Token ' + token.auth_token, 'Content-Type': 'application/json' }
    } else {
        return {}
    }
}
