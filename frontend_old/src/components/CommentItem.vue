<template>
  <div class="flex-left comment" :id="commentAnchor">
    <div class="unit-0 comment-avatar-box">
      <img class="comment-avatar" alt="" :src="comment.user.avatar_url"/>
    </div>
    <div class="unit root-comment">
      <header class="comment-user">
        <span class="text-small text-muted comment-user-name">{{comment.user.name}}
            <span class="master" v-if="comment.user.name==='追梦人物'">[博主]</span>
        </span>
        <template v-if="!isRoot">
          <i class="ri-share-forward-fill"></i>
          <span class="text-small text-muted comment-user-name">{{comment.parent_user.name}}
            <span class="master" v-if="comment.parent_user.name==='追梦人物'">[博主]</span>
          </span>
        </template>
      </header>

      <div v-html="comment.comment_html" class="comment-body">
        {{comment.comment_html}}
      </div>

      <footer class="comment-footer flex-left">
        <time class="text-small text-muted comment-date">{{comment.submit_date}}</time>
        <a href="#" class="text-small text-muted btn-reply" @click.prevent="replying=!replying" v-if="isAuthenticated">回复</a>
      </footer>
      <comment-form @descendantCommentSuccess="commentSuccess"
                    :flag="commentFormFlag"
                    v-if="replying"
                    :content-type="contentType"
                    :object-pk="objectPk"
                    :token="token"
                    :parent="comment.id"/>
      <div class="comment-descendants" v-if="hasDescendants">
        <comment-item v-for="c in comment.descendants"
                      :content-type="contentType"
                      :object-pk="objectPk"
                      :token="token"
                      :comment="c"
                      :key="c.id"/>
      </div>
    </div>
  </div>
</template>

<script>
    import CommentForm from "./CommentForm.vue";

    export default {
        name: 'comment-item',
        components: {CommentForm},
        props: {
            comment: Object,
            contentType: String,
            objectPk: String,
            token: String
        },
        data() {
            return {
                'replying': false
            }
        },
        methods: {
            commentSuccess(c) {
                this.replying = !this.replying
                if (this.isRoot) {
                    this.comment.descendants.push(c)
                    return
                }
                // Vue 不提倡子组件中修改父组件的状态，
                // 但是为了简单起见，且在无副作用的情况下，这里直接修改父组件的状态
                this.$parent.comment.descendants.push(c)
            },
        },

        computed: {
            commentFormFlag() {
                return 'descendant'
            },

            hasDescendants() {
                return this.isRoot && this.comment.descendants.length > 0
            },
            isRoot() {
                return this.comment.parent === null
            },
            isAuthenticated() {
                return this.token.length !== 0
            },
            commentAnchor() {
                return 'c' + this.comment.id
            }
        },
    }
</script>

<style lang="css">
  .comment {
    margin-top: 3rem;
  }

  .root-comment {
    width: 0; /* 防止 flex 子元素宽度超出父元素 https://www.cnblogs.com/Red-ButterFly/p/8794286.html */
  }

  .comment-avatar-box {
    flex-shrink: 0;
  }

  .comment .comment-avatar {
    width: 48px;
    border-radius: 3px;
    margin-right: 1rem;
  }

  .comment-descendants .comment {
    margin-top: 2rem;
  }

  .comment-descendants .comment .comment-avatar {
    width: 32px;
  }

  .comment-footer .btn-reply {
    margin-left: 0.8rem;
  }

  @media (max-width: 768px) {
    .comment .comment-avatar {
      width: 32px;
    }

    .comment-descendants .comment .comment-avatar {
      width: 24px;
    }
  }

</style>