import axios from 'axios';
import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    SIGNUP_SUCCESS,
    SIGNUP_FAIL,
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
            // console.log(res.data)
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
    if (localStorage.getItem('access')) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${localStorage.getItem('access')}`
            }
        };

        try {
            const res = await axios.post(`http://localhost:8000/users/logout/`, {}, config);
            dispatch({
                type: LOGOUT_SUCCESS,
                payload: res.data
            });

        } catch (err) {
            console.log('Fail')
            dispatch({
                type: LOGOUT_FAIL
            })
        }
    } else {
        dispatch({
            type: LOGOUT_FAIL
        });
    }
};

export const signup = (username, password, email, first_name, last_name, phone_number, credit_card_number) => async dispatch => {
    if (!localStorage.getItem('access')) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const body = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "credit_card_number": credit_card_number
        }

        try {
            const res = await axios.post(`http://localhost:8000/users/register/user/`, body, config);
            dispatch({
                type: SIGNUP_SUCCESS,
                payload: res.data
            });
        } catch (err) {
            // console.log(err.response.data)
            alert(err.response.data.username)
            dispatch({
                type: SIGNUP_FAIL
            })
        }
    } else {
        dispatch({
            type: SIGNUP_FAIL
        });
    }
};