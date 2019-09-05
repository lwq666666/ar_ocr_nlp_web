import { logout, getUserInfo } from '@/api/permission'

const user = {
  state: {
    roles: []
  },

  mutations: {
    SET_ROLES: (state, roles) => {
      state.roles = roles
    }
  },

  actions: {
    // 获取用户信息
    GetUserInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getUserInfo().then(response => {
          const data = response.data;
          if (data.roles && data.roles.length > 0) { // 验证返回的roles是否是一个非空数组
            commit('SET_ROLES', data.roles)
          } else {
            reject('getInfo: roles must be a non-null array !')
          }
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit, state }) {
      return new Promise((resolve, reject) => {
        logout().then(() => {
          commit('SET_ROLES', []);
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
  }
}

export default user
