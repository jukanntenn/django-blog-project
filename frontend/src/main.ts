// Must import the processed file from dist instead of src
import 'mobi.css/dist/mobi.css';
import './style/colorful.css';
import './styles.scss';

import BackTop from './scripts/backtop';
import Offcanvas from '@/scripts/offcanvas';
import './scripts/search';
import './scripts/toc';
import Comment from './CommentApp.vue';
import { createApp } from 'vue';

// @ts-ignore
const {contentType, objectPk, token,numComments, numCommentParticipants} = jscontext

createApp(Comment, {
    contentType,
    objectPk,
    token,
    numComments,
    numCommentParticipants,
}).mount('#comment_app');


export default { BackTop, Offcanvas };
