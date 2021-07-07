import axios from 'axios'

let host = 'http://localhost:8090'

// 登陆
export const login = params => { return axios.post(`${host}/user/login/`, params)};

// 注册
export const register = params => { return axios.post(`${host}/user/register/`, params)};
