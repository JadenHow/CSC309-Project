import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { login } from '../../actions/auth';


const Login = ({ login, isAuthenticated }) => {
    const[formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const[msg, setMsg] = useState('')
    const { username, password } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();

        login(username, password);
        setMsg("Unable to log in with provided credentials.")
    };

    if (isAuthenticated) {
        return <Navigate to='/'/>
    }

    return(
        <div className='container mt-5'>
            <h1 className='title'>Login</h1>
            <p>Login to your Account</p>
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
                <button className='btn btn-primary' type='submit'>Login</button>
                <h4 style={{ color: 'red' }}>{msg}</h4>
            </form>
            <p className='mt-3'>
                Don't have an account? <Link to='/signup'>Sign Up</Link>
            </p>
        </div>
    )
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { login })(Login);
// export default Login;