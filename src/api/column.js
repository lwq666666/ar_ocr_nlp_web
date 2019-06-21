import request from '@/utils/request'


export function getColumn() {
    return request({
        url: '/column/getColumn',
        method: 'get'
    })
}