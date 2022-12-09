import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    SIGNUP_SUCCESS,
    SIGNUP_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
    LOGOUT_SUCCESS,
    LOGOUT_FAIL,
} from '../actions/types';

const initialState = {
    access: localStorage.getItem('access'),
    isAuthenticated: null,
    user: null
};

export default function func(state = initialState, action) {
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
        case AUTHENTICATED_SUCCESS:
            return {
                ...state,
                isAuthenticated: true,
            }
        case AUTHENTICATED_FAIL:
            return {
                ...state,
                isAuthenticated: false,
            }
        case LOGOUT_SUCCESS:
            localStorage.removeItem('access');
            return {
                ...state,
                access: null,
                isAuthenticated: false,
                user: null
            }
        case LOGOUT_FAIL:
            return {
                ...state,
            }
        case SIGNUP_SUCCESS:
            return {
                ...state,
                isAuthenticated: false,
            }
        case SIGNUP_FAIL:
            return {
                ...state,
                isAuthenticated: false,
            }
        default:
            return state
    }
};
