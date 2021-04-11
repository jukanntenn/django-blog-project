<template>
    <div class="flex-center comment-form">
        <div class="unit-1 form">
            <textarea
                v-model="value"
                placeholder="评论（支持 Markdown 语法）..."
                rows="5"
            ></textarea>
            <button class="btn btn-default float-right" @click="submitComment">
                <i class="ri-send-plane-fill" aria-hidden="true"></i> 发布
            </button>
        </div>
    </div>
</template>

<script>
import { getCommentSecurityData, postComment } from '../api.js';

export default {
    name: 'comment-form',
    props: {
        contentType: String,
        objectPk: String,
        token: String,
        parent: Number,
        flag: String,
    },
    data() {
        return {
            value: '',
            security_data: null,
        };
    },
    mounted() {
        getCommentSecurityData(this.contentType, this.objectPk)
            .then((response) => {
                this.security_data = response.data;
            })
            .catch((err) => {
                console.log(err.response);
            });
    },
    methods: {
        submitComment() {
            if (this.value.length === 0) {
                alert('请输入评论内容');
            }
            let token = this.token;
            let data = {
                comment: this.value,
                parent: this.parent,
                ...this.security_data,
            };
            postComment(token, data)
                .then((response) => {
                    this.$emit(this.flag + 'CommentSuccess', response.data);
                    this.value = '';
                })
                .catch((err) => {
                    console.log(err.response);
                });
        },
    },
};
</script>

<style lang="css" scoped>
.comment-form {
    margin-top: 1rem;
}

.v-note-wrapper {
    z-index: 1;
}
</style>
