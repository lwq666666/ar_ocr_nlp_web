<template>
<div>
    <div class="block">
        <el-carousel height="220px">
            <el-carousel-item>
                <img src="@/image/post1.jpg" width="110%">
        </el-carousel-item>
                <el-carousel-item>
                    <img src="@/image/post2.jpg" width="100%">
        </el-carousel-item>
                    <el-carousel-item>
                        <img src="@/image/post3.jpeg" width="100%">
        </el-carousel-item>
                        <el-carousel-item>
                            <img src="@/image/post4.jpg" width="100%">
        </el-carousel-item>
        </el-carousel>
    </div>
    <el-row>
        <el-col :span="24" v-for="bcase in cases" :key="bcase.id">
            <div>
                <el-card class="box-card2" shadow="hover">
                    <div slot="header" class="clearfix">
                        <div style="text-align:center;font-size:20px">{{bcase.columnName}}</div>
                    </div>
                    <div v-for="scene in bcase.scenes" :key="scene.id" class="text item">
                        <el-button style="margin:3px;cursor:pointer;" @click="handerClickScene(scene)">{{scene.sceneName}}</el-button>
                    </div>
                </el-card>
            </div>
        </el-col>
    </el-row>
    <div style="text-align:center;margin-top:40px;">
        <el-button center="true" @click="back()">返回首页</el-button>
    </div>
</div>
</template>

<script>
import {
    getColumn
} from "@/api/column";

export default {
    data() {
        return {
            cases: []
        };
    },
    mounted: function () {
        getColumn()
            .then(response => {
                this.cases = response.data;
            })
            .catch(function () {});
    },
    methods: {
        handerClickScene(scene) {
            this.$router.push({
                name: "DriverResult",
                params: {
                    id: scene.sceneStrId
                },
                query: {
                    uid: this.$route.query.uid
                }
            });
        },
        back() {
            this.$router.push({
                name: "DriverLogin"
            });
        }
    }
};
</script>

<style>
.box-card2 {
    width: 90%;
    background-color: white;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 30px;
    margin-top: 10px;
}
</style>
