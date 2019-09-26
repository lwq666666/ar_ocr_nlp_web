<template>
<div>
  <div class="train_top">
    <div class="tech-banner-content">
      <div class="tech-banner-title">
        人脸识别
      </div>
      <div class="tech-banner-info">
        基于深度学习的人脸识别方案，准确识别图片中的人脸信息，提供人脸属性识别、关键点定位、人脸1：1比对、人脸1：N识别、活体检测等能力
      </div>
    </div>
  </div>
  <div class="catalog">
    <div class="ai-container" >
      <div class="catalog-title">训练功能</div>
      <div class="catalog-gallery">
        <div class="tech-prod-container">
          <div class="tech-prod-item-img"></div>
          <div class="tech-prod-item-info">
            <p> 人脸训练操作</p>
            <el-button @click="train" class="btn-primary-new" plain>点击执行训练操作</el-button>
          </div>
        </div>
        <div class="tech-prod-container">
          <div class="tech-prod-item-img2"></div>
          <div class="tech-prod-item-info">
            <p> 注册训练模型</p>
            <el-button class="btn-primary-new" @click="registeModel" :disabled="visible">注册训练模型</el-button>
          </div>
        </div>
      </div>
    </div>

  </div>
  <el-dialog title="模型注册" :visible.sync="dialogVisible" width="40%" center="true">
    <el-form :model="modelform" :rules="rules" ref="modelform" label-width="100px">
      <el-form-item label="模型名称" prop="modelName">
        <el-input v-model="modelform.modelName" placeholder="请输入模型名称"></el-input>
      </el-form-item>
      <el-form-item label="模型类型" prop="modelType">
        <el-select class="filter-item" v-model="modelform.modelType" placeholder="请选择">
          <el-option v-for="item in  sexOptions" :key="item" :label="item" :value="item"> </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间" prop="createTime">
        <el-date-picker v-model="modelform.createTime" type="datetime" placeholder="选择日期时间"></el-date-picker>
      </el-form-item>
      <el-form-item label="描述" prop="description">
        <el-input type="textarea" :rows="3" v-model="modelform.description" placeholder="请输入模型名称"></el-input>
      </el-form-item>

    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="cancel('form')">取 消</el-button>
      <el-button type="primary" @click="addModel('form')">确 定</el-button>
    </div>
  </el-dialog>

</div>
</template>

<script>

import {trainData,registeObj} from '@/api/face';
import axios from  'axios'
export default {
  data(){

     return{
         modelform:{
             modelName:'',
             modelType:'',
             filePath:'',
             createTime:'',
             description:'',
         },
         rules:{
             modelName: [
                 {required: true, message: '请输入模型名称', trigger: 'blur'}
             ],
             modelType: [
                 {required: true, message: '请选择类型', trigger: 'blur'}
             ],
             createTime: [
                 {required: true, message: '请选择创建时间', trigger: 'blur'}
             ],
             description: [
                 {required: false, message: '添加详细信息', trigger: 'blur'}
             ],
         },
         dialogVisible:false,
         visible:true,
         sexOptions:['识别','检测','特性提取'],
     }
  },
  methods:{
      train(){
          axios.post("http://localhost:8762/model/face-train").then(res =>{
            //alert(res.data);
            console.log(res);
            if(res.status == 200){
                this.modelform.filePath = res.data.data.result;
                this.visible = false;
                this.$notify({
                    title: '成功',
                    message: '训练成功',
                    type: 'success',
                    duration: 2000
                });
            }
          }).catch(res =>{
            console.log(res)
          })
      },
      registeModel(){
          this.dialogVisible = true;
      },

      cancel(formName) {
          this.dialogVisible = false;
          this.$refs[formName].resetFields();
      },
      addModel(formName){
          console.log(this.modelform);
          if(this.modelform.filePath == ""){
              this.cancel();
          }else {
              registeObj(this.modelform)
                  .then(() => {
                      this.dialogVisible = false;
                      this.$notify({
                          title: '成功',
                          message: '注册成功',
                          type: 'success',
                          duration: 2000
                      });
                  })
          }

      }
  }
}
</script>

<style>
.train_top{
  background: url(../../image/B3.jpg);
  height: 500px;
  position: relative;
  width: 100%;
  background-size: contain;
  background-color: black;
  text-align: center;
  box-sizing: border-box;
}
  .tech-banner-content{
    display: inline-block;
    vertical-align: middle;
    position: relative;
    margin-top: 50px;
  }
.tech-banner-title {
  padding-bottom: 24px;
  font-size: 48px;
  letter-spacing: 5px;
  color: #fff;}

.tech-banner-info {
  width: 500px;
  margin: 0 auto;
  padding-bottom: 24px;
  font-size: 20px;
  line-height: 28px;

  }

  .btn-primary-new{position: relative;
    border: 1px solid ;
    z-index: 1;}
.ai-container {
  display: block;
  width: 1180px;
  height: 100%;
  margin: 0 auto;
  position: relative;
  overflow: hidden;}
.catalog-title{padding: 80px 0 50px;
  font-size: 30px;
  letter-spacing: 2px;
  text-align: center;
  color: #333;}
.tech-prod-container{position: relative;margin: 0 18px 35px;vertical-align: top;width: 45%;display: inline-block;}
.tech-prod-item-img{position: relative;height: 220px;background: url(../../image/list-one.jpg) no-repeat;margin-left: 60px}
.tech-prod-item-img2{position: relative;height: 220px;background: url(../../image/list-two.jpg) no-repeat;margin-left: 60px}
  .tech-prod-item-info{    box-sizing: border-box;
    width: 100%;
    text-align: center;
    padding: 20px 30px;}
</style>


