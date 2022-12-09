import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import axios from 'axios';
// import App from '../App';
import "./edituser.css";
import { useNavigate } from 'react-router-dom';

const EditUser = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState({})

    const emptyState = {
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        creditcard: '',
    }

    useEffect(() => {
        const getUser = async () => {
            const config = {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Token ${localStorage.getItem('access')}`
                }
            };

            axios.get(`http://localhost:8000/users/info/`, config)
                .then(res => {
                    setUser(res.data)
                })
                .catch(err => {
                    console.log(err)
                })
        };
        getUser();
    }, [])

    const [file, setFile] = useState();
    const [msg, setMsg] = useState('');

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const[formData, setFormData] = useState(emptyState);

    const { username, password, email, avatar, phone_number, creditcard } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async(e) => {
        e.preventDefault();
        console.log("submitted", formData);

        const config = {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Token ${localStorage.getItem('access')}`
            }
        };

        const body = {
            "username": formData.username,
            "password": formData.password,
            "email": formData.email,
            "first_name": formData.first_name,
            "last_name": formData.last_name,
            "phone_number": formData.phone_number,
            "credit_card_number": formData.creditcard,
            "avatar": file
        }

        console.log(body);
        try {
            console.log(formData)
            await axios.patch(`http://localhost:8000/users/edit/`, body, config);
            setMsg("success")
            setFormData(emptyState);
            navigate(`/profile`);

            //return <Navigate to='/edit'/>
        } catch (err) {
            setMsg(err.response.data.msg)
            console.log(err);
        }
        //console.log("button worked");
        // setFormData('');
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
                            value={user.first_name}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='text'
                            name='last_name'
                            placeholder='last name'
                            value={user.last_name}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='text'
                            name='phone_number'
                            placeholder='phone number'
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
                            onChange={handleFileChange}
                        />
                    </div>
                    <div className='inputfield'>
                        <input
                            className='form-control'
                            type='text'
                            name='creditcard'
                            placeholder='credit card number'
                            alt='creditcard'
                            value={creditcard}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='inputfield'>{msg}</div>
                </div>
                <button className='btn btn-primary' type='submit'>Save</button>
            </form>
            {/* <br />
            <div><img src={"http://localhost:8000/images/" + user.avatar} alt="no image" width="100%" /></div> */}
        </div>
    )
};
// https://stackoverflow.com/questions/39153545/how-to-do-post-in-form-submit-using-reactjs-and-pass-the-object-value-into-rest
const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps)(EditUser); //(mapStateToProps);
