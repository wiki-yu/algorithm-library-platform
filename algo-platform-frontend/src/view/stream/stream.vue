<template>
  <div>
    <div class="stream-section">
      <Row :gutter="20" style="margin-top: 10px;" type="flex">
        <i-col :md="24" :lg="24" style="margin-bottom: 10px;">
          <Card shadow>
            <p slot="title" class="card-title">
              <Icon type="logo-youtube" size:="20"/> Camera Live Stream
            </p>
            <div class="cam-form">
              <img
                src="http://localhost:5000/streaming"
                alt="Loading Video Failed"
              />
            </div>
            <p class="title-description">
              Support Type: <span class="badge badge-success">H.264 (MP4)</span>
            </p>
          </Card>
        </i-col>
      </Row>
    </div>

    <Row :gutter="20" style="margin-top: 10px;" type="flex">
      <i-col :md="24" :lg="24" style="margin-bottom: 10px;">
        <Card shadow>
          <p slot="title" class="card-title">
            <Icon type="md-aperture" size="18" />
            Record Video
          </p>

          <!-- <b-form @submit="onSubmit" @reset="onReset" v-if="show"> -->
          <b-form>
            <Button
              class="form-btn"
              type="primary"
              :loading="recording"
              icon="ios-power"
              @click="startRecord"
            >
              <span v-if="!recording">Record</span>
              <span v-else>Recording...</span>
            </Button>
            <Button
              class="form-btn"
              type="error"
              @click="stopRecord"
              :disabled="!recording"
              >Stop</Button
            >
            <Button class="form-btn" type="warning" @click="resetInfo"
              >Reset</Button
            >

            <div class="video-info-input">
              <b-form-group
                id="input-group-1"
                label="Start Time:"
                label-for="input-1"
                v-if="tableShow"
              >
                <b-form-input
                  id="input-1"
                  v-model="form.start"
                  required
                  placeholder="Enter start time"
                ></b-form-input>
              </b-form-group>

              <b-form-group
                id="input-group-2"
                label="End Time:"
                label-for="input-2"
                v-if="tableShow"
              >
                <b-form-input
                  id="input-2"
                  v-model="form.end"
                  required
                  placeholder="Enter end time"
                ></b-form-input>
              </b-form-group>
              <b-form-group
                id="input-group-3"
                label="Video Name:"
                label-for="input-3"
              >
                <b-form-input
                  id="input-3"
                  v-model="form.videoName"
                  required
                  placeholder="Enter the video name"
                ></b-form-input>
              </b-form-group>
            </div>
          </b-form>
        </Card>
      </i-col>
    </Row>

    <Row :gutter="20" style="margin-top: 10px;" type="flex">
      <i-col :md="24" :lg="24" style="margin-bottom: 10px;">
        <Card shadow>
          <p slot="title" class="card-title">
            <Icon type="logo-buffer" size:="20"/> Video Records
          </p>
          <Table
            :columns="Tablecolumns"
            :data="tableData"
            :loading="tableLoading"
          ></Table>
          <Button
            class="form-btn"
            type="success"
            ghost
            icon="md-download"
            :loading="exportLoading"
            @click="exportExcel"
            >Export File</Button
          >
          <Button
            class="form-btn"
            type="warning"
            ghost
            icon="ios-cloud-done"
            @click="saveDatabase"
            >Save to Database</Button
          >
        </Card>
      </i-col>
    </Row>
  </div>
</template>

<script>
import axios from "axios"
import { WebCam } from "vue-web-cam";
import excel from "@/libs/excel";
import { startRecording, stopRecording, saveVideoInfo } from "@/api/video";
export default {
  name: "App",
  components: {
    "vue-web-cam": WebCam
  },
  data() {
    return {
      recording: false,
      controlForm: {
        startRecord: true,
        stopRecord: false,
        videoName: ""
      },
      form: {
        start: "",
        end: "",
        videoName: ""
      },
      tableShow: false,
      tableData: [],
      col1: [],
      col2: [],
      col3: [],
      tableLoading: false,
      exportLoading: false,
      timeBegin: new Date(),
      timeEnd: new Date(),

      Tablecolumns: [
        {
          title: "Start Time",
          key: "start"
        },
        {
          title: "End Time",
          key: "end"
        },
        {
          title: "Video Name",
          key: "videoName"
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
                      this.viewItem(params.index);
                    }
                  }
                },
                "View"
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
                      this.remove(params.index);
                    }
                  }
                },
                "Delete"
              )
            ]);
          }
        }
      ]
    };
  },

  methods: {
    fillTable: function() {
      this.tableData.push({
        start: this.col1,
        end: this.col2,
        videoName: this.col3
      });
    },

    startRecord() {
      this.recording = true;
      var newDate = new Date();
      var datetime =
        newDate.getMonth() +
        1 +
        "-" +
        newDate.getDate() +
        "-" +
        newDate.getFullYear() +
        "-" +
        newDate.getHours() +
        ":" +
        newDate.getMinutes() +
        ":" +
        newDate.getSeconds();
      var saveVideoName =
        newDate.getMonth() +
        1 +
        "-" +
        newDate.getDate() +
        "-" +
        newDate.getFullYear() +
        "-" +
        newDate.getHours() +
        "@" +
        newDate.getMinutes() +
        "@" +
        newDate.getSeconds() +
        ".mp4";
      console.log(saveVideoName);
      this.form.start = datetime;
      this.form.videoName = saveVideoName;
      this.controlForm.videoName = saveVideoName;
      console.log(this.controlForm);
      this.timeBegin = newDate;

      // startRecording(this.controlForm).then(() => {
      //   this.$Message.success("Start Recording...");
      // });
      axios.post("http://localhost:5000/startRecord", this.controlForm)
        .then(res => {
          console.log(res.data);
        })
        .catch(err => {
          console.log(err);
        });
    },

    stopRecord() {
      console.log(this.controlForm);
      console.log(this.controlForm);
      var newDate = new Date();
      this.timeEnd = newDate;
      var timeDiff = (this.timeEnd.getTime() - this.timeBegin.getTime()) / 1000;
      console.log("time diff: ", timeDiff);
      var datetime =
        newDate.getMonth() +
        1 +
        "-" +
        newDate.getDate() +
        "-" +
        newDate.getFullYear() +
        "-" +
        newDate.getHours() +
        ":" +
        newDate.getMinutes() +
        ":" +
        newDate.getSeconds();
      console.log(datetime);
      this.form.end = datetime;
      this.col1 = this.form.start;
      this.col2 = this.form.end;
      this.col3 = this.form.videoName;
      if (timeDiff < 10) {
        this.$Message.error("Please record at least 10 seconds!");
      } else if (timeDiff > 1800) {
        this.$Message.error("Recording exceed 30 minutes!");
      } else {
        this.recording = false;
        this.fillTable();
        this.form.videoName = "";
        stopRecording(this.controlForm).then(() => {
          this.$Message.success("Stopped Recording");
        })
      }
    },

    resetInfo() {
      this.form.start = "";
      this.form.end = "";
      this.form.videoName = "";
      // this.show = false
    },

    viewItem(index) {
      this.$Modal.info({
        title: "Annotation Info",
        content: `Start: ${this.tableData[index].start}<br>End：${this.tableData[index].end}<br>Name：${this.tableData[index].videoName}`
      })
    },
    remove(index) {
      this.tableData.splice(index, 1);
    },

    exportExcel() {
      if (this.tableData.length) {
        this.exportLoading = true;
        const params = {
          title: ["Start Time", "End Time", "Name"],
          key: ["start", "end", "videoName"],
          data: this.tableData,
          autoWidth: true,
          filename: "Video Records"
        };
        excel.export_array_to_excel(params);
        this.exportLoading = false;
      } else {
        this.$Message.info("Excel table cannot be empty!");
      }
    },

    saveDatabase() {
      if (this.tableData.length == 0) {
        this.$Message.error("Nothing in the table yet!");
      } else {
        console.log(this.tableData);
        saveVideoInfo(this.tableData)
          .then(() => {
            this.$Message.success("Info Saved");
          })
          .catch(err => {
            this.$Notice.warning({
              title: "Uploading failed",
              desc: "Upload file failed. Details: " + err.response.data.error
            });
          });

        this.tableData = [];
      }
    }
  }
}
</script>

<style scoped>
.cam-form {
  display: flex;
  justify-content: center;
  background-color: #000000;
}
.form-btn {
  margin: 3px 1px 1px 3px;
  margin-top: 10px;
}
.video-info-input {
  margin-top: 15px;
}
.title-description {
  justify-content: center;
}
</style>