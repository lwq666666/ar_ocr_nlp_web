(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-58bff761"],{"4e8a":function(t,e,a){"use strict";var r=a("94ad"),i=a.n(r);i.a},"94ad":function(t,e,a){},a15f:function(t,e,a){t.exports=a.p+"img/user.6275f1a0.jpg"},d9ce:function(t,e,a){"use strict";a.r(e);var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("el-header",{staticStyle:{padding:"0",margin:"0"}},[a("Header")],1),a("router-view"),a("el-footer",{staticStyle:{"background-color":"gray"}},[a("Footer")],1)],1)},i=[],o=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("el-menu",{staticClass:"el-menu-demo",attrs:{mode:"horizontal","background-color":"black","text-color":"#fff","active-text-color":"#ffd04b"},on:{select:t.handleSelect}},[r("el-menu-item",{attrs:{index:"front-page"}},[t._v("首页")]),r("el-menu-item",{attrs:{index:"exhibision-page"}},[t._v("智能解题系统项目展示")]),r("el-dropdown",{staticStyle:{float:"right"},attrs:{trigger:"click"}},[r("div",{staticClass:"avatar-wrapper"},[r("img",{staticClass:"user-avatar",staticStyle:{width:"50px",height:"50px","margin-top":"5px","margin-right":"10px"},attrs:{src:a("a15f")}}),r("i",{staticClass:"el-icon-caret-bottom"})]),r("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[r("el-dropdown-item",[r("span",{staticStyle:{display:"block"},on:{click:t.reset}},[t._v("修改密码")])]),r("el-dropdown-item",{attrs:{divided:""}},[r("span",{staticStyle:{display:"block"},on:{click:t.logout}},[t._v("退出登录")])])],1)],1),r("div",{staticStyle:{float:"right",color:"white","line-height":"60px","margin-right":"10px"}},[t._v(t._s(t.roles[0]))])],1)},n=[],l=(a("0feb"),{data:function(){return{roles:this.$store.getters.roles}},methods:{handleSelect:function(t){this.$router.push({path:"/"+t})},logout:function(){var t=this;this.$store.dispatch("LogOut").then(function(){t.$router.push({name:"login"})})},reset:function(){this.$router.push({name:"reset"})}}}),s=l,c=(a("4e8a"),a("2877")),d=Object(c["a"])(s,o,n,!1,null,"11c6ea86",null),u=d.exports,f=function(){var t=this,e=t.$createElement;t._self._c;return t._m(0)},p=[function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"footer-bottom clearfix"},[r("div",{staticStyle:{float:"left"}},[r("div",{staticClass:"editable",staticStyle:{"font-color":"gray"},attrs:{"data-editable":"type=fragment;name=footer-left-content"}},[r("div",[t._v("\n                清水河校区：成都市高新区（西区）西源大道2006号　邮编： 611731   ")]),r("div",[t._v("\n                沙河校区：成都市建设北路二段四号　邮编：610054")])])]),r("div",{staticStyle:{float:"right"}},[r("div",[r("a",{staticStyle:{"margin-right":"10px"}},[r("img",{attrs:{src:a("f024"),height:"60px"}})])])])])}],h={},g=Object(c["a"])(h,f,p,!1,null,null,null),m=g.exports,v={name:"Layout",components:{Header:u,Footer:m}},x=v,b=Object(c["a"])(x,r,i,!1,null,null,null);e["default"]=b.exports},f024:function(t,e,a){t.exports=a.p+"img/wx.dfc0e4fa.png"}}]);
//# sourceMappingURL=chunk-58bff761.b7a4a68b.js.map