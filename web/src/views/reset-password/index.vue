<template>
<div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">
        <div class="title-container">
            <h2 v-if="loginForm._account" class="title">当前用户：{{loginForm._account}}</h2>
            <h2 v-if="loginForm._account" class="title">首次登录，请修改密码</h2>
        </div>

        <el-form-item prop="password">
            <span style="color:white;">请输入新密码</span>
            <span class="svg-container">
          <svg-icon icon-class="password"/>
        </span>
            <el-input :type="passwordType" v-model="loginForm.password" name="password" auto-complete="on" @keyup.enter.native="handleLogin" />
            <span class="show-pwd" @click="showPwd">
          <svg-icon icon-class="eye"/>
        </span>
        </el-form-item>
        <el-form-item prop="passwordAgain">
            <span style="color:white;">再次输入密码</span>
            <span class="svg-container">
          <svg-icon icon-class="password"/>
        </span>
            <el-input :type="passwordType" v-model="loginForm.passwordAgain" name="password" auto-complete="on" @keyup.enter.native="handleLogin" />
            <span class="show-pwd" @click="showPwd">
          <svg-icon icon-class="eye"/>
        </span>
        </el-form-item>
        <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleChangePassword">提交</el-button>
    </el-form>
</div>
</template>

<script>
import {
    isvalidUsername
} from "@/utils/validate";
import {
    updateAccount
} from "@/api/permission";

export default {
    name: "Login",
    data() {
        const validatePassword = (rule, value, callback) => {
            if (value.length < 3) {
                callback(new Error("密码必须在3位以上！"));
            } else {
                callback();
            }
        };
        const validatePasswordAgain = (rule, value, callback) => {
            if (value != this.loginForm.password) {
                callback(new Error("两次输入密码不一致！"));
            } else if (value == this.loginForm._password) {
                callback(new Error("不能与旧密码相同！"));
            } else {
                callback();
            }
        };
        return {
            loginForm: {
                _account: this.$route.params.account,
                _password: this.$route.params.password,
                password: "",
                passwordAgain: ""
            },
            loginRules: {
                password: [{
                    required: true,
                    trigger: "blur",
                    validator: validatePassword
                }],
                //validator跟porp绑定
                passwordAgain: [{
                    required: true,
                    trigger: "blur",
                    validator: validatePasswordAgain
                }]
            },
            passwordType: "password",
            loading: false,
            showDialog: false,
            redirect: undefined
        };
    },

    methods: {
        showPwd() {
            if (this.passwordType === "password") {
                this.passwordType = "";
            } else {
                this.passwordType = "password";
            }
        },
        handleChangePassword() {
            this.$refs.loginForm.validate(valid => {
                if (valid) {
                    this.loading = true;
                    updateAccount(this.loginForm.password)
                        .then(response => {
                            console.log(response);
                            if (response.code == 200) {
                                this.$router.push({
                                    path: "/layout"
                                });
                            }
                            this.loading = false;
                            // this.$router.push({
                            //     path: this.redirect || "/"
                            // });
                        })
                        .catch(error => {});
                } else {
                    console.log("error submit!!");
                    return false;
                }
            });
        }
    }
};
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #eee;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .login-container .el-input input {
        color: $cursor;

        &::first-line {
            color: $light_gray;
        }
    }
}

/* reset element-ui css */
.login-container {
    .el-input {
        display: inline-block;
        height: 47px;
        width: 60%;

        input {
            background: transparent;
            border: 0px;
            -webkit-appearance: none;
            border-radius: 0px;
            padding: 12px 5px 12px 15px;
            color: $light_gray;
            height: 47px;
            caret-color: $cursor;

            &:-webkit-autofill {
                -webkit-box-shadow: 0 0 0px 1000px $bg inset !important;
                -webkit-text-fill-color: $cursor !important;
            }
        }
    }

    .el-form-item {
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        color: #454545;
    }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
    min-height: 100%;
    width: 100%;
    background-color: $bg;
    overflow: hidden;

    .login-form {
        position: relative;
        width: 520px;
        max-width: 100%;
        padding: 160px 35px 0;
        margin: 0 auto;
        overflow: hidden;
    }

    .tips {
        font-size: 14px;
        color: #fff;
        margin-bottom: 10px;

        span {
            &:first-of-type {
                margin-right: 16px;
            }
        }
    }

    .svg-container {
        padding: 6px 5px 6px 15px;
        color: $dark_gray;
        vertical-align: middle;
        width: 30px;
        display: inline-block;
    }

    .title-container {
        position: relative;

        .title {
            font-size: 26px;
            color: $light_gray;
            margin: 0px auto 40px auto;
            text-align: center;
            font-weight: bold;
        }

        .set-language {
            color: #fff;
            position: absolute;
            top: 5px;
            right: 0px;
        }
    }

    .show-pwd {
        position: absolute;
        right: 10px;
        top: 7px;
        font-size: 16px;
        color: $dark_gray;
        cursor: pointer;
        user-select: none;
    }

    .thirdparty-button {
        position: absolute;
        right: 0;
        bottom: 6px;
    }
}
</style>
