<template>
<div class="bg">
    <router-view/>
</div>
</template>

<script>
export default {

}
</script>

<style scoped>
.bg {
    background: url(../../../../../image/background3.jpg);
    background-size: contain;
    height: 640px;
    margin: 20px;
    border: 10px ridge rgb(151, 230, 132);
    border-radius: 20px;
    width: 81.5%;
    overflow: scroll;
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
    clear: both
}

.box-card {
    width: 90%;
}

.el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
}

.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
}

.box-card3 {
    margin: 5px;
    height: 90px;
    background: url(../../../../../image/background2.jpg);
    background-size: contain;
}
</style>
