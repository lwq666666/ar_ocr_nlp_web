import request from '@/utils/request'

export function showPageListTest() {
    return request({
        url: '/exhibision/actionData',
        method: 'get'
    })
}

export function login(account, password) {
    return request({
        url: '/login',
        method: 'post',
        params: { account: account, password: password }
    })
}

export function logout() {
    return request({
        url: '/logout',
        method: 'get'
    })
}

export function updateAccount(newPassword) {
    return request({
        url: '/account',
        method: 'put',
        params: { newPassword: newPassword }
    })
}

export function getUserInfo() {
    return request({
        url: '/user/roles',
        method: 'get'
    })
}