import React, {useState} from 'react'
import "./classdetail.css";
import axios from 'axios';
import { connect } from 'react-redux';
import { useParams } from "react-router-dom";

const ClassDetail = ({ pk, name, description, coach, keywords, capacity, currently_enrolled, class_date, start_time, end_time, isAuthenticated }) => {
    const params = useParams();
    const [msg, setMsg] = useState("")
    
    function enrollClass(params, pk, isAuthenticated) {
        if (isAuthenticated) {
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('access')}`
                }
            };

            axios.post(`http://localhost:8000/studios/0/classes/${pk}/enrol/`, {}, config)
                .then(res => {
                    console.log(res.data.msg)
                    setMsg(res.data.msg)
                })
                .catch(err => {
                    // console.log(err.response.data.msg)
                    // window.alert(err.response.data.msg)
                    console.log(err)
                    setMsg(err.response.data.msg)
                })
        } else {
            setMsg("Please login to enrol.")
        }
    };

    function enrollAllClass(pk, isAuthenticated) {
        if (isAuthenticated) {
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('access')}`
                }
            };
            axios.post(`http://localhost:8000/studios/0/classes/${pk}/enrol/multiple`, {}, config)
                .then(res => {
                    console.log(res.data.msg)
                    setMsg(res.data.msg)
                })
                .catch(err => {
                    // console.log(err.response.data.msg)
                    // window.alert(err.response.data.msg)
                    console.log(err)
                })
        } else {
            setMsg("Please login to enrol.")
        }
    };

    return (
        <div className="c">
            <div className="c-wrap">
                <h2>Name: {name}</h2>
                <h3>Description: {description}</h3>
                <h3>Coach: {coach}</h3>
                <h3>Keywords: {keywords}</h3>
                <h3>Capacity: {capacity}</h3>
                <h3>Class Date: {class_date}</h3>
                <h3>Start Time: {start_time}</h3>
                <h3>End Time: {end_time}</h3>
                <button onClick={() => enrollClass(params, pk, isAuthenticated)}>Enroll</button>
                <button onClick={() => enrollAllClass(pk, isAuthenticated)}>Enroll All</button>
                <h3>{msg}</h3>
            </div>
        </div>
    )
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, {})(ClassDetail);
// export default ClassDetail
