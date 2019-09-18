<template>
  <div class="flex-left comment" :id="commentItemAnchor">
    <div class="unit-0 comment-mugshot-box">
      <img class="comment-mugshot" alt="" :src="comment.user.mugshot"/>
    </div>
    <div class="unit root-comment">
      <header class="comment-user">
        <span class="text-small text-muted comment-user-name">{{comment.user.name}}
            <span class="master" v-if="comment.user.name==='追梦人物'">[博主]</span>
        </span>
        <template v-if="!isRoot">
          <i class="remixicon-share-forward-fill"></i>
          <span class="text-small text-muted comment-user-name">{{comment.parent_user.name}}
            <span class="master" v-if="comment.parent_user.name==='追梦人物'">[博主]</span>
          </span>
        </template>
      </header>

      <div v-html="comment.comment" class="comment-body">
        {{comment.comment}}
      </div>

      <footer class="comment-footer flex-left">
        <time class="text-small text-muted comment-date">{{comment.submit_date}}</time>
        <a href="#" class="text-small text-muted btn-reply" @click.prevent="replying=!replying" v-if="isAuthenticated">回复</a>
      </footer>
      <comment-form @rootCommentSuccess="rootCommentSuccessed"
                    @descendantCommentSuccess="descendantCommentSuccess"
                    :flag="commentFormFlag"
                    v-if="replying"
                    :content-type="contentType"
                    :object-pk="objectPk"
                    :token="token"
                    :parent="comment.id"/>
      <div class="comment-descendants" v-if="hasChildren">
        <comment-item v-for="c in comment.descendants" @descendantCommentSuccess="descendantCommentSuccessed"
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
            descendants: {
                type: Array,
                required: false
            },
            token: String
        },
        data() {
            return {
                'replying': false
            }
        },
        methods: {
            rootCommentSuccessed(payload) {
                this.comment.descendants.push(payload)
                this.replying = !this.replying
            },
            descendantCommentSuccess(payload) {
                this.replying = !this.replying
                this.$emit('descendantCommentSuccess', payload)
            },
            descendantCommentSuccessed(payload) {
                this.comment.descendants.push(payload)
            }
        },

        computed: {
            commentFormFlag() {
                return this.isRoot ? 'root' : 'descendant'
            },

            hasChildren() {
                return this.isRoot && this.comment.hasOwnProperty('descendants') && this.comment.descendants.length > 0
            },
            isRoot() {
                return this.comment.parent === null
            },
            isAuthenticated() {
                return this.token.length !== 0
            },
            commentItemAnchor() {
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

  .comment-mugshot-box {
    flex-shrink: 0;
  }

  .comment .comment-mugshot {
    width: 48px;
    border-radius: 3px;
    margin-right: 1rem;
  }

  .comment-descendants .comment {
    margin-top: 2rem;
  }

  .comment-descendants .comment .comment-mugshot {
    width: 32px;
  }

  .comment-footer .btn-reply {
    margin-left: 0.8rem;
  }

  @media (max-width: 768px) {
    .comment .comment-mugshot {
      width: 32px;
    }

    .comment-descendants .comment .comment-mugshot {
      width: 24px;
    }
  }

</style>