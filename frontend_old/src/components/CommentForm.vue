<template>
  <div class="flex-center comment-form">
    <div class="unit-1">
      <mavon-editor v-model="value"
                    :boxShadow="false"
                    :subfield="true"
                    placeholder="评论..."
                    :autofocus="false"
                    :toolbars="this.toolbars"
      />
      <button class="btn btn-default float-right" @click="submitComment">
        <i class="ri-send-plane-fill" aria-hidden="true"></i> 发布
      </button>
    </div>
  </div>
</template>

<script>
    import {getCommentSecurityData, postComment} from '../api.js'

    export default {
        name: 'comment-form',
        props: {
            contentType: String,
            objectPk: String,
            token: String,
            parent: Number,
            flag: String
        },
        data() {
            return {
                value: '',
                toolbars: {
                    bold: true, // 粗体
                    italic: true, // 斜体
                    strikethrough: true, // 中划线
                    quote: true, // 引用
                    ol: true, // 有序列表
                    ul: true, // 无序列表
                    link: true, // 链接
                    // imagelink: true, // 图片链接
                    code: true, // code
                    preview: true, // 预览
                },
                security_data: null
            }
        },
        mounted() {
            getCommentSecurityData(this.contentType, this.objectPk).then(response => {
                this.security_data = response.data
            }).catch(err => {
                console.log(err.response)
            })
        },
        methods: {
            submitComment() {
                if (this.value.length === 0) {
                    alert("请输入评论内容")
                }
                let token = this.token
                let data = {
                    'comment': this.value,
                    'parent': this.parent,
                    ...this.security_data
                }
                postComment(token, data).then(response => {
                    this.$emit(this.flag + 'CommentSuccess', response.data)
                    this.value = ''
                }).catch(err => {
                    console.log(err.response)
                })
            }
        }
    }
</script>

<style lang="css" scoped>
  .comment-form {
    margin-top: 1rem;
  }

  .v-note-wrapper {
    z-index: 1;
  }
</style>