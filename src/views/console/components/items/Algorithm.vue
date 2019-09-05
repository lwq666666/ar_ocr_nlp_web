<template>
  <div style="text-align: center">
    <el-alert
      title=""
      type="success"
      style="margin-bottom: 50px"
      :closable="false"
      show-icon>
      {{caseName}}/管理配置/算法配置
    </el-alert>
    <el-transfer v-model="value1"
                 :data="data"
                 :titles="['未启用算法', '当前业务算法']"
                 style="text-align: left; display: inline-block">
    </el-transfer>
    <div style="margin-top: 50px">
      <el-button type="primary" plain :loading="buttonLoading" @click="editAlgorithm(value1)">确认</el-button>
    </div>
  </div>
</template>

<script>
    export default {
        name: "Algorithm",
        data() {
          return {
            caseName: this.$route.query.caseName,
            caseId: this.$route.params.id,
            data: [],
            value1: [],
            buttonLoading:false
          };
        },
        created() {
          this.$ajax.get('businesses/'+ this.caseId+'/algorithms' ).then(response => {
            const algorithms = response.data.algorithms;
            const length = algorithms.length;
            for (let i=0; i<length; i++) {
              this.data.push({
                key: algorithms[i].id,
                label: algorithms[i].algorithmName
              });
            }
            const configAlgorithms = response.data.configAlgorithms;
            const length1 = configAlgorithms.length;
            for (let j=0; j<length1; j++) {
              this.value1.push(configAlgorithms[j].id)
            }
          }).catch(function () {

          });
        },
        methods: {
          editAlgorithm(value1) {
            this.buttonLoading = true;
            var valueString = "";
            value1.forEach(element => {
              valueString += (element+',');
            });
            this.$ajax({
              method: 'put',
              url: 'businesses/'+ this.caseId,
              params: {
                value:valueString.substr(0, valueString.length - 1)
              }
            }).then(() => {
                this.buttonLoading = false;
                this.$notify({
                  title: '成功',
                  message: '算法配置成功',
                  type: 'success'
                });
            }).catch(error => {
              this.buttonLoading = false;
                this.$notify({
                  title: '失败',
                  message: error.response.data.msg,
                  type: 'error'
                });
            });
          }
        }
    }
</script>

