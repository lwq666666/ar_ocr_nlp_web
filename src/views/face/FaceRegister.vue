<template>
  <div>
    <h1 align="center" class="headers">人脸注册</h1>
    <el-form ref="form" :model="form">
      <el-form-item class="index">
        <el-input v-model="form.input" placeholder="请输入身份证ID" ></el-input>
      </el-form-item>
      <el-form-item prop="picture" class="index">
        <el-col>请拍摄三张照片</el-col>
        <el-form-item style="display: inline-block">
          <div class="takePhotostyle" id="takeindex"><i class="el-icon-plus" @click="handleChange"></i></div>
          <div id="imgindex"></div>
        </el-form-item>
        <el-dialog title="拍摄图像"  :visible.sync="visibleCamera" placement="bottom" trigger="click" ref="dialog">
          <!--@click="handleCamera" modal="true" append-to-body="true"-->
          <div style="display: flex; width: 970px">
            <div class="cameraBox">
              <div style="text-align: center;font-size: 14px;font-weight: bold;margin-bottom: 10px;">摄像头</div>
              <video id="video" width="550" height="440" style="border: 1px solid #ccc" ref="myvedio"></video>
              <div class="iCenter" style="margin-top: 20px">
                <el-Button type='primary' long size='large' @click="takePhone" style='width: 200px;'>拍照</el-Button>
              </div>
            </div>
            <div>
              <div style="text-align: center;font-size: 14px;font-weight: bold;margin-bottom: 10px;">拍摄效果</div>
              <canvas id='canvas' width='440' height='440' style="display: block;border: 1px solid #ccc" ref="mycanvas"></canvas>
              <div class="iCenter" style="margin-top: 20px">
                <el-Button type='primary' long size='large' @click="takePhoneUpfile" style='width: 200px;' v-if="preViewVisible" >保存</el-Button>
              </div>
            </div>
          </div>
        </el-dialog>
      </el-form-item>
      <el-form-item style="border-top: 1px solid #ccc;margin-left: 50px;width: 85%">
        <p>人脸检测图像</p>
          <li class ="img_iden" id ="detecturl"><img ></li>
      </el-form-item>
      <el-form-item style="border-top: 1px solid #ccc;margin-left: 50px;width: 85%;border-bottom: 1px solid #ccc">
        <p>人脸对齐图像</p>
          <li class ="img_iden" id="imgUrl"><img ></li>
      </el-form-item>
    </el-form>
    <div class="centerbu">
      <el-button @click="subPicForm" type="primary" class="buttonnum" v-if="show">点击上传到服务器进行身份验证</el-button>
      <el-button @click="subReg" type="primary" class="buttonnum" v-else v-show="flag">注册</el-button>
      <el-button @click="indexfile" type="primary" class="buttonnum" >返回首页</el-button>
    </div>

  </div>
</template>

<script>

  import axios from 'axios'

  export default {
      data(){
        return {
          formDate:'',
           flag:true,
          image:false,
          show:true,
          imageurl:'',
          visibleCamera:false,
          preViewVisible:false,
          blobFile: null,
          canvas: null,
          video: null,
          MediaStreamTrack: null,
          memberInit: {}, //form标记
          images:[],
          number:0,
          form:{
            picture:'',
            input:'',
          }
        }
      },
    methods: {

      uploadFile(file){
          this.formDate.append('files',file.file);
          // this.formData.append('uid',this.input);
      },
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
        that.canvas.getContext('2d').drawImage(this.video, 90, 0, 440, 440, 0, 0, 440, 440) // context.drawImage(img,sx,sy,swidth,sheight,x,y,width,height);
        let dataurl = that.canvas.toDataURL('image/jpeg')
        let filename = this.randomString(5)+'.jpeg';
        console.log(filename);
        that.blobFile = that.dataURLtoFile(dataurl, filename)
        that.images[that.number++] =  that.blobFile;
        that.preViewVisible = true
      },
      //保存图片
      takePhoneUpfile() {
        let that = this;
        let type = 'png';
        that.canvas.getContext('2d').drawImage(this.video, 90, 0, 440, 440, 0, 0, 440, 440) // context.drawImage(img,sx,sy,swidth,sheight,x,y,width,height);
        let dataurl = that.canvas.toDataURL(type);
        dataurl = dataurl.replace(this._fixType(type),'image/octet-stream');
        that.visibleCamera=false;
        let myparent  = document.getElementById("imgindex");
        let mydiv = document.getElementById("takeindex");
        let offsetx = mydiv.offsetLeft;
        console.log( mydiv.offsetLeft);
        if(that.number <= 3){
          let myImage = document.createElement("img");
          myImage.src = dataurl;
          myparent.appendChild(myImage);
          myImage.style.marginRight = "2px";
          myImage.style.width = "148px";
          myImage.style.height = "148px";
          myparent.style.marginTop="-148px";
          mydiv.style.marginLeft = offsetx + 150+"px";
        }else {
          alert("图片超过指定的数量");
        }
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
      randomString(len) {
        len = len || 32;
        let $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
        let maxPos = $chars.length;
        let pwd = '';
        for (let i = 0; i < len; i++) {
          pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
        }
        return pwd;
      },
      subPicForm(){
        this.formDate = new FormData();
        for(let i=0;i<this.images.length;i++){
          this.formDate.append("files",this.images[i]);
        }
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
        for(let i=0;i<this.images.length;i++){
          this.formDate.append("files",this.images[i]);
        }
        this.formDate.append('uid', this.form.input);
        let config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        };
        axios.post("http://localhost:8762/face-reg",this.formDate,config).then(res =>{
          console.log(res.data);
            if(res.data.success == true){
                this.$notify({
                    title: '成功',
                    message: res.data.body,
                    type: 'success',
                    duration: 3000
                });
                let imgurls =[];
                imgurls = res.data.imgUrl.split(",");
                for(let i=0;i<imgurls.length;i++){
                    let img=new Image();
                    img.src ="data:image/jpg;base64,"+imgurls[i];
                    console.log(img.src);
                    img.style.width = 148+"px";
                    img.style.height = 148+"px";
                    img.style.marginRight = "2px";
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
                    imgdete.style.marginRight = "2px";
                    let imgConDete=document.getElementById("detecturl");
                    imgConDete.appendChild(imgdete);
                }
                this.flag = false;
            }else {
                this.$notify({
                    title: '注册失败',
                    message: "请重新注册",
                    type: 'success',
                    duration: 3000
                });
                this.flag = true;
            }

        }).catch(res =>{
          alert(res.data);
        });
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
    margin-bottom: 270px;

  }
  .centerbu >.buttonnum{
    width: 60%;
    margin-top: 15px;
  }
  .el-form-item {
    margin-bottom: 0px;
  }
  .el-dialog{
    width: 1100px;
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


