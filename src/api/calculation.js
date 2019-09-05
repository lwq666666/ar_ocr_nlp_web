import request from '@/utils/request'

export function getEvaluation(sceneId) {
    return request({
        url: '/evaluation/getEvaluation',
        method: 'get',
        params: {
            sceneId: sceneId,
        }
    })
}

export function getItemData(sceneId) {
    return request({
        url: '/evaluation/evaluationItemData',
        method: 'get',
        params: {
            sceneId: sceneId,
        }
    })
}

export function getRankList(sceneId, number) {
    return request({
        url: '/evaluation/getRankList',
        method: 'get',
        params: {
            sceneId: sceneId,
            number: number
        }
    })
}

export function getAllUsersCount(sceneId, number) {
    return request({
        url: '/evaluation/usersCount',
        method: 'get',
    })
}