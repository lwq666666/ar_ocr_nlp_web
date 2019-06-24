<template>
  <div>
    <el-main style=" border:8px dotted gray;  background-color: #f5f6f7;height:660px">
      <el-form :label-position="labelPosition" :model="form" label-width="80px">
        <el-form-item label="输入题目:">
          <el-input
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 500}"
            v-model="form.question"
            style="width:600px"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">解题开始</el-button>
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
