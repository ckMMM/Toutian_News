<template>
  <div class="home">
    <van-nav-bar title="首页" fixed />
    <van-tabs class="channel-tabs" v-model="activeChannelIndex">
      <div slot="nav-right" class="wap-nav" @click="isChannelShow = true">
        <van-icon name="wap-nav" />
      </div>
      <van-tab :key="channelItem.id" :title="channelItem.name" v-for="channelItem in channels">
        <van-pull-refresh
          v-model="channelItem.downPullLoading"
          :success-text="channelItem.downPullSuccessText"
          :success-duration="1000"
          @refresh="onRefresh"
        >
          <van-list
            v-model="channelItem.upPullLoading"
            :finished="channelItem.upPullFinished"
            finished-text="没有更多了"
            @load="onLoad"
          >
            <van-cell
              v-for="articleItem in channelItem.articles"
              :key="articleItem.art_id"
              :title="articleItem.title"
            />
          </van-list>
        </van-pull-refresh>
      </van-tab>
    </van-tabs>
    <!-- 频道管理组件
      v-model 实际上是
         v-bind:value = "数据"
         v-on:input = "数据 = $event"
    -->
    <!-- <HomeChannel v-model="isChannelShow" :channels="channels" :activeIndex="activeChannelIndex" /> -->
    <!-- <HomeChannel v-model="isChannelShow" :channels="channels" :activeIndex="activeChannelIndex" @update:active-index="activeChannelIndex = $event"/> -->
    <!-- 上面的简写 -->
    <HomeChannel v-model="isChannelShow" :channels="channels" :activeIndex.sync="activeChannelIndex"/>
    <!-- 说明 -->
    <!--
      :activeIndex.sync="activeChannelIndex" 相当于下面两句
        :activeIndex="activeChannelIndex"
        @update:active-index="activeChannelIndex = $event"

      当你给一个属性加上 .sync 修饰符的时候，它会自动监听
      @update:绑定的字段 = "绑定的字段 = $event"
      其中的事件名称的 update: 是固定语法
      所以你在你的子组件中发布自定义事件的时候务必要发送一个名字叫 update:绑定的字段 的事件
      参考文档：https://cn.vuejs.org/v2/guide/components-custom-events.html#sync-%E4%BF%AE%E9%A5%B0%E7%AC%A6
      说白了：props数据.sync 和 v-model 的作用是一样的，但是一个组件只能有一个v-model

      v-model是
        v-bind:value = "isChannelShow" 和
        @input = "isChannelShow = false" 的简写
     -->
  </div>
</template>

<script>
import { getUserChannels } from '@/api/channel'
import { getArticles } from '@/api/article'
import HomeChannel from '@/components/channel'
export default {
  name: 'HomeIndex',
  components: {
    HomeChannel
  },
  data () {
    return {
      activeChannelIndex: 0, // 激活的索引
      // list: [], // 数据列表
      // loading: false, // 加载中
      // finished: false, // 是否完成
      // isLoading: false, // 是否加载中
      channels: [], // 存储频道列表数据
      isChannelShow: false
    }
  },
  created () {
    this.loadChannels()
  },
  computed: {
    /**
     * 当前激活的频道对象
     */
    activeChannel () {
      return this.channels[this.activeChannelIndex]
    }
  },
  watch: {
    // 监视容器中的 user 用户
    // 记住：凡是能 this. 点出来的成员都可以直接在这里监视
    // 由于路由缓存了，所以这里监视用户的登录状态，如果登录了，则重新获取
    async '$store.state.user' () {
      // 重新加载用户频道列表
      this.loadChannels()

      // 频道数据改变，重新加载当前激活频道的数据
      this.activeChannel.upPullLoading = true
    },
    isChannelShow () {
      // 如果频道面板隐藏了，并且当前频道没有数据，那我们就手动的 onLoad 加载更多
      if (!this.isChannelShow && this.activeChannel.articles.length === 0) {
        this.onLoad()
      }
    }
  },
  methods: {
    async loadChannels () {
      const { user } = this.$store.state

      let channels = []
      if (user) {
        // 已登录
        const data = await getUserChannels()
        channels = data.channels
      } else {
        // 未登录
        const localChannels = window.localStorage.getItem('channels')
        if (localChannels) {
          // 本地频道数据
          channels = JSON.parse(localChannels)
        } else {
          const data = await getUserChannels()
          channels = data.channels
        }
      }

      // 修改 channels，将这个数据结构修改为满足我们使用的需求
      channels.forEach(item => {
        item.articles = [] // 用来存储当前的文章列表
        item.timestamp = Date.now() // 存储下一页数据的时间戳
        item.downPullLoading = false // 控制当前频道的下拉刷新 loading 状态
        item.upPullLoading = false // 控制当前频道的上拉加载更多的 loading 状态
        item.upPullFinished = false // 控制当前频道数据是否加载完毕
      })

      this.channels = channels
    },
    /**
     * 上拉加载更多 push 数据
     *  */
    async onLoad () {
      await this.$sleep(800)
      // 异步更新数据
      // setTimeout(() => {
      //   for (let i = 0; i < 10; i++) {
      //     this.list.push(this.list.length + 1)
      //   }
      //   // 加载状态结束
      //   this.loading = false

      //   // 数据全部加载完成
      //   if (this.list.length >= 40) {
      //     this.finished = true
      //   }
      // }, 1000)
      let data = []
      data = await this.loadArticles()

      // 如果没有 pre_timestamp 并且数组是空的，则意味着没有数据了
      if (!data.pre_timestamp && !data.results.length) {
        // 设置该频道数据已加载完毕，组件会自动给出提示，并且不再 onLoad
        this.activeChannel.upPullFinished = true

        // 取消 loading
        this.activeChannel.upPullLoading = false

        return
      }

      // pre_timestamp 下一页的页码(上次时间点推荐的数据)
      // results 文章列表

      // 解决初始化的时候没有最新推荐数据的问题（没有最新数据，那就加载下一次推荐数据）
      if (data.pre_timestamp && !data.results.length) {
        this.activeChannel.timestamp = data.pre_timestamp

        // 加载下一页数据
        data = await this.loadArticles()
      }

      // 数据加载好以后，将 pre_timestamp 更新到当前频道的中用于加载下下页数据
      this.activeChannel.pre_timestamp = data.pre_timestamp

      // 将文章数据更新到频道中(注意：是 push 追加 不是覆盖)
      this.activeChannel.articles.push(...data.results)

      // 数据加载完毕，取消上拉 loading
      this.activeChannel.upPullLoading = false
    },

    /**
     * 下拉刷新 如果有新数据，则是重置列表数据
     */
    async onRefresh () {
      // setTimeout(() => {
      //   this.isLoading = false
      // }, 3000)
      const { activeChannel } = this

      // 备份加载下一页数据的时间戳
      // const timestamp = activeChannel.timestamp

      activeChannel.timestamp = Date.now()
      const data = await this.loadArticles()

      // 如果有最新数据，将数据更新到频道的文章列表中
      if (data.results.length) {
        // 将当前最新的推荐内容重置到频道文章中
        activeChannel.articles = data.results

        // 由于你重置了文章列表，那么当前数据中的 pre-timestamp 就是上拉
        activeChannel.timestamp = data.pre_timestamp
        activeChannel.downPullSuccessText = '更新成功'

        // 当下拉刷新有数据并重置以后数据无法满足一屏，所以我们使用 onLoad
        this.onLoad()
      } else {
        // 如果没有最新数据，提示已是最新内容
        activeChannel.downPullSuccessText = '已是最新数据'
      }

      // 下拉刷新结束，取消 loading 状态
      activeChannel.downPullLoading = false
    },

    async loadArticles () {
      const { id: channelId, timestamp } = this.activeChannel

      const data = await getArticles({
        channelId, // 当前激活的频道id
        // channelId: 26, // 测试没有数据了
        // timestamp: Date.now(), // 时间戳，用于分页
        timestamp, // 当前频道下一页数据的时间戳
        withTop: 1 // 是否包含置顶数据
      })

      return data
    }
  }
}
</script>

<style lang="less" scoped>
.channel-tabs {
  margin-bottom: 100px;
  // .van-tabs__wrap{
  //   width: 100%;
  //   position: fixed;
  //   top: 92px;
  //   z-index: 2;
  // }
  // .van-tabs__content {
  //   // display: none;
  //   margin-top: 200px;
  // }
}
.channel-tabs /deep/ .van-tabs__wrap {
  position: fixed;
  z-index: 2;
  width: 100%;
  top: 92px;
}

.channel-tabs /deep/ .van-tabs__content {
  margin-top: 192px;
}

.channel-tabs /deep/ .wap-nav {
  position: fixed;
  right: 0;
}
</style>
