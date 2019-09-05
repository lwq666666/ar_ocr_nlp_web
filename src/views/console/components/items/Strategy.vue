<template>
<div style="text-align: center">
    <el-alert title="" type="success" style="margin-bottom: 50px" :closable="false" show-icon>
        {{caseName}}/管理配置/策略配置
    </el-alert>
    <el-transfer v-model="value1" :data="data" :titles="['未启用策略', '当前场景策略']" style="text-align: left; display: inline-block">
    </el-transfer>
    <div style="margin-top: 50px">
        <el-button type="primary" plain :loading="buttonLoading" @click="editStrategy(value1)">确认</el-button>
    </div>
</div>
</template>

<script>
import {
    getAllStrategiesAndIsConf
} from "@/api/strategy";
export default {
    name: "Strategy",
    data() {
        return {
            caseName: this.$route.query.caseName,
            caseId: this.$route.params.id,
            data: [],
            value1: [],
            buttonLoading: false
        };
    },
    created() {
        this.initStrategyList();
    },
    methods: {
        initStrategyList() {
            this.data = [];
            getAllStrategiesAndIsConf(this.$route.params.id).then(response => {
                console.log("策略信息" + response.data.configStrategyDtoList[0].strategyName);
                const strategies = response.data.strategyDtoList;
                const length = strategies.length;
                const configStrategies = response.data.configStrategyDtoList;
                const length1 = configStrategies.length;
                let defaultStrategyId;
                let failStrategyArray = new Array();
                for (let j = 0; j < length1; j++) {
                    if (configStrategies[j].defaultStrategy) {
                        defaultStrategyId = configStrategies[j].id;
                    }
                    //配置失败的strategy
                    if (configStrategies[j].configStatus.match("失败")) {
                        failStrategyArray.push(configStrategies[j].id);
                    }
                }
                console.log("failStrategyArray:" + failStrategyArray);
                for (let i = 0; i < length; i++) {
                    //从失败strategy数组中查找是否有当前strategyId，如果有，修改strategyName为+"失败"
                    if (failStrategyArray.indexOf(strategies[i].id) != (-1)) {
                        console.log("找到失败");
                        strategies[i].strategyName += "(失败)";
                    }
                    if (strategies[i].id === defaultStrategyId) {
                        strategies[i].strategyName += "(默认)";
                    }
                    this.data.push({
                        key: strategies[i].id,
                        label: strategies[i].strategyName,
                        disabled: strategies[i].id === defaultStrategyId
                    });
                }
                for (let j = 0; j < length1; j++) {
                    this.value1.push(configStrategies[j].id)
                }
            }).catch(function (error) {

            });
        },
        editStrategy(value1) {
            console.log(this);
            this.buttonLoading = true;
            var valueString = "";
            value1.forEach(element => {
                console.log(element);
                valueString += (element + ',');
            });
            console.log(valueString.substr(0, valueString.length - 1));
            addStrategyList(valueString.substr(0, valueString.length - 1)).then(response => {
                this.buttonLoading = false;
                this.successNotify("策略配置成功");
                this.initStrategyList();
            }).catch(error => {
                this.buttonLoading = false;
                console.log(error.response);
                this.errorNotify(error.response.data);
                this.initStrategyList();
            });
        },
        errorNotify(message) {
            this.$notify.error({
                title: '错误',
                message: message
            });
        },
        successNotify(message) {
            this.$notify.success({
                title: '成功',
                message: message
            });
        }
    }
}
</script>

<style scoped>
div.el-transfer-panel {
    width: 330px !important;
}
</style>
