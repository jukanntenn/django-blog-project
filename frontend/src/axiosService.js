import axios from 'axios'

let apiTable = {
    production: 'https://www.zmrenwu.com',
    development: 'http://127.0.0.1:8010'
}

const baseURL = apiTable[process.env.environ]

const instance = axios.create({
    baseURL: baseURL,
    timeout: 10000,
});

export default instance