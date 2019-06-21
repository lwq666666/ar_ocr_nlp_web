<template>
    <div :class="className" :id="id" :style="{height:'300px',width:'500px',display:'inline-block'}" ref="myEchart">
    </div>
</template>
<script>
    export default {
        props: {
            className: {
                type: String,
                default: 'yourClassName'
            },
            id: {
                type: String,
                default: 'yourID'
            },
            width: {
                type: String,
                default: '500px'
            },
            height: {
                type: String,
                default: '500px'
            },
            chartType: {
                type: String,
                default: 1
            },
            chartData: {
                type: String,
                default: {}
            }
        },
        data() {
            return {
                chart: null,
                xList: [],
                yList: [],
            }
        },
        created() {
        },
        mounted() {
            this.initChart();
        },
        beforeDestroy() {
            if (!this.chart) {
                return
            }
            this.chart.dispose();
            this.chart = null;
        },
        watch: {
            chartData: 'initChartData'
        },
        methods: {
//      refreshChart(){
//        window.setInterval(this.initChart,6000)
//        console.log("刷新了")
//        console.log(new Date())
//      },
            initChart() {
                this.chart = this.$echarts.init(this.$refs.myEchart);
                // 把配置和数据放这里
                let title = ""
                switch (this.chartType) {
                    case 1 :
                        title = "准确率";
                        break;
                    case 2 :
                        title = "召回率";
                        break;
                    case 3 :
                        title = "新颖率";
                        break;
                    case 4 :
                        title = "覆盖率";
                        break;
                }
                this.chart.setOption({
                    title: {
                        text: title,
                        target: 'blank',//主标题超链接打开方式
                        textStyle: { //设置主标题风格
                            Color: 'green',//设置主标题字体颜色
                            fontStyle: '',//主标题文字风格
                        },
                        left: 'center'
                    },
                    color: ['#3398DB'],
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: { // 坐标轴指示器，坐标轴触发有效
                            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: [{
                        type: 'category',
                        data: this.xList,
                        axisTick: {
                            alignWithLabel: true
                        }
                    }],
                    yAxis: [{
                        type: 'value',
                    }],
                    series: [{
                        name: '直接访问',
                        type: 'line',
                        barWidth: '60%',
                        data: this.yList
                    }]
                })
            },
            initChartData() {
                this.xList = [];
                this.yList = [];
                let cdata = this.chartData[this.chartType];
                console.log(cdata);
                for (let x in cdata) {
                    this.xList.push(x);
                    this.yList.push(cdata[x]);
                }
//        for(let i=0;i<cdata.length;i++){
//          console.log(cdata[i]);
////            for(let xkey in cdata[i]){
////              console.log(xkey);
////              this.xList.push(xkey);
////              this.yList.push(cdata[i][xkey]);
////            }
//        }
                this.initChart();
                console.log("显示变了哦");
            },
        }

    }
</script>
