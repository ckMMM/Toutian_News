<template>
  <van-popup
    :value="value"
    @input="$emit('input',$event)"
    position="bottom"
    :style="{ height: '95%' }"
    class="channels"
  >
    <div>
      <div class="channel-head">
        <div>
          <span class="title">我的频道</span>
          <span class="desc">点击进入频道</span>
        </div>
        <div>
          <van-button type="danger" @click="isEdit = !isEdit" plain size="mini">{{isEdit ? '完成' : '编辑'}}</van-button>
        </div>
      </div>
      <div class="channel-content">
        <van-grid :gutter="10" clickable>
          <van-grid-item v-for="(channelItem,index) in channels" @click="handleUserChannelClick(channelItem,index)" :key="channelItem.id">
            <span
              class="text"
              :class="{active:index === activeIndex && !isEdit}"
            >{{channelItem.name}}</span>
            <van-icon class="close-icon" v-show="isEdit" name="close"></van-icon>
          </van-grid-item>
        </van-grid>
      </div>
    </div>

    <!-- 推荐频道 -->
    <div class="channel">
      <div class="channel-head">
        <div>
          <span class="title">频道推荐</span>
          <span class="desc">点击添加频道</span>
        </div>
      </div>
      <van-grid class="channel-content" :gutter="10" clickable>
        <van-grid-item @click="handleChannelAdd(item)" v-for="item in recommendChannels" :key="item.id">
          <div class="info">
            <span class="text">{{item.name}}</span>
          </div>
        </van-grid-item>
      </van-grid>
    </div>
  </van-popup>
</template>

<script>
import { getAllChannels, deleteUserChannel, resetUserChannels } from '@/api/channel'
import { mapState } from 'vuex'

export default {
  name: 'HomeChannel',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    channels: {
      type: Array,
      default: () => []
    },
    activeIndex: {
      type: Number,
      default: 0
    }
  },
  data () {
    return {
      allChannels: [], // 所有频道
      isEdit: false // 是否编辑
    }
  },
  created () {
    this.getAllChannels()
  },
  computed: {
    recommendChannels () {
      const duplicates = this.channels.map(item => item.id)

      return this.allChannels.filter(item => !duplicates.includes(item.id))
    },
    ...mapState(['user'])
  },
  methods: {
    async getAllChannels () {
      const data = await getAllChannels()
      data.channels.forEach(item => {
        item.articles = [] // 用来存储当前的文章列表
        item.timestamp = Date.now() // 存储下一页数据的时间戳
        item.downPullLoading = false // 控制当前频道的下拉刷新 loading 状态
        item.upPullLoading = false // 控制当前频道的上拉加载更多的 loading 状态
        item.upPullFinished = false // 控制当前频道数据是否加载完毕
      })
      this.allChannels = data.channels
    },
    // 添加频道
    async handleChannelAdd (item) {
      this.channels.push(item)

      if (this.user) { // 登录了
        // 如果用户已登录，则将数据添加到后端
        const data = this.channels.slice(1).map((item, index) => {
          return {
            id: item.id, // 频道id
            seq: index + 2
          }
        })

        await resetUserChannels(data)
        return
      }

      // 未登录
      window.localStorage.setItem('channels', JSON.stringify(this.channels))
    },
    // 更改频道
    changeChannel (item, index) {
      this.$emit('update:active-index', index)

      this.$emit('input', false)
    },
    // 删除频道
    async deleteChannel (item, index) {
      this.channels.splice(index, 1)

      // 手动的设置一下当前激活的标签索引，用来触发那个 onLoad 调用，否则可能会看不到那个数据
      // this.$emit('update:active-index',1)
      // 判断当前激活频道中是否有数据，如果没有则手动的 onLoad 一下
      if (this.user) { // 登录了，发请求给后台
        await deleteUserChannel(item.id)
        return
      }

      // 未登录
      window.localStorage.setItem('channels', JSON.stringify(this.channels))
    },
    // 点击用户频道
    handleUserChannelClick (item, index) {
      if (this.isEdit) { // 正在编辑中
        this.deleteChannel(item, index)
      } else { // 未正在编辑中
        this.changeChannel(item, index)
      }
    }
  }
}
</script>

<style lang="less">
.channels {
  .channel-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    .title {
      font-size: 30px;
      margin-right: 5px;
    }
    .desc {
      font-size: 12px;
    }
  }
  .channel-content {
    .text {
      font-size: 20px;
    }
    .active {
      color: red;
    }
    .close-icon {
      font-size: 30px;
      position: absolute;
      top: -5px;
      right: -5px;
      z-index: 999;
      background-color: #fff;
    }
    .info {
      display: flex;
      align-items: center;
    }
  }
}
</style>
