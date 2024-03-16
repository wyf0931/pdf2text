import React, { useEffect, useState } from 'react'
import PdfJs from '../../components/pdfPreview'
import pdf from './Javascript.pdf'
import CustomizedUpload from '../../components/mui/customizedUpload'
import { Stack, Box, OutlinedInput, Typography } from '@mui/material'
// import { useState } from 'react'
import TextField from '@mui/material/TextField'
import { useDispatch } from 'react-redux'
// import axios from 'axios'
import { setFile } from '@/store/slices/uploadSlice'
import { useNavigate } from 'react-router'

const Home = (props) => {
  // const { pdf } = props
  const dispatch = useDispatch()
  const [pageData, setPageData] = useState([])
  const [currentPage, setCurrentPage] = useState(0)
  const [url, setUrl] = useState('')
  const navigate = useNavigate()
  const handleUploadSuccess = (data) => {
    setPageData(data)
  }

  const handleClickNext = (currentPage) => {
    setCurrentPage(currentPage - 1)
  }

  useEffect(() => {}, [])

  const handleSetFileObjectURL = (url) => {
    setUrl(url)
  }
  const handleFileChange = (file) => {
    // dispatch(setFile(file))
    // todo 文件变化之后，跳转到pdfToText页面， file作为参数传递过去
    navigate('/pdfToText', {
      state: { file: file },
    })
  }
  return (
    <Stack
      sx={{
        justifyContent: 'center',
        // alignItems: 'center',
      }}
    >
      <Box
        sx={{
          // border: '5px solid red',
          width: '100%',
          marginTop: '200px',
        }}
      >
        <Box
          sx={{
            // height: '50px',
            // border: '2px solid blue',
            width: '100%',
          }}
        >
          <Typography
            variant="h1"
            sx={{
              margin: '0px',
              fontFamily: '"Source Sans Pro", Helvetica, Arial, sans-serif',
              webkitFontSmoothing: 'antialiased',
              fontWeight: 700,
              color: ' rgb(26, 26, 26)',
              textAlign: 'center',
              marginBottom: '20px',
            }}
          >
            Convert PDF to TEXT
          </Typography>
        </Box>
        <Box
          sx={{
            maxWidth: '1200px',
            width: '100%',
            // border: '5px solid green',
            margin: ' 0 auto',
          }}
        >
          <CustomizedUpload
            onSetFileObjectURL={handleSetFileObjectURL}
            onUploadSuccess={handleUploadSuccess}
            onFileChange={handleFileChange}
          />
        </Box>
      </Box>
    </Stack>
  )
}

export default Home
