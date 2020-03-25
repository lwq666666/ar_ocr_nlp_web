import request from '@/utils/request'

export function getRules(sceneId,pageNumber,pageSize,operation,orderType,isAsc) {
    return request({
        url: '/rule/ruleList',
        method: 'get',
        params: {
            sceneId: sceneId,
            pageNumber: pageNumber,
            pageSize: pageSize,
            operation: operation,
            orderType: orderType,
            isAsc: isAsc
        }
    })
}

export function addShiedRule() {
    return request({
        url: '/rule/shieldRule',
        method: 'post',
        params: {
            sceneId: sceneId,
            itemId: itemId,
        }
    })
}

export function addPriorityRule(sceneId,itemId) {
    return request({
        url: '/rule/priorityRule',
        method: 'post',
        params: {
            sceneId: sceneId,
            itemId: itemId,
        }
    })
}

export function updatePriorityScore(id,priorityWeight) {
    return request({
        url: '/rule/priorityRule',
        method: 'put',
        params: {
            id: id,
            priorityWeight: priorityWeight,
        }
    })
}

export function deleteShiedRule(id,sceneId) {
    return request({
        url: '/rule/shieldRule',
        method: 'delete',
        params: {
            id: id,
            sceneId: sceneId,
        }
    })
}

export function deletePriorityRule(id,sceneId) {
    return request({
        url: '/rule/priorityRule',
        method: 'delete',
        params: {
            id: id,
            sceneId: sceneId,
        }
    })
}