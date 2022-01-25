import axios from '@/libs/api.request'

export const uploadVideo = formData => {
  return axios.request({
    url: 'uploadVideo',
    method: 'post',
    data: formData
  })
}

export const uploadVideoWithProgress = (formData, onUploadProgress) => {
  return axios.request({
    url: 'uploadVideo',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    method: 'post',
    data: formData,
    onUploadProgress
  })
}

export const startRecording = formData => {
  return axios.request({
    url: 'startRecord',
    method: 'post',
    data: formData
  })
}

export const stopRecording = formData => {
  return axios.request({
    url: 'stopRecord',
    method: 'post',
    data: formData
  })
}

export const saveVideoInfo = formData => {
  return axios.request({
    url: 'saveVideoInfo',
    method: 'post',
    data: formData
  })
}

export const getOriVideoInfo = () => {
  return axios.request({
    url: 'getOriVideoInfo',
    method: 'get'
  })
}

export const getAnnoVideoInfo = () => {
  return axios.request({
    url: 'getAnnoVideoInfo',
    method: 'get'
  })
}

export const delVideo = formData => {
  return axios.request({
    url: 'delVideo',
    method: 'post',
    data: formData
  })
}
export const getAnnoNumber = () => {
  return axios.request({
    url: 'annoNumber',
    method: 'get'
  })
}

export const getVideoNumber = () => {
  return axios.request({
    url: 'videoNumber',
    method: 'get'
  })
}

export const getVideoSign = () => {
  return axios.request({
    url: 'videoSign',
    method: 'get'
  })
}

export const getBackgroundImage = formData => {
  return axios.request({
    url: 'backgroundImage',
    method: 'post',
    data: formData
  })
}