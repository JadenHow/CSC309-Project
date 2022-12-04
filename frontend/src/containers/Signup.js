import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { signup } from '../actions/auth';


const Signup = ({ signup, isAuthenticated }) => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        credit_card_number: ''
    });

    const { username, password, email, first_name, last_name, phone_number, credit_card_number } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();
        
        signup(username, password, email, first_name, last_name, phone_number, credit_card_number);
    };

    if (isAuthenticated) {
        return <Navigate to='/' />
    }

    return (
        <div className='container mt-5'>
            <h1>Register</h1>
            <p>Register An Account</p>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group'>
                    <input
                        className='form-control'
                        type='username'
                        placeholder='Username'
                        name='username'
                        value={username}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div className='form-group'>
                    <input
                        className='form-control'
                        type='password'
                        placeholder='Password'
                        name='password'
                        value={password}
                        onChange={e => onChange(e)}
                        // minLength='6'
                        required
                    />
                </div>
                <div className='form-group'>
                    <input
                        className='form-control'
                        type='email'
                        placeholder='Email'
                        name='email'
                        value={email}
                        onChange={e => onChange(e)}
                    />
                </div>
                <div className='form-group'>
                    <input
                        className='form-control'
                        type='first_name'
                        placeholder='First Name'
                        name='first_name'
                        value={first_name}
                        onChange={e => onChange(e)}
                    />
                </div>
                <div className='form-group'>
                    <input
                        className='form-control'
                        type='last_name'
                        placeholder='Last Name'
                        name='last_name'
                        value={last_name}
                        onChange={e => onChange(e)}
                    />
                </div>
                <div className='form-group'>
                    <input
                        className='form-control'
                        type='phone_number'
                        placeholder='Phone Number'
                        name='phone_number'
                        value={phone_number}
                        onChange={e => onChange(e)}
                    />
                </div>
                <button className='btn btn-primary' type='submit'>Register</button>
                {/* { !errorMsg || <h4 style={{ color: "red" }}>Incorrect Combination</h4>} */}
            </form>
            <p className='mt-3'>
                Already have an account? <Link to='/login'>Login</Link>
            </p>
        </div>
    )
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { signup })(Signup);
