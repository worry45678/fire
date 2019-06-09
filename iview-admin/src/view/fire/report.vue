<template>
  <div>
    <Row class="margin-top-10">
      <DatePicker type="month" v-model="searchDate" placeholder="Select month" style="width: 200px"></DatePicker>
      <Button @click="submit" icon="md-search" type="primary" clearable>查询</Button>
      <Table :columns="tableTitle" :data="tableData" :loading="tableLoading"></Table>
    </Row>
  </div>
</template>

<script>
import { getReport } from "@/api/data";
export default {
  name: "report",
  data() {
    const now = new Date()
    return {
      searchDate: now,
      tableLoading: false,
      tableData: [],
      tableTitle: [
        {
          title: '设备名称',
          key: 'name'
        },
        {
          title: '应检次数',
          key: '应检次数'
        },
        {
          title: '实检次数',
          key: '实检次数'
        },
        {
          title: '巡检率',
          key: '巡检率'
        }
      ]
    };
  },
  methods: {
    fetchData() {
      getReport({date: this.searchDate}).then(res => {
        this.tableData = res.data.data
        console.log(res.data)
      })
    },
    submit() {
      this.fetchData()
    }
  },
  mounted() {
    this.fetchData()
  }
};
</script>
