<template>
<div>
    <el-alert title="" type="success" style="margin-bottom: 50px" :closable="false" show-icon>
        {{caseName}}/管理配置/统计分析/排行
    </el-alert>
    <el-card class="box-card" style="width: 50%;margin-left: 20%">
        <el-tabs v-model="activeName">
            <el-tab-pane :label="rankName1" name="first">
                <el-table :show-header=false :data="rankData1" style="width: 100%" max-height="500">
                    <el-table-column prop="mediaId" label="媒资ID" width="400">
                    </el-table-column>
                </el-table>
                <!--<div class="block">-->
                <!--<el-pagination layout="prev, pager, next" :total="22">-->
                <!--</el-pagination>-->
                <!--</div>-->
            </el-tab-pane>
            <el-tab-pane :label="rankName2" name="second">
                <el-table :show-header=false :data="rankData2" style="width: 100%">
                    <el-table-column prop="mediaId" label="日期" width="400">
                    </el-table-column>
                </el-table>
                <!--<div class="block">-->
                <!--<el-pagination layout="prev, pager, next" :total="22">-->
                <!--</el-pagination>-->
                <!--</div>-->
            </el-tab-pane>
        </el-tabs>
    </el-card>

</div>
</template>

<script>
export default {
    name: "rank",
    data() {
        return {
            caseName: this.$route.query.caseName,
            //                rankData1: [{mediaId: "5aa9d99e1e7f525a076fd49ce2cc3230"}, {mediaId: "111"}],
            rankData1: [],
            rankName1: "",
            rankData2: [],
            rankName2: "",
            activeName: "first"
        }
    },
    created: function () {
        this.getRankData();
    },
    methods: {
        getRankData() {
            this.rankData1 = [];
            this.rankData2 = [];
            getRankList(this.$route.params.id, 10).then((res) => {
                let data = res.data;
                let index = 1;
                for (let key in data) {
                    if (index == 1) {
                        this.rankName1 = key;
                        let media = {};
                        let medias = JSON.parse(data[key]);
                        for (let item in medias) {
                            if (item != null && item != "") {
                                media.mediaId = "无数据";
                                let index = this.rankData1.push(media);
                                console.log("1index=" + index + "查看现在index的数据是多少" + this.rankData1[index - 1].mediaId);
                                this.getMediaName(1, index, medias[item]);
                            }
                        }
                    } else if (index == 2) {
                        this.rankName2 = key;
                        let media = {};
                        let medias = JSON.parse(data[key]);
                        for (let item in medias) {
                            if (item != null && item != "") {
                                media.mediaId = "无数据";
                                let index = this.rankData2.push(media);
                                console.log("2index=" + index + "查看现在index的数据是多少" + this.rankData2[index - 1].mediaId);
                                this.getMediaName(2, index, medias[item]);
                            }
                        }
                    }
                    index++;
                }
            }).catch(function () {

            });
        },

        getMediaName(option, index, itemId) {
            getItemName(itemId).then(res => {
                let media = {};
                let itemName = res.data.data;
                media.mediaId = "媒资名：" + itemName;
                if (option == 1) {
                    console.log("1index=" + index + "查看修改前数据是多少" + this.rankData1[index - 1].mediaId);
                    this.rankData1.splice(index - 1, 1, media);
                    console.log("1index=" + index + "查看修改后数据是多少" + this.rankData1[index - 1].mediaId);
                } else if (option == 2) {
                    console.log("2index=" + index + "查看修改前数据是多少" + this.rankData2[index - 1].mediaId);
                    this.rankData2.splice(index - 1, 1, media);
                    console.log("2index=" + index + "查看修改后数据是多少" + this.rankData2[index - 1].mediaId);
                }
            }).catch(() => {});
        }
    }
}
</script>
