import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';

const EditUser = ({ isAuthenticated }) => {
    const params = useParams();
    const[formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        avatar: ''
    });
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });


    return (
        <div>
            <h1>Edit User</h1>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group'>
                    <input
                        className='form-control'
                        type='text'
                        name='username'
                        value={username}
                        onChange={e => onChange(e)}
                    />
                    <input
                        className='form-control'
                        type='password'
                        name='password'
                        value={password}
                        onChange={e => onChange(e)}
                    />
                    <input
                        className='form-control'
                        type='email'
                        name='email'
                        value={email}
                        onChange={e => onChange(e)}
                    />
                    <input
                        className='form-control'
                        type='text'
                        name='first_name'
                        value={first_name}
                        onChange={e => onChange(e)}
                    />
                    <input
                        className='form-control'
                        type='text'
                        name='last_name'
                        value={last_name}
                        onChange={e => onChange(e)}
                    />
                    <input
                        className='form-control'
                        type='image'
                        name='avatar'
                        value={avatar}
                        onChange={e => onChange(e)}
                    />
                </div>
                <button className='btn btn-primary' type='submit'>Save</button>
            </form>
        </div>
    )
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default EditUser(mapStateToProps);