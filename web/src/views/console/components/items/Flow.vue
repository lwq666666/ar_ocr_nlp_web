<template>
<div>
    <el-alert title="" type="success" style="margin-bottom: 20px" :closable="false" show-icon>
        {{caseName}}/管理配置/策略流
    </el-alert>
    <el-collapse v-model="activeNames" @change="handleChange" v-for="i in tableData" :key="i">
        <el-collapse-item>
            <template slot="title">
                <div v-if="i.configStatus=='已配置'">{{i.strategyName}}</div>
                <div v-else class="line">{{i.strategyName}}</div>
            </template>
            <div v-if="!(i.configStatus=='已配置')">
                <el-button type="primary" @click="start(i.id,i.defaultStrategy)" style="margin:30px;">启用策略</el-button>
            </div>
            <el-table v-if="i.configStatus=='已配置'" :header-cell-style="{background:'#fafafa'}" :data="i.flows" height="100%" border style="width: 100%">
                <el-table-column prop="createTime" label="创建时间" :formatter="formatCreateTime">
                </el-table-column>
                <el-table-column prop="operationCycle" label="操作周期" :formatter="formatOperationCycle">
                </el-table-column>
                <el-table-column prop="flowStatus" label="状态">
                </el-table-column>
            </el-table>
        </el-collapse-item>
    </el-collapse>
</div>
</template>

<script>
const Operation = {
    INIT: 0
};
export default {
    name: "Flow",
    data() {
        return {
            activeName: "flowModel",
            caseName: this.$route.query.caseName,
            caseId: this.$route.params.id,
            tableData: []
        };
    },
    created() {
        getFlowByScene(this.caseId).then(res => {
            this.tableData = res.data;
        });
    },
    methods: {
        start: function (strategyId, defaultStrategy) {
            addStrategy(this.caseId, strategyId, defaultStrategy).then(res => {
                alert(res);
            });
        },
        formatCreateTime: function (row) {
            let date = new Date(parseInt(row.createTime));
            let Y = date.getFullYear() + '-';
            let M = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) + '-' : date.getMonth() + 1 + '-';
            let D = date.getDate() < 10 ? '0' + date.getDate() + ' ' : date.getDate() + ' ';
            let h = date.getHours() < 10 ? '0' + date.getHours() + ':' : date.getHours() + ':';
            let m = date.getMinutes() < 10 ? '0' + date.getMinutes() + ':' : date.getMinutes() + ':';
            let s = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds();
            return Y + M + D + h + m + s;
        },
        formatOperationCycle: function (row) {
            return Math.round(row.operationCycle / 60, 2) + "分钟";
        }
    }
};
</script>

<style scoped>
.line {
    text-decoration: line-through
}
</style>
