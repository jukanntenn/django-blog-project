<template>
    <div>
        <comment-form
            v-if="isAuthenticated"
            :content-type="contentType"
            :object-pk="objectPk"
            :token="token"
            flag="root"
            @rootCommentSuccess="commentSuccess"
        />
        <comment-list
            :content-type="contentType"
            :object-pk="objectPk"
            :token="token"
            :comment-list="commentList"
            :num-comments="numComments"
            :num-comment-participants="numCommentParticipants"
        />
        <div class="flex-center top-gap-big" v-if="hasMore">
            <a class="text-small text-muted" href="" @click.prevent="loadMore" v-if="!loading"
                >加载更多 <i class="ri-arrow-down-s-line"></i
            ></a>
            <span class="text-small text-muted" v-else>加载中...</span>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import CommentList from './components/CommentList.vue';
import CommentForm from './components/CommentForm.vue';

export default defineComponent({
    name: 'Comment',
    components: {
        CommentList,
        CommentForm,
    },
});
</script>

<style lang="scss">
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
