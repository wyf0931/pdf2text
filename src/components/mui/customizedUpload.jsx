import React, { useEffect, useState } from 'react'
import { styled, useTheme } from '@mui/material/styles'
import {
  Card,
  IconButton,
  Box,
  FormLabel,
  Typography,
  Stack,
  Button,
} from '@mui/material'
import AddIcon from '@mui/icons-material/Add'
import LinearProgress from '@mui/material/LinearProgress'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'

const Input = styled('input')({
  display: 'none',
})

const CustomizedUpload = (props) => {
  const { id = 'id', sx = {}, direction = 'column', onFileChange } = props
  // const [files, setFiles] = useState([])

  const handleUploadClick = async (event) => {
    const file = event.target.files[0]
    // setFiles([...files, file])
    onFileChange && onFileChange(file)
  }

  return (
    <Stack
      sx={{
        alignItems: direction === 'column' ? 'flex-start' : 'flex-end',
        maxWidth: '1200px',
        width: '100%',
        // border: '5px solid green',
      }}
      spacing={1}
      direction={direction}
    >
      <Box sx={{ width: '100%' }}>
        <FormLabel
          htmlFor={`upload-input-${id}`}
          sx={{
            display: 'block',
            width: '100%',
            ...sx,
          }}
        >
          <Stack
            sx={{
              width: '100%',
              height: '350px',
              alignItems: 'center',
              justifyContent: 'center',
              background: 'rgb(255, 183, 0)',
              padding: '10px',
              borderRadius: '10px',
            }}
          >
            <Stack
              sx={{
                width: '100%',
                height: '100%',
                borderRadius: '4px',
                justifyContent: 'center',
                alignItems: 'center',
                background: 'rgb(232, 167, 3)',
                border: '1px dashed #fff',
              }}
            >
              <Stack
                direction={'row'}
                spacing={'10px'}
                sx={{
                  width: '180px',
                  height: '54px',
                  background: '#fff',
                  borderRadius: '4px',
                  justifyContent: 'center',
                  alignItems: 'center',
                  cursor: 'pointer',

                  transition: '0.3',
                  ':hover': {
                    color: 'red',
                  },
                }}
              >
                <CloudUploadIcon /> <Typography>选择文件</Typography>
                {/* <VisuallyHiddenInput type="file" /> */}
              </Stack>
            </Stack>
          </Stack>
        </FormLabel>
      </Box>

      <Input
        accept="*"
        id={`upload-input-${id}`}
        type="file"
        onChange={handleUploadClick}
      />
    </Stack>
  )
}

export default CustomizedUpload
