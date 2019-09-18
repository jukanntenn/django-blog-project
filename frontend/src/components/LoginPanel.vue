<template>
  <div class="flex-center top-gap login-panel p-7">
    <div>
      <div class="text-muted text-center login-header"><span>登录后回复</span></div>
      <div class="flex-center text-center social-icons mt-3">
        <span class="weibo mr-3"><a href="weiboLoginUrl"><i class="fab fa-weibo"></i></a></span>
        <span class="github"><a href="githubLoginUrl"><i class="fab fa-github"></i></a>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
    import {getCommentList} from '../api.js'
    import CommentItem from "./CommentItem.vue";

    export default {
        name: 'comment-list',
        components: {CommentItem},
        props: {
            contentType: String,
            objectPk: String,
            weiboLoginUrl: String,
            githubLoginUrl: String
        },
        data() {
            return {
                commentList: null
            }
        },
        mounted() {
            getCommentList(this.contentType, this.objectPk).then(response => {
                this.commentList = response.data.results
            }).catch(err => {
                console.log(err.response)
            })
        }
    }
</script>