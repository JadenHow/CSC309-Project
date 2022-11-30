import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
} from '../actions/types';

const initialState = {
    access: localStorage.getItem('access'),
    isAuthenticated: null,
    user: null
};

export default function (state = initialState, action) {
    const { type, payload } = action;

    switch (type) {
        case LOGIN_SUCCESS:
            localStorage.setItem('access', payload.token)
            return {
                ...state,
                access: localStorage.getItem('access'),
                isAuthenticated: true,
                user: payload.user_data
            }
        case LOGIN_FAIL:
            localStorage.removeItem('access');
            return {
                ...state,
                access: null,
                isAuthenticated: false,
                user: null
            }
        default:
            return state
    }
};
