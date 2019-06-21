import request from '@/utils/request'

export function showPageListTest() {
    return request({
        url: '/exhibision/actionData',
        method: 'get'
    })
}

export function getSceneBySceneId(sceneId) {
    return request({
        url: '/scene/getSceneBySceneId',
        method: 'get',
        params: {
            sceneId: sceneId,
        }
    })
}

