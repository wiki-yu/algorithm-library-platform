<template>
  <div>
    <Row :gutter="20">
      <i-col :xs="12" :md="8" :lg="6" v-for="(infor, i) in inforCardData" :key="`infor-${i}`" style="height: 120px;padding-bottom: 10px;">
        <infor-card shadow :color="infor.color" :icon="infor.icon" :icon-size="36">
          <count-to :end="infor.count" count-class="count-style"/>
          <p>{{ infor.title }}</p>
        </infor-card>
      </i-col>
    </Row>
    <Row :gutter="20" style="margin-top: 10px;">
        <i-col :md="24" :lg="12" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="barData" text="Classification Distribution"/>
        </Card>
      </i-col>
      <i-col :md="24" :lg="12" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie style="height: 300px;" :value="pieData" text="Lean Classification"></chart-pie>
        </Card>
      </i-col>
    </Row>
    <Row>
      <Card shadow>
        <example style="height: 310px;"/>
      </Card>
    </Row>
  </div>
</template>

<script>
import InforCard from '_c/info-card'
import CountTo from '_c/count-to'
import { ChartPie, ChartBar } from '_c/charts'
import Example from './example.vue'
export default {
  name: 'home',
  components: {
    InforCard,
    CountTo,
    ChartPie,
    ChartBar,
    Example
  },
  data () {
    return {
      inforCardData: [
        { title: 'User Number', icon: 'md-person-add', count: 21, color: '#2d8cf0' },
        { title: 'Annotations', icon: 'md-locate', count: 232, color: '#19be6b' },
        { title: 'Revenue', icon: 'md-help-circle', count: 14200, color: '#ff9900' },
        { title: 'Videos', icon: 'md-share', count: 57, color: '#ed3f14' },
      ],
      pieData: [
        { value: 335, name: 'VA' },
        { value: 310, name: 'NVA' },
        { value: 234, name: 'RNVA' }
      ],
      barData: {
        'Unit Pick-Up/Transfer': 1170,
        'Operation': 7280,
        'Material Setup/Handling': 0,
        'Fixture Setup/Handling': 1080,
        'Inspection': 470,
        'Tool Setup/Handling': 0,
        'Operation Trash': 0,
        'Scanning': 0,
        'Cleaning': 0
      }
    }
  },
  mounted () {
    //
  }
}
</script>

<style lang="less">
.count-style{
  font-size: 50px
}
</style>