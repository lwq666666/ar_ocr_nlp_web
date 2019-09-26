<template>
  <div>
    <h1 align="center" class="headers">人脸识别服务</h1>
    <el-form ref="formface" :model="formface">
      <el-form-item class="index">
        <el-input v-model="formface.input" placeholder="请输入身份证ID" ></el-input>
      </el-form-item>

    <div style="margin-left: 50px;width: 85%">
      <p style="margin-bottom: 2px">请拍摄1张自拍图像</p>
      <el-form-item >
        <div class="takePhotostyle" id="takeindex">
          <i class="el-icon-plus" @click="handleChange"></i>
        </div>
        <div id="imgindex" >
          <img  v-if="imageUrl" :src="imageshow" class="avatar" >
        </div>
      </el-form-item>
      <el-dialog title="拍摄图像"  :visible.sync="visibleCamera" placement="bottom" trigger="click" ref="dialog" width="45%">
        <!--@click="handleCamera" modal="true" append-to-body="true"-->
        <div style="display: flex; width: 970px">
          <div class="cameraBox">
            <div style="text-align: center;font-size: 14px;font-weight: bold;margin-bottom: 10px;">摄像头</div>
            <video id="video" width="550" height="440" style="border: 1px solid #ccc" ref="myvedio"></video>
            <div class="iCenter" style="margin-top: 20px">
              <el-Button type='primary' long size='large' @click="takePhone" style='width: 200px;'>
                拍照
              </el-Button>
            </div>
          </div>

          <div>
            <div style="text-align: center;font-size: 14px;font-weight: bold;margin-bottom: 10px;">
              拍摄效果
            </div>
            <canvas id='canvas' width='350' height='440' style="display: block;border: 1px solid #ccc"
                    ref="mycanvas"></canvas>
            <div class="iCenter" style="margin-top: 20px">
              <el-Button type='primary' long size='large' @click="takePhoneUpfile"
                         style='width: 200px;' v-if="preViewVisible" >保存</el-Button>
            </div>
          </div>
        </div>
      </el-dialog>
    </div>
    <el-form-item style="border-top: 1px solid #ccc;margin-left: 50px;width: 85%">
      <p>人脸检测图像</p>
      <li class ="img_iden" id ="detecturl"><img ></li>
    </el-form-item>
    <el-form-item style="border-top: 1px solid #ccc;margin-left: 50px;width: 85%;border-bottom: 1px solid #ccc">
      <p>人脸对齐图像</p>
      <li class ="img_iden" id="imgUrl"><img ></li>
    </el-form-item>
    <div class="centerbu">
      <el-button @click="subReg" type="primary" class="buttonnum" >识别</el-button>
      <el-button @click="indexfile" type="primary" class="buttonnum" >返回首页</el-button>
    </div>
    </el-form>
  </div>
</template>

<script>

  import axios from 'axios'
  import ElUploadList from "element-ui/packages/upload/src/upload-list";

  export default {
    components: {ElUploadList},
    data(){
      return {
        isMultiple: true,
        formDate:'',
        imageUrl:false,
        show:true,
        visibleCamera:false,
        preViewVisible: false,
        blobFile: null,
        canvas: null,
        video: null,
        MediaStreamTrack: null,
        memberInit: {}, //form标记
        formface:{
          input:'',
        }
      }
    },
    mounted() {
      this.memberInit = Object.assign({}, this.form);
      // 摄像头
      this.canvas = document.getElementById('canvas');
      this.video = document.getElementById('video');
      //this.setHeaders() // 上传token
      //this.handleCamera();
    },
    methods: {
      handleChange() {
        //console.log(this.$refs.dialog);
        this.visibleCamera = true;
        this.preViewVisible = false;
        setTimeout(() => {
          this.canvas = this.$refs.mycanvas;
          this.video = this.$refs.myvedio;
          //console.log(this.canvas);
          this.canvas.getContext('2d').clearRect(0, 0, this.canvas.width, this.canvas.height);
          let that = this;
          if (navigator.getUserMedia || navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({
              video: true,
              //audio: true
            }).then(function (stream) {
              that.MediaStreamTrack = typeof stream.stop === 'function' ? stream : stream.getTracks()[1];
              that.video.srcObject = stream;
              that.video.play()
            }).catch(function (err) {
              console.log(err)
            })
          } else if (navigator.getMedia) {
            navigator.getMedia({
              video: true
            }).then(function (stream) {
              that.MediaStreamTrack = stream.getTracks()[1];
              that.video.srcObject = stream;
              that.video.play()
            }).catch(function (err) {
              console.log(err)
            })
          } else if (navigator.webkitGetUserMedia) {
            navigator.webkitGetUserMedia({
              video: true
            }).then(function (stream) {
              that.MediaStreamTrack = stream.getTracks()[1];
              that.video.srcObject = stream
              that.video.play()
            }).catch(function (err) {
              console.log(err)
            })
          } else {
            navigator.mozGetUserMedia({
              video: true
            }).then(function (stream) {
              that.MediaStreamTrack = stream.getTracks()[1];
              that.video.srcObject = stream;
              that.video.play()
            }).catch(function (err) {
              console.log(err)
            })
          }
        }, 0);
      },
      takePhone() {
        let that = this
        //console.log(that.canvas);
        that.canvas.getContext('2d').drawImage(this.video, 140, 0, 350, 440, 0, 0, 350, 440) // context.drawImage(img,sx,sy,swidth,sheight,x,y,width,height);
        let dataurl = that.canvas.toDataURL('image/jpeg')
        that.blobFile = that.dataURLtoFile(dataurl, 'camera.jpg')
        that.preViewVisible = true
      },
      //保存图片
      takePhoneUpfile() {
        let that = this
        // let formData = new FormData()
        // formData.append('file', that.blobFile)

        let type = 'png';
        that.canvas.getContext('2d').drawImage(this.video, 140, 0, 350, 440, 0, 0, 350, 440) // context.drawImage(img,sx,sy,swidth,sheight,x,y,width,height);
        let dataurl = that.canvas.toDataURL(type);
        dataurl = dataurl.replace(this._fixType(type),'image/octet-stream');
        console.log(dataurl);
        //let save_link = document.createElementNS('http://www.w3.org/1999/xhtml', 'a');
        that.imageshow = dataurl;

        let divposition = document.getElementById('takeindex');
        let imgposition = document.getElementById('imgindex');
        divposition.style.margin = "0 150px 0 ";
        imgposition.style.margin = "-148px 0 1px 0 ";
        that.imageUrl = true;
        that.visibleCamera=false;
        //将图片放在上传的list中
        // that.onSubmit(formData) // formdata方式上传图片
      },

      _fixType(type){
        type = type.toLowerCase().replace(/jpg/i, 'jpeg');
        let r = type.match(/png|jpeg|bmp|gif/)[0];
        return 'image/' + r;
      },
      dataURLtoFile(dataurl, filename) {
        let arr = dataurl.split(',')
        let mime = arr[0].match(/:(.*?);/)[1]
        let bstr = atob(arr[1])
        let n = bstr.length
        let u8arr = new Uint8Array(n)
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n)
        }
        return new File([u8arr], filename, {type: mime})
      },

      subReg(){
        this.formDate = new FormData();
        //this.$refs.upload.submit();
        console.log(this.blobFile);
        this.formDate.append('uid', this.formface.input);
        this.formDate.append('file',this.blobFile);
        let config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        };
        axios.post("http://localhost:8087/face-recognise",this.formDate,config).then(res =>{
          //console.log("返回数据"+res.data);
          if(res.data != null){
              this.$notify({
                  title: '成功',
                  message: '带UID图片识别成功，头像属于对应uid人员',
                  type: 'success',
                  duration: 2000
              });
              let imgurls = [];
              imgurls = res.data.split(",");
              let imgdete=new Image();
              imgdete.src ="data:image/jpg;base64,"+imgurls[0];
              imgdete.style.width = 148+"px";
              imgdete.style.height = 148+"px";
              let imgConDete=document.getElementById("detecturl");
              imgConDete.appendChild(imgdete);

              let imgurl = new Image();
              imgurl.src ="data:image/jpg;base64,"+imgurls[1];
              imgurl.style.width = 148+"px";
              imgurl.style.height = 148+"px";
              let imgConurl=document.getElementById("imgUrl");
              imgConurl.appendChild(imgurl);

          }
        }).catch(res =>{
          console.log(res)
        })
      },
      indexfile(){
        this.$router.push('/layout');
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
    margin-top: 150px;
  }
  .centerbu >.buttonnum{
    width: 60%;
    margin-top: 15px;
  }
  .el-dialog{
    width: 970px;
  }

  .takePhotostyle{
    display: inline-block;
    text-align: center;
    cursor: pointer;
    outline: 0;
    background-color: #fbfdff;
    border: 1px dashed #c0ccda;
    border-radius: 6px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    width: 148px;
    height: 148px;
    line-height: 146px;
    vertical-align: top;
  }

  .takePhotostyle i{
    font-size: 30px;
    color: #8c939d;
    font-style: normal;
    font-weight: 400;
    font-family: element-icons!important;
  }

  .avatar{
    width: 148px;
    height: 148px;
    line-height: 146px;
  }
  .img_iden{list-style-type: none;margin-left: 0px;padding-right: 2px;}

</style>


