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

<script>
import { defineComponent } from 'vue';
import CommentList from './components/CommentList.vue';
import CommentForm from './components/CommentForm.vue';
import { getCommentList } from './api.js';
import axios from './axiosService';
// import { AxiosError, AxiosResponse } from 'axios';

export default defineComponent({
    name: 'Comment',
    components: {
        CommentList,
        CommentForm,
    },
    props: {
        contentType: String,
        objectPk: String,
        token: String,
        numComments: Number,
        numCommentParticipants: Number,
    },
    data() {
        return {
            value: '',
            commentList: null,
            loading: false,
            next: null,
        };
    },
    computed: {
        isAuthenticated() {
            return this.token && this.token.length !== 0;
        },
        hasMore() {
            return this.next !== null;
        },
    },
    mounted() {
        getCommentList(this.contentType, this.objectPk)
            .then((response) => {
                this.commentList = response.data.results;
                this.next = response.data.next;
                this.$nextTick(() => {
                    this.scrollToCommentByHash();
                });
            })
            .catch((err) => {
                // Todo: handle errors
                console.log(err.response);
            });
    },
    methods: {
        commentSuccess(c) {
            c.descendants = [];
            this.commentList && this.commentList.unshift(c);
            this.value = '';
        },
        loadMore() {
            this.loading = !this.loading;
            axios
                .get(this.next)
                .then((response) => {
                    this.commentList && this.commentList.push(...response.data.results);
                    this.next = response.data.next;
                    this.loading = !this.loading;
                })
                .catch((err) => {
                    console.log(err.response);
                    this.loading = !this.loading;
                });
        },
        scrollToCommentByHash() {
            let hash = window.location.hash;
            if (hash === '') {
                return;
            }
            let eleId = hash.substring(1);
            let ele = window.document.getElementById(eleId);
            ele && ele.scrollIntoView();
        },
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
