import 'mobi.css';
import './styles.scss';

import BackTop from './scripts/backtop';
import SideBar from "@/scripts/sidebar";
import Comment from './Comment.vue';
import { createApp } from 'vue';

createApp(Comment).mount('#comments_app');

export default { BackTop, SideBar };
