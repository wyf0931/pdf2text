import React, { PureComponent, useEffect, useState } from 'react'
import { Box, Stack } from '@mui/material'
import 'react-pdf/dist/Page/AnnotationLayer.css'
import 'react-pdf/dist/Page/TextLayer.css'
import { Document, Page, pdfjs } from 'react-pdf'

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`

const PdfJs = (props) => {
  const { prfUrl, onNext, onPre } = props

  const [pageNum, setPageNum] = useState(1)
  const [pageNumberInput, setPageNumberInput] = useState(1)
  const [pageNumFocus, setPageNumFocus] = useState(false)
  const [pageWidth, setPageWidth] = useState(503)
  const [fullscreen, setFullscreen] = useState(false)
  const [totalPage, setTotalPage] = useState(1)
  // const [totalPage, setNumPages] = useState(0)

  const handleClickPre = () => {
    if (pageNum === 1) {
      return
    }
    setPageNum(pageNum - 1)
    onPre && onPre(pageNum - 1)
  }
  const handleClickNext = () => {
    if (pageNum === totalPage) {
      return
    }
    setPageNum(pageNum + 1)
    onNext && onNext(pageNum + 1)
  }

  const pageZoomOut = () => {
    if (pageWidth <= 503) {
      return
    }
    const _pageWidth = pageWidth * 0.8
    setPageWidth(_pageWidth)
  }

  const pageZoomIn = () => {
    const _pageWidth = pageWidth * 1.2
    setPageWidth(_pageWidth)
  }

  const pageFullscreen = () => {
    if (fullscreen) {
      this.setState({ fullscreen: false, pageWidth: 600 })
      setFullscreen(false)
      setPageWidth(600)
    } else {
      setFullscreen(true)
      setPageWidth(window.screen.width - 40)
    }
  }

  const toPage = (e) => {
    if (e.keyCode === 13) {
      setPageNum(e.target.value * 1)
    }
  }

  const onDocumentLoadSuccess = (pageInfo) => {
    const { numPages } = pageInfo
    console.log('log==pageInfo============>>', pageInfo)
    setTotalPage(numPages)
  }

  useEffect(() => {
    console.log('log==prfUrl======1======>>', prfUrl)
  }, [prfUrl])

  return (
    <Stack
      sx={{
        position: 'relative',
        // border: '1px solid red',
        height: '1000px',
        justifyContent: 'flex-start',
      }}
    >
      <Box
        sx={{
          height: '830px',
          // border: '1px solid red',
        }}
      >
        <Document
          onLoadSuccess={onDocumentLoadSuccess}
          file={prfUrl}
          loading={'加载中...'}
        >
          <Page pageNumber={pageNum} width={pageWidth} loading={'加载中...'} />
        </Document>
      </Box>

      <Stack
        direction="row"
        sx={{
          alignItems: 'center',
          background: 'rgb(168, 168, 168)',
          color: 'white',
          borderRadius: '10px',
          height: '50px',
          // border: '1px solid red',
          marginTop: '20px',
          justifyContent: 'center',
        }}
      >
        <div className="page-tool-item" onClick={handleClickPre}>
          上一页
        </div>{' '}
        <div className="input">
          {/* <input type="number" onKeyDown={toPage} />  */}
          {pageNum} /{totalPage}
        </div>
        <div className="page-tool-item" onClick={handleClickNext}>
          下一页
        </div>
        {/* <div className="page-tool-item" onClick={pageZoomIn}>
          放大
        </div>
        <div className="page-tool-item" onClick={pageZoomOut}>
          缩小
        </div> */}
      </Stack>
    </Stack>
  )
}

export default PdfJs
