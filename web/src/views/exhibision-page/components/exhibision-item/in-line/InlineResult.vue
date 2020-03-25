<template>
<div>
    <el-row>
        <el-card class="box-card">
            <my-linecharts :style="{height:'200px',width:'300px'}" :chartType="1" :chartData="chartData"></my-linecharts>
        </el-card>
        <el-card class="box-card">
            <my-linecharts :style="{height:'200px',width:'300px'}" :chartType="2" :chartData="chartData"></my-linecharts>
        </el-card>
        <el-card class="box-card">
            <my-linecharts :style="{height:'200px',width:'300px'}" :chartType="3" :chartData="chartData"></my-linecharts>
        </el-card>
        <el-card class="box-card">
            <my-linecharts :style="{height:'200px',width:'300px'}" :chartType="4" :chartData="chartData"></my-linecharts>
        </el-card>
    </el-row>
</div>
</template>

<script>
import Echarts from '@/components/echarts/Linechart.vue'
export default {
    name: "InlineResult",
    components: {
        'my-linecharts': Echarts,
    },
    data() {
        return {
            chartData: {}
        }
    },
    created() {
        this.getData();
    },
    methods: {
        getData() {
            this.$ajax({
                method: 'get',
                url: 'evaluation/getEvaluation',
                params: {
                    sceneId: this.$route.params.id,
                }
            }).then((res) => {
                this.chartData = res.data.eid_dict;
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
