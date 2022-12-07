import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StudioDetailComponents from '../../components/StudioDetailComponents/StudioDetail'
import ClassDetailComponents from '../../components/ClassComponents/ClassDetail'
import { useParams } from "react-router-dom";

const StudioDetail = () => {
    const params = useParams();
    const [posts1, setPosts1] = useState([])
    const [posts2, setPosts2] = useState([])
    const [loading1, setLoading1] = useState(true)
    const [loading2, setLoading2] = useState(true)
    
    useEffect(() => {
        getStudioDetail();
        getClass();
    }, []);

    const getStudioDetail = async () => {
        await axios.get(`http://localhost:8000/studios/${params.id}/`)
            .then(res => {
                setPosts1(res.data)
                setLoading1(false)
            })
            .catch(err => {
                console.log(err)
                setLoading1(false)
            })
    };

    const getClass = async () => {
        await axios.get(`http://localhost:8000/studios/${params.id}/classes/`)
            .then(res => {
                console.log(res.data.results)
                setPosts2(res.data.results)
                setLoading2(false)
            })
            .catch(err => {
                console.log(err)
                setLoading2(false)
            })
    };

    if (loading1 || loading2) {
        return <div className="App">Loading...</div>;
    } else {
        return (
            <div>
                <div>
                    {<StudioDetailComponents name={posts1.name} phone_number={posts1.phone_number} address={posts1.address} postal_code={posts1.postal_code} latitude={posts1.latitude} longitude={posts1.longitude} images={posts1.images} amenities={posts1.amenities} />}
                </div>
                <div>
                    {posts2.map((posts2, i) => (
                        <ClassDetailComponents key={i} pk={posts2.pk} name={posts2.name} description={posts2.description} coach={posts2.coach} keywords={posts2.keywords} capacity={posts2.capacity} currently_enrolled={posts2.currently_enrolled} class_date={posts2.class_date} start_time={posts2.start_time} end_time={posts2.end_time} />
                    ))}
                </div>
            </div>
        )
    }
}

export default StudioDetail;
