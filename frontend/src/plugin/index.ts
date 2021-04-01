import 'mobi.css';
import '../styles.scss';

import { App } from 'vue';
// import type { SFCWithInstall } from '@element-plus/utils/types'
import Comment from '../Comment.vue';

Comment.install = (app: App): void => {
    app.component(Comment.name, Comment);
};

// const _Table: SFCWithInstall<typeof Table> = Table

export default Comment;
