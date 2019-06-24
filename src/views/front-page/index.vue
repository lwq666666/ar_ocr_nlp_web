<template>
<div>
    <div>
        <div class="setbg">
            <h1 style="padding-top:40px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;电子科技大学·智慧教育项目&nbsp;&nbsp;&nbsp;</h1>
        </div>
    </div>
</div>
</template>

<script>
import SelectFront from "./SelectFront.vue";
import TabFront from "./TabFront.vue";
export default {
    name: "frontpage",
    components: {
        SelectFront,
        TabFront
    }
}
</script>

<style scoped>
.setbg {
    background: url("../../image/1.jpg");
    height: 700px;
    position: relative;
    width: 100%;
    background-size: contain;
    background-color: black;
}

h1 {
    color: #fff;
    font-size: 36px;
    position: relative;
    display: inline-block;
    font-weight: 400;
    margin-top: 49px;
    margin-bottom: 0;
    line-height: inherit;
    font-family: PingFangSC, helvetica neue, hiragino sans gb, arial,
        microsoft yahei ui, microsoft yahei, simsun, "sans-serif";
}

h2 {
    font-size: 18px;
    color: #fff;
    font-weight: bolder;
    margin: 0;
    font-family: PingFangSC, helvetica neue, hiragino sans gb, arial,
        microsoft yahei ui, microsoft yahei, simsun, sans-serif;
}

h3 {
    padding: 80px 0 60px;
    color: #fff;
    font-size: 22px;
    text-align: center;
    margin: 0;
    line-height: inherit;
}

/* p {
    margin-top: 12px;
    font-size: 14px;
    line-height: 20px;
    width: 220px;
    color: #fff;
} */
</style>
