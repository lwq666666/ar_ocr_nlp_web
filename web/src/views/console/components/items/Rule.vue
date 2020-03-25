<template>
<div>
    <el-alert title="" type="success" style="margin-bottom: 20px" :closable="false" show-icon>
        {{caseName}}/管理配置/规则配置
    </el-alert>
    <el-collapse v-model="activeName" accordion>
        <el-collapse-item title="优先屏蔽" name="1">
            <el-button type="primary" :loading="addShieldButtonLoading" style="margin-bottom: 15px;float: right" @click="showShieldDialog">新增规则
            </el-button>
            <el-table :data="shieldData" style="width: 100%" @sort-change="shieldSortChange">
                <el-table-column label="屏蔽列表">
                    <el-table-column prop="itemId" sortable="custom" label="媒资ID">
                    </el-table-column>
                    <el-table-column prop="itemName" label="媒资名">
                    </el-table-column>
                    <el-table-column prop="createTime" sortable="custom" label="规则创建日期">
                    </el-table-column>
                    <el-table-column label="操作">
                        <template slot-scope="scope">
                            <el-button size="mini" type="danger" :loading="deleteShieldButtonLoading" @click="showDeleteConfirm(1,scope.$index, scope.row,shieldData)">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table-column>
            </el-table>
            <el-pagination style="margin-top: 15px" @size-change="handleShieldSizeChange" @current-change="handleShieldCurrentChange" :current-page="shieldCurrentPage" :page-sizes="[5, 10, 20, 50]" :page-size="shieldPageSize" layout="total, sizes, prev, pager, next, jumper" :total="totleShieldRules">
            </el-pagination>
        </el-collapse-item>
        <el-collapse-item title="优先推荐" name="2">
            <el-button type="primary" :loading="addPriorityButtonLoading" style="margin-bottom: 15px;float: right" @click="showPriorityDialog">新增规则
            </el-button>
            <el-table :data="currentPriorityData" style="width: 100%" @sort-change="prioritySortChange">
                <el-table-column label="优选列表">
                    <el-table-column prop="itemId" sortable="custom" label="媒资ID">
                    </el-table-column>
                    <el-table-column prop="itemName" label="媒资名">
                    </el-table-column>
                    <el-table-column prop="createTime" sortable="custom" label="规则创建日期">
                    </el-table-column>
                    <el-table-column prop="priorityWeight" sortable="custom" label="推荐优先级(1-100)">
                    </el-table-column>
                    <el-table-column label="操作">
                        <template slot-scope="scope">
                            <el-button size="mini" type="primary" @click="showPriorityWeight(scope.row)">修改优先级
                            </el-button>
                            <el-button size="mini" type="danger" :loading="deletePriorityButtonLoading" @click="showDeleteConfirm(2,scope.$index, scope.row,currentPriorityData)">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table-column>
            </el-table>
            <el-pagination style="margin-top: 15px" @size-change="handlePrioritySizeChange" @current-change="handlePriorityCurrentChange" :current-page="priorityCurrentPage" :page-sizes="[5, 10, 20, 50]" :page-size="priorityPageSize" layout="total, sizes, prev, pager, next, jumper" :total="priorityDataLength">
            </el-pagination>
        </el-collapse-item>
        <!-- <el-collapse-item title="推荐列表去重" name="3">
                <div style="text-align: center">
                    去重周期:
                    <el-input v-model="frequency" style="width: 200px;margin-left: 10px;margin-right: 10px"></el-input>
                    小时
                    <br>
                    <el-button type="primary" :loading="editPeriodButtonLoading" style="margin-top: 15px;"
                               @click="submitForm(3)">更改周期
                    </el-button>
                </div>
            </el-collapse-item> -->
    </el-collapse>
    <!--新增屏蔽规则对话框-->
    <el-dialog title="新增屏蔽媒资" :visible.sync="dialogShieldVisible">
        <el-form :model="shieldForm" :rules="rules" ref="addShieldForm">
            <el-form-item label="媒资ID" label-width="120px" prop="id">
                <el-input v-model="shieldForm.id" auto-complete="off"></el-input>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="hideDialog">取 消</el-button>
            <el-button type="primary" @click="submitForm(1)">确 定</el-button>
        </div>
    </el-dialog>
    <!--新增新增规则对话框-->
    <el-dialog title="新增推荐媒资" :visible.sync="dialogPriorityVisible">
        <el-form :model="priorityForm" :rules="rules" ref="addPriorityForm">
            <el-form-item label="媒资ID" label-width="120px" prop="id">
                <el-input v-model="priorityForm.id" auto-complete="off"></el-input>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="hideDialog">取 消</el-button>
            <el-button type="primary" @click="submitForm(2)">确 定</el-button>
        </div>
    </el-dialog>
    <el-dialog title="修改推荐优先级" :visible.sync="priorityWeightVisible">
        <el-form :model="priorityWeightForm" :rules="rules" ref="">
            <el-form-item label="优先级" label-width="120px" prop="id">
                <el-input v-model="priorityWeightForm.weight" auto-complete="off" style="width: 30%"></el-input>
                <i style="margin-left: 12px" class="el-icon-info"> 优先级在1-100之间，越小推荐越靠前，默认为100</i>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="hideDialog">取 消</el-button>
            <el-button type="primary" @click="handleUpdateWeight()">确 定</el-button>
        </div>
    </el-dialog>
</div>
</template>

<script>
import {
    getRules,
    addShiedRule,
    addPriorityRule,
    updatePriorityScore,
    deleteShiedRule,
    deletePriorityRule
} from "@/api/rule";

const Operation = {
    INIT: 0,
    SHIELD: 1,
    COMMEND: 2,
    DUMPLICATION: 3,
};

export default {
    name: "Rule",
    data() {
        return {
            caseName: this.$route.query.caseName,
            activeName: '1',
            shieldData: [],
            shieldCurrentPage: 1,
            shieldPageSize: 5,
            totleShieldRules: 5,

            currentPriorityData: [],
            priorityCurrentPage: 1,
            priorityCurrentOderType: 0,
            priorityCurrentId: 0,
            priorityPageSize: 5,
            priorityDataLength: 0,

            priorityOrderType: 0,
            priorityIsAsc: true,
            shieldOrderType: 0,
            shieldIsAsc: true,

            frequency: 24,
            dialogShieldVisible: false,
            shieldForm: {
                name: ''
            },
            dialogPriorityVisible: false,
            priorityForm: {
                name: ''
            },
            priorityWeightForm: {
                weight: 0
            },
            priorityWeightVisible: false,
            addShieldButtonLoading: false,
            addPriorityButtonLoading: false,
            deleteShieldButtonLoading: false,
            deletePriorityButtonLoading: false,
            editPeriodButtonLoading: false,
        }
    },
    created: function () {
        this.getCurrentPageInfo(Operation.INIT);
    },
    watch: {
        shieldData: function (newShieldData, oldShieldData) {
            if (this.shieldData.length == 0 && this.shieldCurrentPage > 1) {
                this.handleShieldCurrentChange(this.shieldCurrentPage - 1);
            }
        },
        currentPriorityData: function (newPriorityData, oldPriorityData) {
            if (this.currentPriorityData.length == 0 && this.priorityCurrentPage > 1) {
                this.handlePriorityCurrentChange(this.priorityCurrentPage - 1);
            }
        }
    },
    methods: {
        getCurrentPageInfo(operation) {
            let currentPage = 0;
            let pageSize = 0;
            let orderType = 0;
            let isAsc = true;
            if (operation == Operation.INIT) {
                currentPage = 1;
                pageSize = 5;
            } else if (operation == Operation.SHIELD) {
                currentPage = this.shieldCurrentPage;
                pageSize = this.shieldPageSize;
                orderType = this.shieldOrderType;
                isAsc = this.shieldIsAsc;
            } else if (operation == Operation.COMMEND) {
                currentPage = this.priorityCurrentPage;
                pageSize = this.priorityPageSize;
                orderType = this.priorityOrderType;
                isAsc = this.priorityIsAsc;
            }
            getRules(this.$route.params.id, currentPage, pageSize, operation, orderType, isAsc).then((res) => {
                let data = res.data;
                if (operation == Operation.INIT) {
                    this.shieldData = data.shieldRules.tableData;
                    this.totleShieldRules = data.shieldRules.countAll;
                    this.currentPriorityData = data.priorityRules.tableData;
                    this.priorityDataLength = data.priorityRules.countAll;
                    this.frequency = data.duplicateRemoval;

                } else if (operation == Operation.SHIELD) {
                    this.shieldData = data.shieldRules.tableData;
                    this.totleShieldRules = data.shieldRules.countAll;
                } else if (operation == Operation.COMMEND) {
                    this.currentPriorityData = data.priorityRules.tableData;
                    this.priorityDataLength = data.priorityRules.countAll;
                }

            }).catch(function () {

            });

        },

        prioritySortChange: function (column) {
            let prop = column.prop;
            let order = column.order;
            switch (prop) {
                case "itemId":
                    this.priorityOrderType = 3;
                    break;
                case "createTime":
                    this.priorityOrderType = 1;
                    break;
                case "priorityWeight":
                    this.priorityOrderType = 2;
                    break;
                default:
                    this.priorityOrderType = 0;
            }
            console.log(order)
            if (order == "descending") {
                this.priorityIsAsc = false;
            } else if (order == "ascending") {
                this.priorityIsAsc = true;
            }
            this.getCurrentPageInfo(Operation.COMMEND)
        },

        shieldSortChange: function (column) {
            let prop = column.prop;
            let order = column.order;
            switch (prop) {
                case "itemId":
                    this.shieldOrderType = 3;
                    break;
                case "createTime":
                    this.shieldOrderType = 1;
                    break;
                case "priorityWeight":
                    this.shieldOrderType = 2;
                    break;
                default:
                    this.shieldOrderType = 0;
            }
            if (order == "descending") {
                this.shieldIsAsc = false;
            } else if (order == "ascending") {
                this.shieldIsAsc = true;
            }
            this.getCurrentPageInfo(Operation.SHIELD)
        },
        handleDelete(operation, index, rows, data) {
            let id = rows.id;
            if (operation == Operation.SHIELD) {
                this.deleteShieldButtonLoading = true;
                deleteShiedRule(id,rows.sceneId).then((res) => {
                    if (res.data.match("成功")) {
                        this.deleteShieldButtonLoading = false;
                        data.splice(index, 1);
                        this.getCurrentPageInfo(operation);
                    }
                }).catch((error) => {
                    this.deleteShieldButtonLoading = false;
                    this.errorNotify(error.response.data.msg);
                });
            } else {
                this.deletePriorityButtonLoading = true;
                deletePriorityRule(id,rows.sceneId).then((res) => {
                    if (res.data.match("成功")) {
                        this.deletePriorityButtonLoading = false;
                        data.splice(index, 1);
                        this.getCurrentPageInfo(operation);
                    }
                }).catch((error) => {
                    this.deletePriorityButtonLoading = false;
                    this.errorNotify(error.response.data.msg);
                });
            }
        },
        handleUpdateWeight() {
            updatePriorityScore(this.priorityCurrentId, this.priorityWeightForm.weight).then((res) => {
                this.priorityWeightVisible = false;
                this.getCurrentPageInfo(Operation.COMMEND)
                this.successNotify("修改推荐规则优先级成功");
            }).catch(error => {
                this.priorityWeightVisible = false;
                this.errorNotify(error.response.data.msg);
            });
        },

        handleShieldSizeChange: function (size) {
            this.shieldPageSize = size;
            this.getCurrentPageInfo(Operation.SHIELD)
        },

        handleShieldCurrentChange: function (currentPage) {
            this.shieldCurrentPage = currentPage;
            this.getCurrentPageInfo(Operation.SHIELD);
        },

        handlePrioritySizeChange: function (size) {
            this.priorityPageSize = size;
            this.getCurrentPageInfo(Operation.COMMEND)
        },
        handlePriorityCurrentChange: function (currentPage) {
            this.priorityCurrentPage = currentPage;
            this.getCurrentPageInfo(Operation.COMMEND);
        },

        showShieldDialog: function () {
            this.dialogShieldVisible = true
            this.shieldForm.name = ""
            this.shieldForm.id = ""
        },
        showPriorityDialog: function () {
            this.dialogPriorityVisible = true
            this.priorityForm.name = ""
            this.priorityForm.id = ""
        },
        showPriorityWeight: function (row) {
            this.priorityWeightForm.weight = row.priorityWeight
            this.priorityWeightVisible = true
            this.priorityForm.name = ""
            this.priorityCurrentId = row.id
            // this.handleUpdateWeight(row.id);
        },
        showDeleteConfirm: function (operation, index, rows, data) {
            this.$confirm('此操作将永久删除该规则, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.handleDelete(operation, index, rows, data);
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },
        hideDialog: function () {
            this.dialogShieldVisible = false
            this.dialogPriorityVisible = false
            this.priorityWeightVisible = false
        },
        submitForm: function (operation) {
            let itemId;
            if (operation === Operation.SHIELD) {
                this.addShieldButtonLoading = true;
                if (!this.shieldForm.id) {
                    this.errorNotify("媒资数据不得为空！")
                    return
                }
                itemId = this.shieldForm.id;
                addShiedRule(this.$route.params.id, itemId).then((res) => {
                    this.addShieldButtonLoading = false;
                    if (response.data.code == 200) {
                        this.successNotify("添加屏蔽规则成功");
                        this.getCurrentPageInfo(operation)
                    }
                }).catch(error => {
                    this.addShieldButtonLoading = false;
                    this.errorNotify(error.response.data.msg);
                });
            } else if (operation === Operation.COMMEND) {
                this.addPriorityButtonLoading = true;
                if (!this.priorityForm.id) {
                    this.errorNotify("媒资数据不得为空！")
                    return
                }
                itemId = this.priorityForm.id;
                //axios请求
                 addPriorityRule(this.$route.params.id, itemId).then(response => {
                    this.addPriorityButtonLoading = false;
                    if (response.data.code == 200) {
                        this.successNotify("添加推荐规则成功");
                        this.getCurrentPageInfo(operation)
                    }
                }).catch(error => {
                    this.addPriorityButtonLoading = false;
                    this.errorNotify(error.response.data.msg);
                });
            } else if (operation == Operation.DUMPLICATION) {
                this.editPeriodButtonLoading = true;
                this.$ajax({
                    method: 'put',
                    url: 'rule/duplicateRemovalRule',
                    data: this.$qs.stringify({
                        sceneId: this.$route.params.id,
                        duplicatePeriod: this.frequency,
                    })
                }).then(response => {
                    this.editPeriodButtonLoading = false;
                    console.log(response.data);
                    if (response.data.match("成功")) {
                        this.successNotify("修改去重周期成功");
                    }
                }).catch(error => {
                    this.editPeriodButtonLoading = false;
                    this.errorNotify("修改去重周期失败(请联系管理员)");
                });
            } else {
                this.errorNotify("类型有误！")
                return
            }

            this.hideDialog()
        },
        errorNotify(message) {
            this.$notify.error({
                title: '错误',
                message: message
            });
        },
        successNotify(message) {
            this.$notify.success({
                title: '成功',
                message: message
            });
        }
    }
}
</script>

<style scoped>

</style>
