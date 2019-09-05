<template>
<div>
    <el-header style="padding:0;margin: 0">
        <Header></Header>
    </el-header>
    <router-view />
    <el-footer style="background-color:gray;">
        <Footer></Footer>
    </el-footer>
</div>
</template>

<script>
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";

export default {
    name: "Layout",
    components: {
        Header,
        Footer
    }
};
</script>
