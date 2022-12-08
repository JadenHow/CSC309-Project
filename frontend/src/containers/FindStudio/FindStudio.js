import React, { useState, useEffect } from 'react'
import './FindStudio.css';
import axios from 'axios';

const FindStudio = (props) => {
    const [loading, setLoading] = useState(true)
    const [posts, setPosts] = useState([])

    useEffect(() => {
        getUserLocation();
    }, []);

    
    async function getUserLocation() {
        const body = {
            'latitude' : '',
            'longitude': ''
        };

        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const long = position.coords.longitude;
                body.latitude = lat;
                body.longitude = long;
                console.log(body);
                console.log(lat);
                console.log(long);
            },
            error => {
                console.log("Error getting location");
            }
        )

        await axios.get(`http://localhost:8000/studios/nearme/`, body)
        .then(res => {
            console.log(res.data.results)
            setPosts(res.data.results)
            setLoading(false)
        })
        .catch(err => {
            // console.log(err.response.data.msg)
            // window.alert(err.response.data.msg)
            console.log(err)
            setLoading(false)
        })
    }

    if (loading) {
        return (
            <h1>loading</h1>
        )
    }
    else {
        return (
            <div>
                plz load the data
            </div>
        )
    }
}

export default FindStudio;