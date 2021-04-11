import axios from './axiosService';

export function getCommentSecurityData(contentType, objectPk) {
    return axios.get('/comments/security-data/', {
        params: {
            content_type: contentType,
            object_pk: objectPk,
        },
    });
}

export function getCommentList(contentType, objectPk) {
    return axios.get('/comments/', {
        params: {
            content_type: contentType,
            object_pk: objectPk,
        },
    });
}

export function postComment(token, data) {
    return axios.post('/comments/', data, {
        headers: {
            Authorization: 'Token ' + token,
        },
    });
}
