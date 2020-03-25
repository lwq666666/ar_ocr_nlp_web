<template>
<el-container>
    <Aside />
    <el-main class="bg6">
        <router-view />
    </el-main>
</el-container>
</template>

<script>
import Aside from "./Aside";
export default {
    name: "Main",
    components: {
        Aside
    }
}
</script>

<style scoped>
.bg6 {
    background-color: white;
}
</style>
