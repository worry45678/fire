import axios from '@/libs/api.request'

export const getTableData = () => {
  return axios.request({
    url: 'get_table_data',
    method: 'get'
  })
}

export const getDragList = () => {
  return axios.request({
    url: 'get_drag_list',
    method: 'get'
  })
}

export const errorReq = () => {
  return axios.request({
    url: 'error_url',
    method: 'post'
  })
}

export const saveErrorLogger = info => {
  return axios.request({
    url: 'save_error_logger',
    data: info,
    method: 'post'
  })
}

export const uploadImg = formData => {
  return axios.request({
    url: 'image/upload',
    data: formData
  })
}

export const getOrgData = () => {
  return axios.request({
    url: 'get_org_data',
    method: 'get'
  })
}

export const getTreeSelectData = () => {
  return axios.request({
    url: 'get_tree_select_data',
    method: 'get'
  })
}

// 获取设备列表
export const getDevicesList = () => {
  return axios.request({
    url: 'devices',
    method: 'get'
  })
}

// 删除设备
export const deleteDevice = (params) => {
  return axios.request({
    url: 'devices',
    method: 'delete',
    params: params
  })
}

// 添加设备
export const addDevice = (params) => {
  return axios.request({
    url: 'devices',
    method: 'put',
    data: params
  })
}

