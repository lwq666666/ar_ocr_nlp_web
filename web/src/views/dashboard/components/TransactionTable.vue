<template>
    <el-table :data="list" style="width: 100%;padding-top: 15px;">
        <el-table-column label="媒资ID" min-width="200">
            <template slot-scope="scope">
                {{ scope.row.itemId }}
            </template>
        </el-table-column>
        <!--<el-table-column label="观影时长" width="195" align="center">-->
        <!--<template slot-scope="scope">-->
        <!--{{ scope.row.watchDuration }}分钟-->
        <!--</template>-->
        <!--</el-table-column>-->
        <el-table-column label="时间" width="195" align="center">
            <template slot-scope="scope">
                {{ rankDate | dateFilter}}
            </template>
        </el-table-column>
        <el-table-column label="观影时长" width="100" align="center">
            <template slot-scope="scope">
                <el-tag :type="scope.row.watchDuration | durationFilter"> {{ scope.row.watchDuration }}</el-tag>
            </template>
        </el-table-column>
    </el-table>
</template>

<script>
    import {fetchList} from '@/api/transaction'

    export default {
        props: ['columnId'],
        filters: {
            durationFilter(length) {
                const statusMap = {
                    success: 'success',
                    pending: 'danger'
                };
                if (length > 3000) {
                    return statusMap.success;
                }
                else {
                    return statusMap.pending;
                }
            },
            dateFilter(str) {
                return str.substring(0, 10)
            }
        },
        data() {
            return {
                list: null
            }
        },
        created() {
            this.fetchData()
        },
        methods: {
            fetchData() {
                let query = new Object();
                query.collumId = this.columnId;
                console.log(query);

                fetchList(query).then(response => {
                    this.list = JSON.parse(response.data).rank;
                    this.rankDate = JSON.parse(response.data).date;
                })
            },
        }
    }
</script>
