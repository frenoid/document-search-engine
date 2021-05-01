
import { authHeader } from '../helpers'
const BASE_URL = 'http://0.0.0.0:8000/api/v1/files'

async  function searchFiles () {
    const requestOptions = {
        method: 'GET',
        headers: authHeader(),
    }
    return fetch(`${BASE_URL}/search`, requestOptions).then(handleResponse)
}
export { searchFiles }