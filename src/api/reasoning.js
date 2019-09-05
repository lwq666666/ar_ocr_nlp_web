import request from '@/utils/request'

export function reasoning(problem) {
    return request({
        url: '/reason/reasoning',
        method: 'get',
        params: {
            problem: problem
        }
    })
}