<template>
  <div>
    <div class='stream-section'>
      <Row :gutter='20' style='margin-top: 10px;' type='flex'>
        <i-col :md='24' :lg='24' style='margin-bottom: 10px;'>
          <Card shadow>
            <p slot='title' class='card-title'>
              <Icon type='logo-youtube' size:='20'/> Camera Live Stream
            </p>
            <div class='cam-form'>
              <img
                src='http://localhost:5000/streaming'
                alt='Loading Video Failed'
              />
            </div>
            <p class='title-description'>
              Support Type: <span class='badge badge-success'>H.264 (MP4)</span>
            </p>
          </Card>
        </i-col>
      </Row>
    </div>
  </div>
</template>

<script>
import { WebCam } from 'vue-web-cam'
export default {
  name: 'App',
  components: {
    'vue-web-cam': WebCam
  },
  data () {
    return {
    }
  },

  methods: {
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
