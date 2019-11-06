<template>
  <div>
    <el-main style="height:680px">
      <el-form ref="form" :model="form" label-width="200px" style="padding:70px">
        <el-form-item label="请输入题目：">
          <el-input type="textarea" v-model="form.problem"></el-input>
        </el-form-item>
        <el-form-item :inline="true" label="请上传解题过程:">
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
        </el-form-item>
        <el-form-item :inline="true" label="识图结果:">
          <el-table :data="answer" style="width: 100%" :row-class-name="tableRowClassName">
            <el-table-column prop="text" label="过程" width="500">
              <template slot-scope="scope">
                <el-input v-model="scope.row.text"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="result" label="批改结果" width="180">
              <template slot-scope="scope">
                <i v-if="scope.row.result" class="el-icon-check" style="color:green"></i>
                <i v-else class="el-icon-close" style="color:red"></i>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>
        <el-form-item>
          <el-button style="margin-top: 10px" size="small" type="primary" @click="marking">开始自动批改</el-button>
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>
import { marking } from "@/api/reasoning";
import { Loading } from "element-ui";
import Qs from "qs";

export default {
  data() {
    return {
      imgUrl: "http://localhost:8762/reason/answer",
      answer: [
        { text: "1", result: true },
        { text: "2", result: false },
        { text: "22", result: true }
      ],
      form: {
        problem: "11"
      }
    };
  },
  methods: {
    marking() {
      marking().then(response => {
        console.log(response);
        if (response.code == 200) {
          this.$notify({
            title: "批改成功",
            message: response.msg,
            type: "success"
          });
          this.answer = response.data;
          
          this.$nextTick(() => {
            // 以服务的方式调用的 Loading 需要异步关闭
            loadingInstance.close();
          });
        }
      });
    },
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
    }
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
