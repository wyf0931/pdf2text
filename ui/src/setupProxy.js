// 配置代理 - 用于联调
const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(
    createProxyMiddleware('/api', {
      target: 'http://www.pdfcvt.cn',
    }),
  )
}
