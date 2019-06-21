import request from '@/utils/request'

export function getRecommendList(sceneStrId,userId,number) {
    return request({
        url: '/recommendTest',
        method: 'get',
        params: {
            sceneStrId: sceneStrId,
            userId: userId,
            number: number
        }
    })
}