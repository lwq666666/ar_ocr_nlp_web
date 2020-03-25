<template>
  <el-menu
    class="el-menu-demo"
    mode="horizontal"
    background-color="black"
    @select="handleSelect"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <el-menu-item index="front-page">首页</el-menu-item>
    <el-menu-item index="exhibision-page">自动解题部分展示</el-menu-item>
    <el-menu-item index="third-page">自动阅卷系统展示</el-menu-item>
    <el-dropdown style="float:right;" trigger="click">
      <div class="avatar-wrapper">
        <img
          src="@/image/user.jpg"
          style="width:50px;height:50px;margin-top:5px;margin-right:10px;"
          class="user-avatar"
        />
        <i class="el-icon-caret-bottom" />
      </div>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>
          <span style="display:block;" @click="reset">修改密码</span>
        </el-dropdown-item>
        <el-dropdown-item divided>
          <span style="display:block;" @click="logout">退出登录</span>
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <div style="float:right;color:white;line-height:60px;margin-right:10px;">{{roles[0]}}</div>
  </el-menu>
</template>

<script>
import { logout } from "@/api/permission";

export default {
  data() {
    return {
      roles: this.$store.getters.roles
    };
  },
  methods: {
    handleSelect(key) {
      this.$router.push({
        path: "/" + key
      });
    },
    logout() {
      this.$store.dispatch("LogOut").then(() => {
        this.$router.push({
          name: "login"
        });
      });
    },
    reset() {
      this.$router.push({
        name: "reset"
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  line-height: 50px;
  border-radius: 0px !important;

  .hamburger-container {
    line-height: 58px;
    height: 50px;
    float: left;
    padding: 0 10px;
  }

  .breadcrumb-container {
    float: left;
  }

  .errLog-container {
    display: inline-block;
    vertical-align: top;
  }

  .right-menu {
    float: right;
    height: 100%;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      margin: 0 8px;
    }

    .screenfull {
      height: 20px;
    }

    .international {
      vertical-align: top;
    }

    .theme-switch {
      vertical-align: 15px;
    }

    .avatar-container {
      height: 50px;
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}
</style>
