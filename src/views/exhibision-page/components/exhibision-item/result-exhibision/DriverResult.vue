<template>
<div style="text-align:center">
    <el-card class="box-card" v-for="i in result" :key="i">
        <div class="clearfix">
            <span>{{i}}</span>
        </div>
    </el-card>
    <el-button @click="back()">返回上一页</el-button>
</div>
</template>

<script>
import {
    getRecommendList
} from "@/api/recommend"

export default {
    data() {
        return {
            caseId: this.$route.params.id,
            uid: this.$route.query.uid,
            result: []
        };
    },
    methods: {
        back() {
            this.$router.push({
                name: "DriverList",
                query: {
                    uid: this.$route.query.uid
                }
            });
        }
    },
    mounted: function () {
        getRecommendList(caseId, uid, 10)
            .then(response => {
                this.result = response.data.data;
            })
            .catch(function () {});
    }
};
</script>
