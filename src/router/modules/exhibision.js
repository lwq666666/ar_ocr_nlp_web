import Driver from '@/views/exhibision-page/components/exhibision-item/result-exhibision/Driver'
import DriverList from '@/views/exhibision-page/components/exhibision-item/result-exhibision/DriverList'
import DriverResult from '@/views/exhibision-page/components/exhibision-item/result-exhibision/DriverResult'
import DriverLogin from '@/views/exhibision-page/components/exhibision-item/result-exhibision/DriverLogin'
import ModelTraining from '@/views/exhibision-page/components/exhibision-item/offline/ModelTraining'
import row from '@/views/exhibision-page/components/exhibision-item/offline/row'
import Home from '@/views/exhibision-page/components/exhibision-item/Home'
import Inline from '@/views/exhibision-page/components/exhibision-item/in-line/Inline'
import InlineDriver from '@/views/exhibision-page/components/exhibision-item/in-line/InlineDriver'
import InlineResult from '@/views/exhibision-page/components/exhibision-item/in-line/InlineResult'
import DataCleaning from '@/views/exhibision-page/components/exhibision-item/data-cleaning/DataCleaning'

const exhibisionRouter = {
    path: '/exhibision-page',
    name: 'exhibision',
    component: () => import('@/views/exhibision-page/index'),
    children: [
        {
            path: 'G1',
            components: {
                default: DataCleaning,
            }
        },
        {
            path: 'G2',
            components: {
                default: row,
                bottom: ModelTraining
            }
        },
        {
            path: 'G3',
            component: InlineDriver,
            redirect: { name: 'InlineList' },
            children: [
                {
                    path: '/',
                    name: 'InlineList',
                    component: Inline
                }, {
                    path: '1',
                    name: 'InlineResult',
                    component: InlineResult
                },
            ]
        },
        {
            path: 'P9',
            redirect: 'G4'
        },
        {
            path: 'G4',
            component: Driver,
            redirect: { name: 'DriverLogin' },
            children: [
                {
                    path: '/',
                    name: 'DriverLogin',
                    component: DriverLogin
                },
                {
                    path: '/1',
                    name: 'DriverList',
                    component: DriverList
                },
                {
                    path: '/2',
                    name: 'DriverResult',
                    component: DriverResult
                }
            ]
        },
        {
            path: '*',
            component: Home
        },
    ]
}

export default exhibisionRouter
