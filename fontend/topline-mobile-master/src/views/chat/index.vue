<template>
  <div>
    chat page
  </div>
</template>

<script>
import io from 'socket.io-client'
export default {
  name: 'ChatIndex',
  created () {
    const socket = io('http://ttapi.research.itcast.cn', {
      query: {
        token: this.$store.state.user.token
      }
    })

    socket.on('connect', () => {
      console.log('...连接成功啦...')

      // 连接成功了，就可以发送消息啦
      socket.emit('message', {
        msg: '666',
        timestamp: Date.now()
      })
    })

    socket.on('message', data => {
      console.log(`收到的消息是 `, data)
    })
  }
}
</script>
