<template>
<div>
    <el-alert title="" type="success" style="margin-bottom: 50px" :closable="false" show-icon>
        {{caseName}}/管理配置/统计分析/指标
    </el-alert>
    <el-row :gutter="20">
        <el-col :span="6">
            <el-tag>物料数量：{{itemsCount}}</el-tag>
        </el-col>
        <el-col :span="10">
            <el-tag type="success">当前使用策略：{{currentStrategy}}</el-tag>
        </el-col>
        <el-col :span="6">
            <el-tag type="warning">总用户数：{{usersCount}}</el-tag>
        </el-col>
    </el-row>
    <el-row style="margin-top: 100px">
        <el-col :span="24">
            <div>
                <my-linecharts :chartType="1" :chartData="chartData" style="margin-left: 50px"></my-linecharts>
                <my-linecharts :chartType="2" :chartData="chartData" style="margin-left: 50px"></my-linecharts>
            </div>
            <div>
                <my-linecharts :chartType="3" :chartData="chartData" style="margin-left: 50px"></my-linecharts>
                <my-linecharts :chartType="4" :chartData="chartData" style="margin-left: 50px"></my-linecharts>
            </div>
        </el-col>
    </el-row>
</div>
</template>

<script>
import Echarts from '@/components/echarts/Linechart.vue'
import {
    getEvaluation,
    getItemData,
    getRankList,
    getAllUsersCount
} from "@/api/calculation";
export default {
    name: "Calculation",
    components: {
        'my-linecharts': Echarts,
    },
    data() {
        return {
            caseName: this.$route.query.caseName,
            itemsCount: 0,
            usersCount: 0,
            currentAlgorithm: "",
            chartData: {}
        }
    },
    created() {
        this.getLineChartData();
        window.setInterval(this.getLineChartData, 15000);
        this.getUsersCount();
        this.getItemsCount();
    },
    mounted() {

    },
    methods: {
        getItemsCount() {
            getItemData(this.$route.params.id).then((res) => {
                this.itemsCount = res.data.data;
            }).catch(function () {});
        },
        getUsersCount() {
            getAllUsersCount().then((res) => {
                this.usersCount = res.data.data;
            }).catch(function () {});
        },
        getLineChartData() {
            getEvaluation(this.$route.params.id).then((res) => {
                this.chartData = res.data.data.eid_dict;
                this.currentStrategy = res.data.data.currentStrategy;
            }).catch(function () {});
        }
    }
}
</script>

<style scoped>
.el-tag {
    font-size: 18px !important;
}
</style>
