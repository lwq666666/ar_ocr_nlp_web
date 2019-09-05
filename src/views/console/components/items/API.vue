<template>
<div>
    <el-alert title="" type="success" style="margin-bottom: 20px" :closable="false" show-icon>
        {{caseName}}/管理配置/API测试
    </el-alert>
    <el-row :gutter="20">
        <el-col :span="12">
            <el-form ref="form" :model="form" label-width="80px" :rules="rules" style="width: 80%;">
                <el-form-item label="推荐API">
                    <el-input v-model="form.url" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="请求方法">
                    <el-input v-model="form.method" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="场景ID">
                    <el-input v-model="form.sceneId" disabled="true">
                        <template slot="prepend">sceneId</template>
                    </el-input>
                </el-form-item>
                <el-form-item label="用户ID">
                    <el-input placeholder="请输入用户ID" v-model="form.userId" clearable>
                        <template slot="prepend">userId</template>
                    </el-input>
                </el-form-item>
                <el-form-item label="推荐数目">
                    <el-input placeholder="请输入推荐数目" v-model="form.number" clearable>
                        <template slot="prepend">number</template>
                    </el-input>
                </el-form-item>
                <el-form-item style="float: left">
                    <el-button type="primary" @click="onSubmit">执行</el-button>
                </el-form-item>
            </el-form>
        </el-col>
        <el-col :span="12">
            <el-form ref="form" :model="form" label-width="80px" :rules="rules" style="width: 80%">
                <el-form-item label="推荐列表">
                    <el-table :data="form.result" max-height="600" border style="width: 100%">
                        <el-table-column prop="id" label="媒资Id" width="300">
                        </el-table-column>
                        <el-table-column prop="name" label="媒资名" min-width="50">
                        </el-table-column>
                    </el-table>
                </el-form-item>
            </el-form>
        </el-col>
    </el-row>
</div>
</template>

<script>
import {
    getSceneBySceneId
} from '@/api/scene'
import {
    getRecommendList
} from '@/api/recommend'
import {
    getItemName
} from "@/api/exhibision";
import Echarts from '@/components/echarts/Linechart'
export default {
    name: "API",
    components: {
        'my-linecharts': Echarts,
    },
    data() {
        return {
            caseName: this.$route.query.caseName,
            form: {
                url: '',
                method: '',
                params: '',
                result: '',
                sceneId: '',
            },
            rules: {
                method: []
            },
        }
    },
    created: function () {
        getSceneBySceneId(this.$route.params.id).then(response => {
            this.form.sceneId = response.data.sceneStrId;
        }).catch(() => {});
        this.form.url = this.GLOBAL.BASE_URL + "recommendTest",
            this.form.method = "GET"
    },
    methods: {
        onSubmit() {
            getRecommendList(this.form.sceneId, this.form.userId, this.form.number).then(response => {
                var itemName = "ceshi";
                let data = (response.data.data + '').split(',')
                var itemCount = data.length;
                this.form.result = new Array(itemCount);
                for (let d in data) {
                    //根据itemId获得itemName开始
                    getItemName(data[d]).then(res => {
                        itemName = res.data.data;
                        var single = {
                            id: data[d],
                            name: itemName
                        }
                        this.form.result.splice(d, 1, single);
                    }).catch(() => {});
                    //根据itemId获得itemName结束
                }
                for (let i = 0; i < itemCount; i++) {
                    console.info("数组第" + i + "项对象数据的id: " + this.form.result[i].id + ";name: " + this.form.result[i].name);
                }
            }).catch(() => {});
        }
    }
}
</script>

<style scoped>
.textarea>.el-textarea__inner {
    font-family: "Microsoft" !important;
    font-size: 24px !important;
}
</style>
