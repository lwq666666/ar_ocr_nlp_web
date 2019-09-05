<template>
<el-button id="city_top" @click="haddleClick()" style="margin-top:300px;height:100px;width:400px;" type="primary">click<i class="el-icon-arrow-down"></i></el-button>
</template>

<script>
export default {
    methods: {
        haddleClick: function () {
            window.scrollTo(0,1460);
        }
    }
}
</script>