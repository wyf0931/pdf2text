import { configureStore } from '@reduxjs/toolkit'
import uploadSlice from './slices/uploadSlice'

export const store = configureStore({
  reducer: {
    uploadSlice,
  },
})
