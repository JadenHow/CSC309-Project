import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { signup } from '../../actions/auth';
import './signup.css'

const Signup = ({ signup }) => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        credit_card_number: '',
    });

    const [file, setFile] = useState();

    const { username, password, email, first_name, last_name, phone_number, credit_card_number, avatar } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const onSubmit = e => {
        e.preventDefault();

        signup(username, password, email, first_name, last_name, phone_number, credit_card_number, file);

    };

    return (
        <div className='container mt-5'>
            <h1 className='title'>Register</h1>
            <p className='header'>Register An Account</p>
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
                <div>
                    Avatar:
                    <input
                        className='form-control'
                        type='file'
                        name='avatar'
                        placeholder='avatar'
                        alt='avatar'
                        value={avatar}
                        accept="image/png, image/jpeg"
                        onChange={handleFileChange}
                    />
                </div>
                <button className='btn btn-primary' type='submit'>Register</button>
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
