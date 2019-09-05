<template>
<el-container style="min-height: 100vh;" class="bg4">
    <el-main>
        <el-alert title="请选择 栏目-场景" type="info" :closable="false" style="margin-bottom: 20px;background-color:white;" show-icon></el-alert>
        <el-row>
            <el-col :span="colform.father">
                <el-row :gutter="20">
                    <transition-group name="flip-list">
                        <el-col :span="colform.children_left" v-for="bcase in cases" :key="bcase.id">
                            <div @click="haddleClick(bcase)" style="cursor:pointer;">
                                <el-card :class="{'box-card2':true,'card-selected':selected(bcase.id)}" shadow="hover">
                                    <div slot="header" class="clearfix">
                                        <div style="text-align:center;font-size:20px">{{bcase.columnName}}</div>
                                    </div>
                                    <div v-for="scene in bcase.scenes" :key="scene.id" class="text item" style="text-align: left;font-size: 14px;height:20px;">
                                        <el-button style="padding:9px" @click.stop="handerClickScene(scene)">{{scene.sceneName}}</el-button>
                                    </div>
                                </el-card>
                            </div>
                        </el-col>
                    </transition-group>
                </el-row>
            </el-col>
            <transition name="slide-fade" mode="in-out">
                <el-col :span="colform.children_right" v-if="open">
                    <Dashboard :open="open" :columnId="columnId"></Dashboard>
                </el-col>
            </transition>
        </el-row>
    </el-main>
</el-container>
</template>

<script>
import Dashboard from "@/views/dashboard/index";
import {
    getColumn
} from "@/api/column.js";

export default {
    name: "index",
    components: {
        Dashboard: Dashboard,
    },
    data() {
        return {
            length: 7,
            cases: [],
            tt: [],
            dialogFormVisible: false,
            form: {
                name: ""
            },
            open: false,
            columnId: "1",
            colform: {
                father: 24,
                children_left: 6,
                children_right: 0
            },
            selectColumn: ""
        };
    },
    mounted: function () {
        getColumn()
            .then(response => {
                this.cases = response.data;
                this.length = this.cases.length;
            })
            .catch(function () {});
    },
    methods: {
        haddleClick(bcase) {
            if (this.open == false || this.selectColumn != bcase.id) {
                this.selectColumn = bcase.id;
                this.open = true;
                this.haddleClickmin();
                this.columnId = bcase.columnStrId;
            } else if (this.open == true && this.selectColumn == bcase.id) {
                this.haddleClickmax();
                this.selectColumn = "";
            }
        },
        haddleClickmin() {
            this.colform.father = 6;
            this.colform.children_left = 24;
            this.colform.children_right = 18;
        },
        haddleClickmax() {
            this.colform.father = 24;
            this.colform.children_left = 6;
            this.colform.children_right = 0;
            this.open = false;
        },
        handerClickScene(scene) {
            const roles = this.$store.getters.roles;
            if (roles.includes('admin') || roles.includes('root')) {
                this.$router.push({
                    name: "rules",
                    params: {
                        id: scene.id
                    },
                    query: {
                        caseName: scene.sceneName,
                        caseType: scene.type
                    }
                });
            }
        },
        selected(id) {
            if (id == this.selectColumn) return true;
            else return false;
        }
    }
};
</script>

<style scoped>
.box-card2 {
    width: 90%;
    background-color: white;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 30px;
    margin-top: 10px;
}

.card-selected {
    border: 3px solid red;
}

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

.bg4 {
    background-size: contain;
    background-color: rgb(231, 232, 236) ;
}

.flip-list-move {
    transition: transform 1s;
}

.flip-list1-move {
    transition: transform 1s;
}

.slide-fade-enter-active {
    transition: all 1s ease;
}

/* .slide-fade-leave-active {
    transition: all 2s cubic-bezier(1.0, 0.5, 0.8, 1.0);
} */

.slide-fade-enter,
.slide-fade-leave-to {
    transform: transateX(10px);
    opacity: 0;
}
</style>
