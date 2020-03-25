<template>
<div>
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
        }
    },
    created: function () {
        getColumn()
            .then(response => {
                this.cases = response.data;
            })
            .catch(function () {});
    },
    methods: {
        handerClickScene(scene) {
            this.$router.push({
                name: 'InlineResult',
                params: {
                    id: scene.id
                }
            });
        }
    }
}
</script>
