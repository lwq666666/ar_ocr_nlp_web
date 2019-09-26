<template>
    <div>
        <el-main style=" border:8px dotted gray;  background-color: #f5f6f7;height:680px">
            <el-form :label-position="labelPosition" :model="form" label-width="60px">
                <el-form-item style="margin: 0px" label="上传题目图片:"></el-form-item>

                <el-upload
                        action="http://localhost:5000/up_photo"
                        list-type="picture-card"
                        :on-preview="handlePictureCardPreview"
                        :file-list="img_list"
                        limit="1"
                        :auto-upload="false"
                        ref="upload"
                        :on-progress="update"
                        :on-remove="handleRemove">
                    <i class="el-icon-plus"></i>
                </el-upload>
                <el-button style="margin-top: 10px" size="small" type="primary" @click="submitUpload">上传到服务器
                </el-button>

                <el-form-item style="margin-top: 30px" label="题目内容:">
                    <el-input
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 500}"
                            v-model="form.question"
                            style="width:600px"
                    ></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button size="small" type="primary" @click="onSubmit">解题开始</el-button>
                </el-form-item>
                <el-form-item label="自然语言处理结果:">
                    <el-input
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 500}"
                            v-model="form.nlp"
                            style="width:600px"
                    ></el-input>
                </el-form-item>
                <el-form-item label="模型自动生成的java类">
                    <el-input
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 500}"
                            v-model="form.java"
                            style="width:600px"
                    ></el-input>
                </el-form-item>
                <el-form-item label="解题过程">
                    <el-input
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 500}"
                            v-model="form.precess"
                            style="width:600px"
                    ></el-input>
                </el-form-item>
            </el-form>
        </el-main>
    </div>
</template>

<script>
    import Diagram from "./components/Diagram.vue";
    import {reasoning} from "@/api/reasoning";
    import {Loading} from "element-ui";

    export default {
        data() {
            return {
                img_list: [],
                labelPosition: "top",
                form: {
                    question: "",
                    nlp: "",
                    java: "",
                    precess: ""
                }
            };
        },
        methods: {
            update(event, file, fileList) {
                alert("123");
            },
            submitUpload() {
                this.$refs.upload.submit();
            },
            add() {
                /*let loadingInstance = Loading.service({
                  fullscreen: true,
                  text: "拼命解题中"
                });

                reasoning(this.form.question).then(response => {
                  if (response.code == 200) {
                    this.$notify({
                      title: "识别成功",
                      message: response.msg,
                      type: "success"
                    });*/
                this.form.question = "sinA=1,求A";
                /*this.$nextTick(() => {
                  // 以服务的方式调用的 Loading 需要异步关闭
                  loadingInstance.close();
                });
              }
            });*/
            },
            onSubmit() {
                let loadingInstance = Loading.service({
                    fullscreen: true,
                    text: "拼命解题中"
                });

                reasoning(this.form.question).then(response => {
                    if (response.code == 200) {
                        this.$notify({
                            title: "解题成功",
                            message: response.msg,
                            type: "success"
                        });
                        this.form.nlp = response.data.nlp;
                        this.form.java = response.data.java;
                        this.form.precess = response.data.precess;
                        this.$nextTick(() => {
                            // 以服务的方式调用的 Loading 需要异步关闭
                            loadingInstance.close();
                        });
                    }
                });
            }
        },
        name: "secondpage",
        components: {
            Diagram
        }
    };
</script>

<style scoped>
    .secondpage {
        /* background: url(../../image/B2.jpg); */
        height: 860px;
        position: relative;
        width: 100%;
        background-size: contain;
        background-color: #f5f6f7;
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
