<template>
<div>
    <el-card shadow="hover" class="box-card">
        <div slot="header" class="clearfix">
            <span>行为数据</span>
        </div>
        <el-form :inline="true">
            <el-form-item label="过滤后">
                <el-input v-model="form.actionCount" :readonly="true"></el-input>
            </el-form-item>
            <el-form-item label="过滤前">
                <el-input v-model="form.actionCountBefore" :readonly="true"></el-input>
            </el-form-item>
        </el-form>
        <el-progress type="circle" :percentage="actionPresent" :sshow-text="true"></el-progress>
    </el-card>
    <el-card shadow="hover" class="box-card">
        <div slot="header" class="clearfix">
            <span>物料数据</span>
        </div>
        <el-form :inline="true">
            <el-form-item label="黔新闻">
                <el-input v-model="form.qxw_item" :readonly="true"></el-input>
            </el-form-item>
            <el-form-item label="热播追看">
                <el-input v-model="form.hot_item" :readonly="true"></el-input>
            </el-form-item>
            <el-form-item label="电视院线">
                <el-input v-model="form.tv_item" :readonly="true"></el-input>
            </el-form-item>
        </el-form>
    </el-card>
</div>
</template>

<script>
import {
    getActionData,
    getItemData
} from "@/api/exhibision"

export default {
    data() {
        return {
            form: {
                actionCount: null,
                actionCountBefore: null,
                qxw_item: null,
                hot_item: null,
                tv_item: null
            }
        };
    },
    computed: {
        actionPresent: function () {
            return (
                (this.form.actionCount / this.form.actionCountBefore) *
                100
            ).toFixed(2);
        }
    },
    mounted: function () {
        getActionData()
            .then(response => {
                this.form.actionCount = response.data.actionDataAfter;
                this.form.actionCountBefore = response.data.actionDataBefore;
            })
            .catch(function () {});
        getItemData()
            .then(response => {
                this.form.qxw_item = response.data.qxw_item;
                this.form.hot_item = response.data.hot_item;
                this.form.tv_item = response.data.tv_item;
            })
            .catch(function () {});
    }
};
</script>

<style scoped>
.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}

.clearfix:after {
    clear: both;
}

.box-card {
    width: 400px;
    margin: 20px;
    box-shadow: #888888 0px 0px 5px 6px;
}
</style>
