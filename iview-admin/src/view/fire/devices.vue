<template>
  <div>
    <Row class="margin-top-10">
      <Button @click="modal = true" size="large" icon="ios-add" type="primary">添加设备</Button>
      <Table :columns="tableTitle" :data="tableData" :loading="tableLoading"></Table>
      <Modal v-model="modal" :mask-closable="false" title="添加消防设备" @on-ok="submit" @on-cancel="cancel">
        <Form :model="form" :label-width="80">
          <FormItem label="设备名称">
            <Input v-model="form.name" placeholder="Enter something..."/>
          </FormItem>
          <FormItem label="设备类型">
            <Select v-model="form.type">
              <Option value="消火栓">消火栓</Option>
              <Option value="灭火器">灭火器</Option>
            </Select>
          </FormItem>
          <FormItem label="安装日期">
            <DatePicker v-model="form.date" type="date" placeholder="Select date"></DatePicker>
          </FormItem>
          <FormItem label="巡检周期">
            <Slider v-model="form.period" :min="1" :max="10" :step="1"></Slider>
          </FormItem>
          <FormItem label="设备地址">
            <Input v-model="form.address" placeholder="Enter something..."/>
          </FormItem>
          <FormItem label="设备坐标">
            <Input v-model="form.x" placeholder="X坐标"/>
            <Input v-model="form.y" placeholder="Y坐标"/>
          </FormItem>
        </Form>
      </Modal>
    </Row>
  </div>
</template>

<script>
import { getDevicesList, deleteDevice, addDevice } from "@/api/data";
export default {
  name: "devices",
  data() {
    return {
      modal: false,
      form: {
        name: '',
        address: '',
        date: '',
        x: '',
        y: '',
        type: '',
        period: 1
      },
      tableLoading: false,
      tableData: [],
      tableTitle: [
        {
          title: "设备名称",
          key: "name"
        },
        {
          title: "Address",
          key: "address"
        },
        {
          title: "检查周期",
          key: "period"
        },
        {
          title: "设备类型",
          key: "type"
        },
        {
          title: "坐标",
          key: "axis",
          render: (h, params) => {
            return h("div", [h("strong", `${params.row.x}, ${params.row.y}`)]);
          }
        },

        {
          title: "Action",
          key: "action",
          width: 150,
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.editDevice(params.row);
                    }
                  }
                },
                "编辑"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "error",
                    size: "small"
                  },
                  on: {
                    click: () => {
                      this.$Modal.confirm({
                        title: "Title",
                        content:
                          "<p>Content of dialog</p><p>Content of dialog</p>",
                        onOk: () => {
                          this.deleteDevice(params.row._id);
                        },
                        onCancel: () => {
                          this.$Message.info("Clicked cancel");
                        }
                      });
                    }
                  }
                },
                "删除"
              )
            ]);
          }
        }
      ]
    };
  },
  methods: {
    fetchData() {
      getDevicesList().then(res => {
        this.tableData = res.data.data;
      });
    },
    deleteDevice(i) {
      console.log(i);
      let params = { _id: i };
      deleteDevice(params).then(res => {
        this.fetchData();
        this.$Message.info("删除成功");
      });
    },
    addDevice() {
      console.log(this.form);
      addDevice(this.form).then(res => {
        this.form = {}
        this.$Message.info(res.data)
        this.fetchData()
      })
    },
    editDevice(data) {
      this.modal = true
      this.form.name = data.name
      this.form.address = data.address
      this.form.date = data.date
      this.form.type = data.type
      this.form.period = data.period
      this.form.x = data.x
      this.form.y = data.y
    },
    submit() {
      this.addDevice()
    },
    cancel() {
      this.form = {}
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>
