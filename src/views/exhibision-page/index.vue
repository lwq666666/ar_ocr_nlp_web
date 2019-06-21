<template>
<div>
    <div class="secondpagetop">
        <div>
            <div>
                <div class="title1" style="padding-top:50px">项目介绍</div>
                <div style="background-color:white;margin:30px;padding:20px;border:5px solid blue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;贵州省广播电视信息网络股份有限公司是整合全省广电网络、实行资产重组，于2008年3月27日成立的国有股份制文化企业，是贵州广电传媒集团旗下三家大二型企业之一。公司下设101家分公司，其中10个地级分公司、91个县级分公司，现有员工4329人（不含子公司），总资产逾85亿元。公司服务城乡有线数字电视用户超过631万户，高清互动电视用户达316万户，宽带用户达144万户，光缆网络实现了省、市、县、乡、村五级全覆盖。2016年12月，公司在上海证券交易所成功上市，成为贵州文化产业“第一股”。股票简称“贵广网络”，股票代码600996。
                    公司坚持把社会效益放在首位，大力实施“一云、双擎、三板块、四突破”的发展战略，构建多彩贵州“广电云”，充分发挥融合创新和资本运营双引擎驱动作用，推动“城市、农村、走出去”三大板块全面发展，在融合创新型业态、农村综合信息公共服务、资本运作及联合各省网络创新发展四大领域取得重大突破，取得了良好的社会效益和经济效益。</div>
            </div>
        </div>
    </div>
    <div class="secondpage">
        <div>
            <div style="background-color:#333;">
                <div class="title1">项目流程展示</div>
            </div>
        </div>
        <diagram style="display: -webkit-box; display: -ms-flexbox; display: flex; min-height: 650px; border: solid 40px #E9ECF1; background-color: #FCFCFC;border: solid 5px blue; width:60%;float:left; height:400px;margin:20px"></diagram>
        <div style="float:left;width:36%;padding-top:0px">
            <router-view />
        </div>
    </div>
    <div>
        <router-view name="bottom"></router-view>
    </div>
</div>
</template>

<script>
import Diagram from "./components/Diagram.vue";
export default {
    name: "secondpage",
    components: {
        Diagram
    }
};
</script>

<style scoped>
.secondpage {
    background: url(../../image/B2.jpg);
    height: 860px;
    position: relative;
    width: 100%;
    background-size: contain;
    background-color: black;
}

.title1 {
    padding: 80px 0 60px;
    color: #fff;
    font-size: 22px;
    text-align: center;
    margin: 0;
    line-height: inherit;
}

.secondpagetop {
    background: url(../../image/b2.png);
    height: 500px;
    position: relative;
    width: 100%;
    background-size: contain;
    background-color: black;
}
</style>
