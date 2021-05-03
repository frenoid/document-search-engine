
import { authHeader } from '../helpers'
const BASE_URL = 'http://0.0.0.0:8000/api/v1/'

function searchFiles (params) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader(),
        params,
    }
    return fetch(`${BASE_URL}files?search=${params.search}`, requestOptions).then(handleResponse)
}

function handleResponse (response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text)
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                location.reload(true)
            }

            const error = (data && data.error) || response.statusText
            return Promise.reject(error)
        } else if (response.status === 401) {
            const error = (data && data.error) || response.statusText
            return Promise.reject(error)
        }
        return data
    })
}

export { searchFiles }
