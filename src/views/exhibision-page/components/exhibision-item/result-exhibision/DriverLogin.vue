<template>
<div>
    <p style="text-align:center;font-size:30px;margin-top:120px;">电子科技大学-推荐系统</p>
    <el-card class="bg-card4" shadow="hover">
        <el-form>
            <el-form-item>
                <el-input v-model="uid" placeholder="请输入用户uid"></el-input>
            </el-form-item>
            <el-form-item style="text-align:center">
                <el-button @click="login()" type="primary">登录</el-button>
            </el-form-item>
        </el-form>
    </el-card>
</div>
</template>

<script>
export default {
    data() {
        return {
            uid: ""
        };
    },
    methods: {
        login() {
            this.$router.push({
                name: 'DriverList',
                query: {
                    uid: this.uid
                }
            });
        }
    }
}
</script>

<style scoped>
.bg-card4 {
    margin: 70px;
    margin-top: 70px;
}
</style>
