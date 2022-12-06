import React, { useState } from 'react';
// import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
// import App from '../App';

const EditUser = ({ isAuthenticated }) => {
    const[formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        avatar: ''
    });

    const { username, password, email, first_name, last_name, phone_number, avatar } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();

        fetch(this.props.formAction, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData),
            method: 'POST'
        });

        e.setFormData({
            username: '',
            password: '',
            email: '',
            first_name: '',
            last_name: '',
            phone_number: '',
            avatar: ''
        });
    };

    return (
        <div>
            <h1>Edit User</h1>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group'>
                    <div>
                        <input
                            className='form-control'
                            type='text'
                            name='username'
                            value={username}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div>
                        <input
                            className='form-control'
                            type='password'
                            name='password'
                            value={password}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div>
                        <input
                            className='form-control'
                            type='email'
                            name='email'
                            value={email}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div>
                        <input
                            className='form-control'
                            type='text'
                            name='first_name'
                            value={first_name}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div>
                        <input
                            className='form-control'
                            type='text'
                            name='last_name'
                            value={last_name}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div>
                        <input
                            className='form-control'
                            type='image'
                            name='avatar'
                            value={avatar}
                            onChange={e => onChange(e)}
                        />
                    </div>
                </div>
                <button className='btn btn-primary' type='submit'>Save</button>
            </form>
        </div>
    )
};
// https://stackoverflow.com/questions/39153545/how-to-do-post-in-form-submit-using-reactjs-and-pass-the-object-value-into-rest
const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});


export default connect(mapStateToProps)(EditUser); //(mapStateToProps);