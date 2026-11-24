var app = require('express')()
const path = require('path')
var http = require('http').createServer(app)
var io = require('socket.io')(http)

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname, './index.html'))
})

io.on('connection', function (socket) {
  console.log('a user connected')

  // 广播给所有客户端，不包括自己这个 socket
  socket.broadcast.emit('hi')

  // 广播给所有客户端，包括自己这个 socket
  io.emit('message', '服务端想对你说...')

  // socket.emit('消息类型',数据) 给单个 socket 发消息，非广播

  socket.on('chat message', function (msg) {
    console.log('message: ' + msg)
    io.emit('chat message', `服务端说：${msg}`)
  })

  socket.on('disconnect', function () {
    console.log('user disconnected')
  })
})

http.listen(3000, function () {
  console.log('listening on *:3000')
})
