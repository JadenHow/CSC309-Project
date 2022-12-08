import React, { useState, useEffect } from 'react'
import './FindStudio.css';
import axios from 'axios';
import GeographicalStudioComponents from '../../components/GeographicalStudioComponents/GeographicalStudioComponents';
import { Pagination } from 'antd';

const FindStudio = () => {
    const [loading, setLoading] = useState(true)
    const [posts, setPosts] = useState([])
    const [offset, setOffset] = useState(0);
    const [count, setCount] = useState(0);

    function handleChange(value) {
        setOffset((value - 1) * 10);
    };

    useEffect(() => {
        async function getUserLocation() {
            const body = {
                'latitude': '',
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

            await axios.get(`http://localhost:8000/studios/nearme/?limit=10&offset=${offset}`, body)
                .then(res => {
                    console.log(res.data.results)
                    setPosts(res.data.results)
                    setCount(res.data.count)
                    setLoading(false)
                })
                .catch(err => {
                    // console.log(err.response.data.msg)
                    // window.alert(err.response.data.msg)
                    console.log(err)
                    setLoading(false)
                })
        }
        getUserLocation();
    }, [offset]);

    if (loading) {
        return (
            <h1>loading</h1>
        )
    }
    else {
        return (
            <div>
                <div>
                    {posts.map((posts, i) => (
                        <GeographicalStudioComponents i={i} key={posts.pk} key_num={posts.pk} name={posts.name} address={posts.address} postal_code={posts.postal_code} phone_number={posts.phone_number} />
                    ))}
                </div>
                <br />
                <Pagination
                    defaultCurrent={1}
                    defaultPageSize={10} //default size of page
                    onChange={handleChange}
                    total={count} //total number of card data available
                />
            </div>
        )
    }
}

export default FindStudio;