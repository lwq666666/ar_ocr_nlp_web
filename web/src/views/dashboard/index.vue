<template>
    <div class="dashboard-editor-container" style="margin-top: -20px">
        <panel-group :selOptions="selOptions"
                     :showList="showList" :totleData="totleData"
                     @handleSetLineChartData="handleSetLineChartData"
                     @getEval="getEval"/>
        <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
            <line-chart :type="this.type" :chart-data="lineChartData"/>
        </el-row>

        <el-row :gutter="32">
            <el-col v-if="this.showList[4]" :span="8">
                <div class="chart-wrapper">
                    <raddar-chart/>
                </div>
            </el-col>
            <el-col v-if="this.showList[5]" :span="8">
                <div class="chart-wrapper">
                    <pie-chart/>
                </div>
            </el-col>
            <el-col v-if="this.showList[6]" :span="8">
                <div class="chart-wrapper">
                    <bar-chart/>
                </div>
            </el-col>
        </el-row>

        <el-row :gutter="8">
            <el-col v-if="this.showList[7]" :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}"
                    :lg="{span: 12}" :xl="{span: 12}"
                    style="padding-right:8px;margin-bottom:30px;">
                <transaction-table :columnId="this.columnId"/>
            </el-col>
            <!--<el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">-->
            <!--<todo-list />-->
            <!--</el-col>-->
            <!--<el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}"-->
            <!--style="margin-bottom:30px;">-->
            <!--<box-card/>-->
            <!--</el-col>-->
        </el-row>
    </div>
</template>

<script>
    import {
        mapGetters
    } from 'vuex'
    import PanelGroup from './components/PanelGroup'
    import LineChart from './components/LineChart'
    import RaddarChart from './components/RaddarChart'
    import PieChart from './components/PieChart'
    import BarChart from './components/BarChart'
    import TransactionTable from './components/TransactionTable'
    //    import BoxCard from './components/BoxCard'

    const lineChartData = {
        activeVisitis: {
            expectedData: [],
            actualData: [],
            xData: [],
        },
        watchDuration: {
            expectedData: [],
            actualData: [],
            xData: [],
        },
        oderCount: {
            expectedData: [],
            actualData: [],
            xData: [],
        }
    }

    export default {
        name: "Dashboard",
        components: {
            PanelGroup,
            LineChart,
            RaddarChart,
            PieChart,
            BarChart,
            TransactionTable,
            // BoxCard
        },
        data() {
            return {
                lineChartData: lineChartData.activeVisitis,
                totleData: [0, 0, 0],
                showList: [0, 0, 0, 0, 0, 0, 0, 0],
                type: 'line',
                selOptions: [],
            };
        },
        props: ['open', 'columnId'],
        created() {
            this.getEval("", 1);
            this.getArea();
        },
        watch: {
            columnId: function () {
                this.getEval("", 1);
                this.getArea();
            }
        },
        methods: {
            handleSetLineChartData(type) {
                this.lineChartData = lineChartData[type];
            },
            getArea() {
                this.$ajax({
                    method: "get",
                    url: "/area/all",
                }).then(res => {
                    let data = res.data.data;
                    this.selOptions = [];
                    let first = new Object;
                    first.id = "";
                    first.code = null;
                    first.name = "所有区域";
                    this.selOptions = data;
                    this.selOptions.unshift(first);
                }).catch(() => {
                });
            },
            getEval(areaCode, type) {
                let cid = this.columnId;
                this.$ajax({
                    method: "get",
                    url: "/evaluation",
                    params: {
                        collumnId: cid,
                        areaCode: areaCode
                    }
                }).then(res => {
                    let data = res.data.data;
                    if (type === 1) {
                        this.fillData(data);
                    } else if (type === 2) {
                        this.fillCompareData(data);
                    }
                }).catch(() => {
                });
            },
            fillData(data) {
                this.showList = data.showList;
                for (let i = 0; i < 3; i++) {
                    if (this.showList[i] === 1) {
                        switch (i) {
                            case 0:
                                this.lineChartData = lineChartData.activeVisitis;
                                break;
                            case 1:
                                this.lineChartData = lineChartData.watchDuration;
                                break;
                            case 2:
                                this.lineChartData = lineChartData.oderCount;
                                break;
                            default:
                                break;
                        }
                        break;
                    }
                }
                lineChartData.activeVisitis.actualData = JSON.parse(data.auc).yData;
                lineChartData.activeVisitis.xData = JSON.parse(data.auc).xData;
                this.totleData.splice(0, 1, JSON.parse(data.auc).totle);
                lineChartData.watchDuration.actualData = JSON.parse(data.awd).yData;
                lineChartData.watchDuration.xData = JSON.parse(data.awd).xData;
                this.totleData.splice(1, 1, JSON.parse(data.awd).totle);
            },
            fillCompareData(data) {
                //活跃用户
                let acXData = lineChartData.activeVisitis.xData;
                let exYData = JSON.parse(data.auc).yData;
                let conXData = JSON.parse(data.auc).xData;
                let resYData = [];
                for (let i = 0; i < acXData.length; i++) {
                    let flag = 0;
                    for (let j = 0; j < conXData.length; j++) {
                        if (conXData[j] === acXData[i]) {
                            resYData[i] = exYData[j];
                            flag = 1;
                            break;
                        }
                    }
                    if (flag === 0) {
                        resYData[i] = 0;
                    }
                }
                lineChartData.activeVisitis.expectedData = resYData;


                //观看时长
                acXData = lineChartData.watchDuration.xData;
                exYData = JSON.parse(data.awd).yData;
                conXData = JSON.parse(data.awd).xData;
                resYData = [];
                for (let i = 0; i < acXData.length; i++) {
                    let flag = 0;
                    for (let j = 0; j < conXData.length; j++) {
                        if (conXData[j] === acXData[i]) {
                            resYData[i] = exYData[j];
                            flag = 1;
                            break;
                        }
                    }
                    if (flag === 0) {
                        resYData[i] = 0;
                    }
                }
                lineChartData.watchDuration.expectedData = resYData;
            },

        }
    };
</script>

<style lang="scss" scoped>
    .dashboard-editor-container {
        padding: 32px;
        background-color: rgb(231, 232, 236);

        .chart-wrapper {
            background: #fff;
            padding: 16px 16px 0;
            margin-bottom: 32px;
        }
    }
</style>
