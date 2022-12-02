import axios from 'axios';
import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
    LOGOUT_SUCCESS,
    LOGOUT_FAIL,
} from './types';

export const checkAuthenticated = () => async dispatch => {
    if (localStorage.getItem('access')) {
        dispatch({
            type: AUTHENTICATED_SUCCESS
        });
    } else {
        dispatch({
            type: AUTHENTICATED_FAIL
        });
    }
};

export const login = (username, password) => async dispatch => {
    if (!localStorage.getItem('access')) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const body = {
            "username": username,
            "password": password
        }
        // console.log(body)
        try {
            const res = await axios.post(`http://localhost:8000/users/login/`, body, config);
            console.log(res.data)
            dispatch({
                type: LOGIN_SUCCESS,
                payload: res.data
            });
        
        } catch (err) {
            console.log('Fail')
            dispatch({
                type: LOGIN_FAIL
            })
        }
    } else {
        dispatch({
            type: LOGIN_FAIL
        });
    }
};

export const logout = () => async dispatch => {
    console.log('HI')
    if (localStorage.getItem('access')) {
        const config = {
            headers: {
                'Authorization': `Token ${localStorage.getItem('access')}`,
            }
        };
        console.log('HI')
        try {
            const res = await axios.post(`http://localhost:8000/users/logout/`, {}, config);

            dispatch({
                type: LOGOUT_SUCCESS
            });

        } catch (err) {
            console.log('Fail')
            dispatch({
                type: LOGOUT_FAIL
            });
        }
    } else {
        dispatch({
            type: LOGOUT_FAIL
        });
    }
};
