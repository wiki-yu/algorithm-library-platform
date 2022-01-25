<template>
    <div ref="dom"></div>
</template>

<script>
import echarts from 'echarts'
import { on, off } from '@/libs/tools'
export default {
  name: 'serviceRequests',
  data () {
    return {
      dom: null
    }
  },
  methods: {
    resize () {
      this.dom.resize()
    }
  },
  mounted () {
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      title : {
        text:"Recent Video Analysis",
        // subtext:"test",
        x:'center'
      },
      // legend :{

      // },
      grid: {
        top: '3%',
        left: '1.2%',
        right: '1%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: ['Video 1', 'Video 2', 'Video 3', 'Video 4', 'Video 5', 'Video 6', 'Video 7']
        }
      ],
      yAxis: [
        {
          type: 'value'
        }
      ],
      series: [
        {
          name: 'Motion 1',
          type: 'line',
          stack: '总量',
          areaStyle: { normal: {
            color: '#2d8cf0'
          } },
          data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
          name: 'Motion 2',
          type: 'line',
          stack: '总量',
          areaStyle: { normal: {
            color: '#10A6FF'
          } },
          data: [257, 358, 278, 234, 290, 330, 310]
        },
        {
          name: 'Motion 3',
          type: 'line',
          stack: '总量',
          areaStyle: { normal: {
            color: '#0C17A6'
          } },
          data: [379, 268, 354, 269, 310, 478, 358]
        },
        {
          name: 'Motion 4',
          type: 'line',
          stack: '总量',
          areaStyle: { normal: {
            color: '#4608A6'
          } },
          data: [320, 332, 301, 334, 390, 330, 320]
        },
        {
          name: 'Motion 5',
          type: 'line',
          stack: '总量',
          label: {
            normal: {
              show: true,
              position: 'top'
            }
          },
          areaStyle: { normal: {
            color: '#398DBF'
          } },
          data: [820, 645, 546, 745, 872, 624, 258]
        }
      ]
    }
    this.$nextTick(() => {
      this.dom = echarts.init(this.$refs.dom)
      this.dom.setOption(option)
      on(window, 'resize', this.resize)
    })
  },
  beforeDestroy () {
    off(window, 'resize', this.resize)
  }
}
</script>
