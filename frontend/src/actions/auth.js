import axios from 'axios';
import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
} from './types';

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
        console.log(body)
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