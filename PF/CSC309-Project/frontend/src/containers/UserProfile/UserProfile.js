import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import axios from 'axios';
import './userprofile.css';
import { useNavigate } from 'react-router-dom';

const UserProfile = ({isAuthenticated}) => {

    const [user, setUser] = useState({})
    const navigate = useNavigate();
    const handleClick = () => navigate(`/edit`);
    const handleClick2 = () => navigate(`/history`);
    
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
    if (isAuthenticated) {
        if (user.avatar) {
            return (
                <div className="i">
                    <div className="i-left">
                        <div className="i-left-wrapper">
                            <h1 className="i-name">Username: {user.username}</h1>
                            <h2 className="i-intro">First Name: {user.first_name}</h2>
                            <h2 className="i-intro">Last Name: {user.last_name}</h2>
                            <h2 className="i-intro">Phone Number: {user.phone_number}</h2>
                            <br />
                            <button type='button' onClick={handleClick} className="edit-button">{"Edit Profile"}</button>
                            <br />
                            <button type='button' onClick={handleClick2} className="edit-button">{"View Payment History"}</button>
                        </div>
                    </div>

                    <div className="i-right">
                        <div className="i-bg"></div>
                        <img src={"http://localhost:8000/images/" + user.avatar} alt="" className="i-img" />
                    </div>
                </div>
            )
        } else {
            return (
                <div className="i">
                    <div className="i-left">
                        <div className="i-left-wrapper">
                            <h1 className="i-name">Username: {user.username}</h1>
                            <h2 className="i-intro">First Name: {user.first_name}</h2>
                            <h2 className="i-intro">Last Name: {user.last_name}</h2>
                            <h2 className="i-intro">Phone Number: {user.phone_number}</h2>
                            <br />
                            <button type='button' onClick={handleClick} className="edit-button">{"Edit Profile"}</button>
                            <br />
                            <button type='button' onClick={handleClick2} className="edit-button">{"View Payment History"}</button>
                        </div>
                    </div>

                    <div className="i-right">
                        <div className="i-bg"></div>
                    </div>
                </div>
            )
        }
    } else {
        return (
            <h1>Please log in to view profile.</h1>
        )
    }
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps)(UserProfile); 
