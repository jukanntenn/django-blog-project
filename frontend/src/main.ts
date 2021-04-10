import 'mobi.css';
import './styles.scss';

import BackTop from './scripts/backtop';
import Comment from './Comment.vue';
import { createApp } from 'vue';

createApp(Comment).mount('#comments_app');

export default { BackTop };
