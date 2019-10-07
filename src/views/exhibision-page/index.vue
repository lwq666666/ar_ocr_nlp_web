<template>
  <div>
    <el-main style=" border:8px dotted gray;  background-color: #f5f6f7;height:680px">
      <el-form :label-position="labelPosition" :model="form" label-width="60px">
        <el-form-item style="margin: 0px" label="上传题目图片:"></el-form-item>

        <el-upload
          :action="imgUrl"
          list-type="picture-card"
          :file-list="img_list"
          :limit="1"
          :auto-upload="false"
          ref="upload"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
          :on-exceed="handleExceed"
          :on-error="imgUploadError"
        >
          <i class="el-icon-plus"></i>
        </el-upload>
        <el-button style="margin-top: 10px" size="small" type="primary" @click="submitUpload">识图开始</el-button>

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
import { reasoning } from "@/api/reasoning";
import { Loading } from "element-ui";

export default {
  data() {
    return {
      imgUrl: "http://localhost:8762/reason/upload",
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
    submitUpload() {
      this.$refs.upload.submit();
    },
    beforeAvatarUpload(file) {
      //文件上传之前调用做一些拦截限制
      console.log(file);
      const isJPG = true;
      // const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;

      // if (!isJPG) {
      //   this.$message.error('上传头像图片只能是 JPG 格式!');
      // }
      if (!isLt2M) {
        this.$message.error("上传图片大小不能超过 2MB!");
      }
      return isJPG && isLt2M;
    },
    handleAvatarSuccess(res, file) {
      //图片上传成功，翻译成功
      console.log(res);
      console.log(file);
      this.$message.success("识图成功!");
      this.form.question = res.data.result;
    },
    handleExceed(files, fileList) {
      //图片上传超过数量限制
      this.$message.error("上传图片不能超过1张!");
      console.log(file, fileList);
    },
    imgUploadError(err, file, fileList) {
      //图片上传失败调用
      console.log(err);
      this.$message.error("识图失败!");
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
