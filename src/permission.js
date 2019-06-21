import router from './router'
import store from './store'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css'// progress bar style

NProgress.configure({ showSpinner: false })// NProgress Configuration

router.beforeEach((to, from, next) => {
    NProgress.start();
    if (to.path === '/login') {
        if (store.getters.roles.length === 0) {
            next()
            NProgress.done() // if current page is dashboard will not trigger	afterEach hook, so manually handle it
        }
        else {
            next({ path: '/front-page' })
            NProgress.done()
        }
    } else {
        if (store.getters.roles.length === 0) {
            store.dispatch("GetUserInfo").then((res) => {
                const roles = res.data.roles // note: roles must be a array! such as: ['editor','develop']
                store.dispatch('GenerateRoutes', { roles }).then(() => { // 根据roles权限生成可访问的路由表
                    router.addRoutes(store.getters.addRouters) // 动态添加可访问路由表
                    next({ ...to, replace: true })
                })
            }).catch((err) => {
                // store.dispatch('FedLogOut').then(() => {
                //     Message.error(err || 'Verification failed, please login again')
                //     next({ path: '/' })
                // })
            })
        }
        else {
            next()
        }
    }
})

router.afterEach(() => {
    NProgress.done() // finish progress bar
})