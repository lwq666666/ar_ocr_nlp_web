
import calculation from "@/views/console/components/items/Calculation"
import api from "@/views/console/components/items/API"
import rule from "@/views/console/components/items/Rule"
import strategy from "@/views/console/components/items/Strategy"
import flow from "@/views/console/components/items/Flow"
import Rank from "@/views/console/components/items/Rank"

const sceneRouter = {
    path: '/scene',
    name: 'scene',
    component: () => import('@/views/console/components/ThirdPageMain'),
    children: [
        {
            path: '/case/:id/strategy',
            name: 'strategy',
            component: strategy,
            meta: {
                roles: ['root']
            }
        },
        {
            path: '/case/:id/flow',
            name: 'flow',
            component: flow,
            meta: {
                roles: ['root']
            }
        }, {
            path: '/case/:id/calculation',
            name: 'calculation',
            component: calculation,
            meta: {
                roles: ['root']
            }
        }, {
            path: '/case/:id/api',
            name: 'api',
            component: api,
            meta: {
                roles: ['root']
            }
        }, {
            path: '/case/:id/rules',
            name: 'rules',
            component: rule,
            meta: {
                roles: ['admin']
            }
        }, {
            path: '/case/:id/rank',
            name: 'rank',
            component: Rank,
            meta: {
                roles: ['root']
            }
        }
    ]
}

export default sceneRouter;