import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
// import axios from 'axios'
// import localStorage from '@/utils/localStorage'

export const REDUCER_KEY = 'upload'

// 获取部门树数据
export const getSystemData = createAsyncThunk(
  `${REDUCER_KEY}/getSystemData`,
  async () => {
    const res = await fetch(`/api/setting`)
    return res
  },
)

export const uploadSlice = createSlice({
  name: REDUCER_KEY,
  initialState: {
    file: '',
  },
  reducers: {
    setFile: (state, data) => {
      const { payload } = data
      console.log('Log========>>>', data)
      // state.file = payload
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getSystemData.fulfilled, (state, result) => {
        const { payload } = result

        const menuList = payload.data.modules.map((item) => {
          const p = `/${item.name}`
          localStorage.setItem(p, item)

          return {
            ...item,
            path: p,
            title: item.label,
          }
        })
        localStorage.setItem('menuList', menuList)
        localStorage.setItem('systemName', payload.data.systemName)
        state.systemName = payload.data.systemName
      })
      .addCase(getSystemData.rejected, (state) => {
        state.loading = false
      })
      .addCase(getSystemData.pending, (state) => {
        state.loading = true
      })
  },
})

export const { setFile, file } = uploadSlice.actions

export default uploadSlice.reducer
