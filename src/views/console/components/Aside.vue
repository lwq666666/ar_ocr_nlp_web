<template>
<el-aside width="200px">
    <el-menu :default-active="$route.path" router class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" style="min-height: 100vh;border-right: 0px;height: 100%">
        <el-submenu index="1">
            <template slot="title">
                <i class="el-icon-message"></i>
                <span>管理配置</span>
            </template>
            <el-menu-item-group>
                <el-menu-item :index="'/case/'+caseId+'/rules'" :route="{name: 'rules', query:{caseName: caseName,caseType: caseType}}">规则配置</el-menu-item>
                <el-menu-item v-if="willShow&&permission" :index="'/case/'+caseId+'/'" :route="{name: 'strategy', query:{caseName: caseName,caseType: caseType}}">策略配置</el-menu-item>
                <el-menu-item v-if="willShow&&permission" :index="'/case/'+caseId+'/flow'" :route="{name: 'flow', query:{caseName: caseName,caseType: caseType}}">策略流</el-menu-item>
                <el-submenu v-if="permission" index="2-4">
                    <template v-if="permission" slot="title">统计分析</template>
                    <el-menu-item v-if="permission" :index="'/case/'+caseId+'/calculation'" :route="{name: 'calculation', query:{caseName: caseName,caseType: caseType}}">指标</el-menu-item>
                    <el-menu-item v-if="permission" :index="'/case/'+caseId+'/rank'" :route="{name: 'rank', query:{caseName: caseName,caseType: caseType}}">排行</el-menu-item>
                </el-submenu>
                <el-menu-item v-if="permission" :index="'/case/'+caseId+'/api'" :route="{name: 'api', query:{caseName: caseName,caseType: caseType}}">API测试</el-menu-item>
            </el-menu-item-group>
        </el-submenu>
        <!-- <el-menu-item index="2">
            <i class="el-icon-edit-outline"></i>
            <span slot="title">测试</span>
      </el-menu-item>-->
    </el-menu>
</el-aside>
</template>

<script>
export default {
    name: "Aside",
    data() {
        return {
            caseName: this.$route.query.caseName,
            caseId: this.$route.params.id,
            caseType: this.$route.query.caseType,
        };
    },
    computed: {
        willShow: function () {
            if (this.caseType == 1) {
                return true;
            } else return false;
        },
        permission: function () {
            const roles = this.$store.getters.roles;
            if (roles.includes("root")) {
                return true;
            } else {
                return false;
            }
        }
    },
};
</script>
