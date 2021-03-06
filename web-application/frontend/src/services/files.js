
import { authHeader } from '../helpers'
const BASE_URL = `http://${location.hostname}:8000/api/v1/`

function searchFiles (params) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader(),
        params,
    }
    return fetch(`${BASE_URL}files?search=${params.search}`, requestOptions).then(handleResponse)
}

function getFileDetails (id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader(),
    }
    return fetch(`${BASE_URL}files/${id}`, requestOptions).then(handleResponse)
}

function upVote (data) {
    const requestOptions = {
        method: 'POST',
        headers: authHeader(),
        body: JSON.stringify(data),
    }
    return fetch(`${BASE_URL}files/${data.id}/upvote`, requestOptions).then(handleResponse)
}

function downVote (data) {
    const requestOptions = {
        method: 'POST',
        headers: authHeader(),
        body: JSON.stringify(data),
    }
    return fetch(`${BASE_URL}files/${data.id}/downvote`, requestOptions).then(handleResponse)
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

export { searchFiles, getFileDetails, upVote, downVote }
