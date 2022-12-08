import React, { useState } from 'react'
import "../ClassComponents/classdetail.css";
import axios from 'axios';
import { connect } from 'react-redux';

const ClassSchedule = ({ pk, name, studio, description, coach, keywords, capacity, currently_enrolled, class_date, start_time, end_time, isAuthenticated }) => {
    const [msg, setMsg] = useState("")

    function disenrollClass(studio_id, pk, isAuthenticated) {
        if (isAuthenticated) {
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('access')}`
                }
            };
            axios.post(`http://localhost:8000/studios/${studio_id}/classes/${pk}/drop/`, {}, config)
                .then(res => {
                    setMsg(res.data.msg)
                })
                .catch(err => {
                    setMsg(err.response.data.msg)
                })
        } else {
            setMsg("Please login.")
        }
    };

    function disenrollAllClass(studio_id, pk, isAuthenticated) {
        if (isAuthenticated) {
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('access')}`
                }
            };
            axios.post(`http://localhost:8000/studios/${studio_id}/classes/${pk}/drop/multiple`, {}, config)
                .then(res => {
                    setMsg(res.data.msg)
                })
                .catch(err => {
                    setMsg(err.response.data.msg)
                })
        } else {
            setMsg("Please login.")
        }
    };

    return (
        <div className="c">
            <div className="c-wrap">
                <h3>Studio: {studio}</h3>
                <h2>Name: {name}</h2>
                <h3>Description: {description}</h3>
                <h3>Coach: {coach}</h3>
                <h3>Keywords: {keywords}</h3>
                <h3>Capacity: {capacity}</h3>
                <h3>Currently Enrolled: {currently_enrolled}</h3>
                <h3>Class Date: {class_date}</h3>
                <h3>Start Time: {start_time}</h3>
                <h3>End Time: {end_time}</h3>
                <button onClick={() => disenrollClass(studio.split(' ')[1], pk, isAuthenticated)}>Disenroll</button>
                <button onClick={() => disenrollAllClass(studio.split(' ')[1], pk, isAuthenticated)}>Disenroll All</button>
                <h3>{msg}</h3>
            </div>
        </div>
    )
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, {})(ClassSchedule);
// export default ClassDetail
