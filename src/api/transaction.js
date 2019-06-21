import request from '@/utils/request'

export function fetchList(query) {
  return request({
    url: '/evaluation/watch_duration_rank',
    method: 'get',
    params: query
  })
}
