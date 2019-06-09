<template>
  <div>
    <Row class="margin-top-10">
      <DatePicker v-model="searchDate" type="date" placeholder="Select date" style="width: 200px"></DatePicker>
      <Select v-model="selectResult" style="width:200px" clearable>
        <Option v-for="item in resultList" :value="item.value" :key="item.value">{{ item.label }}</Option>
      </Select>
      <Select v-model="selectDevice" style="width:200px" clearable>
        <Option v-for="item in deviceList" :value="item._id" :key="item._id">{{ item.name }}</Option>
      </Select>
      <Button @click="submit" icon="md-search" type="primary" clearable>查询</Button>
      <Table :columns="tableTitle" :data="tableData" :loading="tableLoading"></Table>
    </Row>
  </div>
</template>

<script>
import { getCheckLog, getDevicesList } from "@/api/data";
export default {
  name: "checklog",
  data() {
    return {
      searchDate: null,
      tableData: [],
      deviceList: [],
      selectResult: null,
      selectDevice: null,
      tableLoading: false,
      tableTitle: [
        {
          title: "检查时间",
          key: "date"
        },
        {
          title: "设备名称",
          key: "device_name"
        },
        {
          title: "检查结果",
          key: "result"
        },
        {
          title: "巡检人员",
          key: "user"
        },
        {
          title: "检查情况",
          key: "content"
        }
      ],
      resultList: [
        {
          label: "正常",
          value: 1
        },
        {
          label: "过期",
          value: 2
        },
        {
          label: "损坏",
          value: 3
        }
      ]
    };
  },
  methods: {
    fetchData() {
      let params = {
        device: this.selectDevice,
        date: this.searchDate,
        result: this.selectResult
      }
      getCheckLog(params).then(res => {
        this.tableData = res.data.data;
      });
    },
    submit() {
      this.fetchData();
    }
  },
  mounted() {
    this.fetchData();
    getDevicesList().then(res => {
      this.deviceList = res.data.data;
    });
  }
};
</script>
