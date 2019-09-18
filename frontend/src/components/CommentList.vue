<template>
  <div>
    <h5>{{ numComments }} 条评论 / {{ numCommentParticipants }} 人参与</h5>
    <comment-item
            v-for="comment in commentList"
            :key="comment.id"
            :comment="comment"
            :content-type="contentType"
            :token="token"
            :object-pk="objectPk"/>
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
            token: String,
            commentList: Array,
            numComments: Number,
            numCommentParticipants: Number,
        },
    }
</script>