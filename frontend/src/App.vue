<template>
  <div>
    <comment-form v-if="isAuthenticated"
                  :content-type="contentType"
                  :object-pk="objectPk"
                  :token="token"
                  flag="global"
                  @globalCommentSuccess="commentSuccessed"/>
    <comment-list
            :content-type="contentType"
            :object-pk="objectPk"
            :token="token"
            :comment-list="commentList"
            :num-comments="numComments"
            :num-comment-participants="numCommentParticipants">
    </comment-list>
    <div class="flex-center top-gap-big" v-if="hasMore">
      <a class="text-small text-muted" href="" @click.prevent="loadMore" v-if="!loading">加载更多 <i
              class="remixicon-arrow-down-s-line"></i></a>
      <span class="text-small text-muted" v-else>加载中...</span>
    </div>
  </div>
</template>

<script>
    import CommentForm from "./components/CommentForm.vue";
    import CommentList from "./components/CommentList.vue";
    import LoginPanel from "./components/LoginPanel.vue";
    import {getCommentList} from './api.js'
    import axios from './axiosService'

    export default {
        components: {CommentList, CommentForm, LoginPanel},
        props: {
            contentType: String,
            objectPk: String,
            token: String,
            weiboLoginUrl: String,
            githubLoginUrl: String,
            numComments: Number,
            numCommentParticipants: Number,
        },
        data() {
            return {
                value: '',
                commentList: null,
                loading: false,
                next: null
            }
        },
        computed: {
            isAuthenticated() {
                return this.token.length !== 0
            },
            hasMore() {
                return this.next !== null
            }
        },
        mounted() {
            getCommentList(this.contentType, this.objectPk).then(response => {
                this.commentList = response.data.results
                this.next = response.data.next
                this.$nextTick(() => {
                    this.scrollToCommentByHash()
                })
            }).catch(err => {
                console.log(err.response)
            })
        },
        methods: {
            commentSuccessed(payload) {
                payload.descendants = []
                this.commentList.unshift(payload)
                this.value = ''
            },
            loadMore() {
                this.loading = !this.loading
                axios.get(this.next).then(response => {
                    console.log(response.data);
                    this.commentList.push(...response.data.results)
                    this.next = response.data.next
                    this.loading = !this.loading
                }).catch(err => {
                    console.log(err.response)
                    this.loading = !this.loading
                })
            },
            scrollToCommentByHash() {
                let hash = window.location.hash
                let eleId = hash.substring(1)
                let ele = window.document.getElementById(eleId)
                ele.scrollIntoView()
            }
        }
    }
</script>
<style lang="css">
</style>