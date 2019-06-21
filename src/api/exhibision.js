import request from '@/utils/request'


export function getActionData() {
    return request({
        url: '/exhibision/actionData',
        method: 'get'
    })
}


export function getItemData() {
    return request({
        url: '/exhibision/itemData',
        method: 'get'
    })
}


export function getItemName(item_id) {
    return request({
        url: '/exhibision/itemName',
        method: 'get',
        params: {

            item_id: item_id
        }
    })
}