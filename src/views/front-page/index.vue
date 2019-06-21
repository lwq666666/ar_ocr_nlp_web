<template>
<div>
    <div>
        <div class="setbg">
            <h1 style="padding-top:40px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;贵州广电·推荐引擎&nbsp;&nbsp;&nbsp;Recommendation Engine</h1>
            <div>
                <div style="height:200px;"></div>
                <img style="width:350px;height:350px;position: relative;float:left;padding-left:40px" src="@/image/2.png"/>
                <div>
                    <div style="height:25px;"></div>
                    <CardFront style="height:300px;position: relative;float:right;"></CardFront>
                </div>
            </div>
        </div>
    </div>
    <div style="background-color:#333;">
        <div style="height:200px"></div>
        <div>
            <h3>精心打造的功能</h3>
            <div style="margin:auto;width:80%;border-style: outset;background-color:white">
                <select-front></select-front>
            </div>
        </div>
    </div>
    <div style="background-color:#333;">
        <div style="height:100px"></div>
        <div>
            <h3>推荐适用场景</h3>
            <div style="margin:auto;width:80%;border-style: outset;background-color:white">
                <TabFront></TabFront>
            </div>
        </div>
    </div>
    <div style="background-color:#333;">
        <div style="height:100px"></div>
    </div>
</div>
</template>

<script>
import CardFront from "./CardFront.vue";
import SelectFront from "./SelectFront.vue";
import TabFront from "./TabFront.vue";
export default {
    name: "frontpage",
    components: {
        CardFront,
        SelectFront,
        TabFront
    }
}
</script>

<style scoped>
.setbg {
    background: url("../../image/1.jpg");
    height: 520px;
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
