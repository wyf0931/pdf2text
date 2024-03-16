import './App.css'

import { useEffect, useState } from 'react'

import { ThemeProvider } from '@mui/material/styles'
import { createTheme } from './themes'
import Home from './page/home'
import GlobalRouter from './router/index'

function App() {
  return (
    <ThemeProvider theme={createTheme()}>
      {/* <Home /> */}

      <GlobalRouter></GlobalRouter>
    </ThemeProvider>
  )
}

export default App
