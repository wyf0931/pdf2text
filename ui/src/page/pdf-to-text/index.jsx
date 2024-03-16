import React, { useEffect, useState } from 'react'
import PdfJs from '../../components/pdfPreview'
import pdf from './Javascript.pdf'
import { Stack, Box, OutlinedInput, Typography, Button } from '@mui/material'
import TextField from '@mui/material/TextField'
import { useLocation } from 'react-router-dom'

import LinearProgress from '@mui/material/LinearProgress'

function LinearProgressWithLabel(props) {
  const { status } = props

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        width: '300px',
      }}
    >
      <Box sx={{ width: '100%', mr: 1 }}>
        <LinearProgress variant="determinate" {...props} />
      </Box>
      <Box sx={{ width: '150px' }}>
        <Typography variant="body2" color="text.secondary">
          {`${Math.round(props.value)}%`} {status ? `(${status})` : ''}
        </Typography>
      </Box>
    </Box>
  )
}

const PdfToText = (props) => {
  // const { pdf } = props
  const [pageData, setPageData] = useState([])
  const [currentPage, setCurrentPage] = useState(0)
  const [url, setUrl] = useState('')
  const location = useLocation()
  const [progress, setProgress] = useState(0)
  const [file, setFile] = useState({})
  const [status, setStatus] = useState('')
  // 0 上传成功， 5 转换中  10 已完成

  const handleClickNext = (currentPage) => {
    if (currentPage <= pageData.length) {
      setCurrentPage(currentPage - 1)
    }
  }

  const handleClickPre = (currentPage) => {
    if (currentPage >= 1) {
      setCurrentPage(currentPage - 1)
    }
  }

  useEffect(() => {}, [])

  const handleSetFileObjectURL = (file) => {
    setUrl(URL.createObjectURL(file))
  }

  const uploadFile = async (file) => {
    // return
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/task/create', {
        method: 'POST',
        body: formData,
      })

      const responseData = await response.json()

      const { hash, code } = responseData
      if (code === 0) {
        window.clearInterval(window.timer)
        getProgress(hash)
      }
      // Handle success response here if needed
    } catch (error) {
      console.error('Error uploading file:', error)
      // Handle error here
    }
  }

  const getProgress = (hash) => {
    const timer = setInterval(async () => {
      try {
        const progressResponse = await fetch(`/api/task/info?id=${hash}`)
        if (!progressResponse.ok) {
          throw new Error('Failed to fetch upload progress')
        }
        const progressData = await progressResponse.json()
        console.log('Upload progress:=================', progressData)
        const { progress, pages, status } = progressData
        setProgress(progress)
        if (pages && pages.length) {
          setPageData(pages)
        }

        if (status === 0) {
          setStatus('上传成功')
        } else if (status === 5) {
          setStatus('处理中')
        } else {
          setStatus('已完成')
        }
        if (progress === 100) {
          window.clearInterval(window.timer)
        }

        // Check if upload is complete
        if (progressData.status === 'completed') {
          clearInterval(timer) // Stop timer if upload is complete
        }
      } catch (error) {
        console.error('Error fetching upload progress:', error)
        clearInterval(timer) // Stop timer on error
      }
    }, 2000) // Adjust interval as needed
    window.timer = timer
  }

  useEffect(() => {
    if (location.state && location.state.file) {
      const _file = location.state.file
      handleSetFileObjectURL(_file)
      setFile(() => {
        uploadFile(_file)
        setFile(_file)
      }, 10)
    }
  }, [location])

  return (
    <Stack
      sx={{
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Stack
        direction="row"
        sx={{
          // border: '1px solid red',
          justifyContent: 'space-between',
          alignItems: 'center',
          width: '100%',
          maxWidth: '1000px',
          margin: '0 auto',
          height: '50px',
          marginTop: '50px',
          padding: '0 80px',
          borderBottom: '1px solid #e4e4e4',
        }}
      >
        <Typography>{file && file.name}</Typography>

        <Box>
          <LinearProgressWithLabel value={progress} status={status} />
        </Box>
      </Stack>

      <Stack direction="row">
        <Box
          sx={{
            // border: '1px solid red',
            width: '500px',
            paddingTop: '20px',
          }}
        >
          <PdfJs prfUrl={url} onNext={handleClickNext} onPre={handleClickPre} />
        </Box>

        <Box
          sx={{
            border: '1px solid #e4e4e4',
            margin: '0 10px 0 20px',
          }}
        ></Box>

        <Box
          sx={{
            width: '500px',
            padding: '0 100px 0 20px',
            lineHeight: '24px',
            height: '1000px',
            overflowY: 'auto',
            overflowX: 'hidden',
          }}
        >
          <pre>
            {pageData[currentPage] ? pageData[currentPage].page_content : null}
          </pre>
        </Box>
      </Stack>
    </Stack>
  )
}

export default PdfToText
