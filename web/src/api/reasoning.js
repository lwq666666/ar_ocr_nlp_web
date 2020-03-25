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

export function marking(answer, problem) {
    return request({
        url: '/reason/marking',
        method: 'get',
        params: {
            answer: answer,
            problem: problem
        }
    })
}