import './styles.scss';
// 无法引入，报错！！
// import 'mavon-editor/dist/css/index.css'
import './script/toc.js'
import './script/backtop.js'
import './script/donate.js'
import './script/search.js'
import './script/sidebar.js'

import "bourbon";
import Vue from 'vue'
import App from './App.vue'
import mavonEditor from 'mavon-editor'

Vue.use(mavonEditor)


new Vue({
    el: '#comments_app',
    render: h => h(App, {
            props: {
                contentType: jscontext.contentType,
                objectPk: jscontext.objectPk,
                token: jscontext.token,
                numComments: jscontext.numComments,
                numCommentParticipants: jscontext.numCommentParticipants,
            }
        }
    )
})
