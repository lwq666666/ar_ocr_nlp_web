<template>
  <div>
    <h1 align="center" class="headers">人脸注册</h1>
    <div class="index">
      <el-input v-model="input" placeholder="请输入身份证ID" ></el-input>
    </div>
    <div style="margin-left: 50px;width: 85%">
      <p style="margin-bottom: 2px">请拍摄3张自拍图像</p>
      <!--拍摄一张验证-->
      <el-upload
        action="http://localhost:8762/api/face-validate"
        list-type="picture-card"
        :on-preview="handlePictureCardPreview"
        :multiple="isMultiple"
        :file-list="productImgs"
        :on-error="imgUploadError"
        :limit="imgLimit"
        accept="image/jpeg,image/gif,image/jpg,image/png"
        :on-exceed="handleExceed"
        :http-request="uploadFile"
        ref="upload"
        :auto-upload="false">
        <i class="el-icon-plus"></i>
      </el-upload>
      <el-dialog :visible.sync="dialogVisible">
        <img width="100%" :src="dialogImageUrl" alt="">
      </el-dialog>
    </div>
    <div style="border-top: 1px solid #ccc;margin-left: 50px;width: 85%">
      <p>人脸检测图像</p>
      <ul>
        <li class ="img_iden" id ="detecturl"><img ></li>
      </ul>
    </div>
    <div style="border-top: 1px solid #ccc;margin-left: 50px;width: 85%">
      <p>人脸识别图像</p>
      <ul>
        <li class ="img_iden" id="imgUrl"><img ></li>
      </ul>
    </div>
    <div class="centerbu">
      <el-button @click="subPicForm" type="primary" class="buttonnum" v-if="show">点击上传到服务器进行身份验证</el-button>
      <el-button @click="subReg" type="primary" class="buttonnum" v-else>注册</el-button>
      <el-button @click="indexfile" type="primary" class="buttonnum" >返回首页</el-button>
    </div>
  </div>
</template>

<script>

  import axios from 'axios'
  import qs from 'qs'


  export default {
      data(){
        return {
          dialogImageUrl: '',
          dialogVisible: false,
          isMultiple: true,
          productImgs: [],
          imgLimit: 3,
          input:'',
          formDate:'',
          imageUrl:'',
          show:true
        }
      },
    methods: {

      handlePictureCardPreview(file) {
        this.dialogImageUrl = file.url;
        this.dialogVisible = true;
        this.imageUrl = URL.createObjectURL(file.raw)
      },
      // handleAvatarSuccess(res, file) {//图片上传成功
      //   console.log(res);
      //   console.log(file);
      //   this.imageUrl = URL.createObjectURL(file.raw);
      // },
      handleExceed(files, fileList) {//图片上传超过数量限制
        this.$message.error('上传图片不能超过3张!');
        console.log(file, fileList);
      },
      imgUploadError(err, file, fileList){//图片上传失败调用
        console.log(err)
        this.$message.error('上传图片失败!');
      },
      // beforeUpload(file){
      //   let fd = new FormData();//通过form数据格式来传
      //   fd.append("files",file);
      //   fd.append("uid",this.input);
      //   var url = this.serverUrl;
      //
      //   axios.post(url,fd).then(
      //     res=>{
      //       console.log(res.data);
      //     })
      // },
      uploadFile(file){
          this.formDate.append('files',file.file);
          // this.formData.append('uid',this.input);
      },
      subPicForm(){
        this.formDate = new FormData();
        this.$refs.upload.submit();
        let config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
        axios.post("http://localhost:8762/face-validate",this.formDate,config).then(res =>{

          alert(res.data);
          this.show=false;
        }).catch(res =>{
          alert(res.data);
        })
      },
      subReg(){
        this.formDate = new FormData();
        this.$refs.upload.submit();
        this.formDate.append('uid', this.input);
        let config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        };
        axios.post("http://localhost:8762/face-reg",this.formDate,config).then(res =>{
          alert(res.data);
            let imgurls =[];
            imgurls = res.data.imgUrl.split(",");
            for(let i=0;i<imgurls.length;i++){
                let img=new Image();
                img.src ="data:image/jpg;base64,"+imgurls[i];
                console.log(img.src);
                img.style.width = 148+"px";
                img.style.height = 148+"px";
                let imgContainer=document.getElementById("imgUrl");
                imgContainer.appendChild(img);
            }

            let imgdeurls =[];
            imgdeurls = res.data.img_detectUrl.split(",");
            for(let j=0;j<imgdeurls.length;j++){
                let imgdete=new Image();
                imgdete.src ="data:image/jpg;base64,"+imgdeurls[j];
                console.log(imgdete.src);
                imgdete.style.width = 148+"px";
                imgdete.style.height = 148+"px";
                let imgConDete=document.getElementById("detecturl");
                imgConDete.appendChild(imgdete);
            }
        }).catch(res =>{
          alert(res.data);
        });
        // axios.post("http://localhost:8089/face-train").then(res =>{
        //   //alert(res.data);
        //   console.log(res.status);
        // }).catch(res =>{
        //   console.log(res)
        // })
      },
      indexfile(){
        this.$router.push('/indexapp');
      }

    }

  }
</script>

<style>
  .index{
    width: 85%;
    height: auto;
    margin-left: 50px;
  }

  .centerbu{
    text-align: center;
    width: 85%;
    height: auto;
    margin-top: 20px;
  }
  .centerbu >.buttonnum{
    width: 60%;
    margin-top: 15px;
  }

</style>


