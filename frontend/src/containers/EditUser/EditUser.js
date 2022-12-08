import React, { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
// import axios from 'axios';
// import App from '../App';
import "./edituser.css";

const EditUser = ({ isAuthenticated }) => {
    const emptyState = {
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        avatar: '',
        creditcard: ''}
    const[formData, setFormData] = useState(emptyState);

    const { username, password, email, first_name, last_name, phone_number, avatar, creditcard } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async(e) => {
        e.preventDefault();
        console.log("submitted", formData);

        try {
            let response = await fetch(`http://localhost:8000/users/edit/`, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('access')}`
                },
                body: JSON.stringify(formData),
                method: 'PATCH'
            });
            console.log(response);
            if (response.status === 200) {
                console.log("success")
                setFormData(emptyState);
                //return <Navigate to='/profile/'/>;
                window.location.reload(false);
            } else {
                console.log("some error occurred")
            }
            //return <Navigate to='/edit'/>
        } catch (err) {
            console.log(err);
        }
        //console.log("button worked");
        setFormData('');
    };

    return (
        <div className='form'>
            <h1 className='title'>Edit User</h1>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group'>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='text'
                            name='username'
                            placeholder='username'
                            value={username}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='password'
                            name='password'
                            placeholder='password'
                            value={password}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='email'
                            name='email'
                            placeholder='email'
                            value={email}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='text'
                            name='first_name'
                            placeholder='first name'
                            value={first_name}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='text'
                            name='last_name'
                            placeholder='last name'
                            value={last_name}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='tel'
                            name='phone_number'
                            placeholder='phone number'
                            value={phone_number}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        Avatar:
                        <input
                            className='form-control'
                            type='file'
                            name='avatar'
                            placeholder='avatar'
                            alt='avatar'
                            value={avatar}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='number'
                            name='creditcard'
                            placeholder='credit card number'
                            alt='creditcard'
                            value={creditcard}
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