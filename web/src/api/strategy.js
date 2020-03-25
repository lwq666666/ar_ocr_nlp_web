import request from '@/utils/request'

export function getAllStrategiesAndIsConf(sceneId) {
    return request({
        url: '/strategy/getAllStrategiesAndIsConf',
        method: 'get',
        params: {
            sceneId: sceneId,
        }
    })
}

export function addStrategyList(sceneId, value) {
    return request({
        url: '/strategy/config',
        method: 'post',
        params: {
            sceneId: sceneId,
            value: value
        }
    })
}

export function addStrategy(sceneId, strategyId, isDefault) {
    return request({
        url: '/strategy/addStrategy',
        method: 'post',
        params: {
            sceneId: sceneId,
            strategyId: strategyId,
            isDefault: isDefault
        }
    })
}

export function getFlowByScene(sceneId) {
    return request({
        url: '/strategy/strategyandflow',
        method: 'get',
        params: {
            sceneId: sceneId,
        }
    })
}