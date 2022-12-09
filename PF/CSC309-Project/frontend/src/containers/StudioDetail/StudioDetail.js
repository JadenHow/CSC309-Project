import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StudioDetailComponents from '../../components/StudioDetailComponents/StudioDetail'
import ClassDetailComponents from '../../components/ClassComponents/ClassDetail'
import { ClassStudioSearch } from '../../components/Search/StudioSearch'
import { useParams } from "react-router-dom";
import { Pagination } from 'antd';

const StudioDetail = () => {
    const params = useParams();
    const [posts1, setPosts1] = useState([])
    const [posts2, setPosts2] = useState([])
    const [loading1, setLoading1] = useState(true)
    const [loading2, setLoading2] = useState(true)

    const [offset, setOffset] = useState(0);
    const [count, setCount] = useState(0);

    function handleChange(value) {
        setOffset((value - 1) * 10);
    };
    
    useEffect(() => {
        const getClass = async () => {
            // console.log(offset)
            await axios.get(`http://localhost:8000/studios/${params.id}/classes/?limit=10&offset=${offset}`)
                .then(res => {
                    // console.log(res.data.results)
                    setPosts2(res.data.results)
                    setCount(res.data.count)
                    setLoading2(false)
                })
                .catch(err => {
                    console.log(err)
                    setLoading2(false)
                })
        };
        getClass();
        getStudioDetail();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [offset]);

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

    if (loading1 || loading2) {
        return <div className="App">Loading...</div>;
    } else {
        return (
            <div>
                <div>
                    {<StudioDetailComponents name={posts1.name} phone_number={posts1.phone_number} address={posts1.address} postal_code={posts1.postal_code} latitude={posts1.latitude} longitude={posts1.longitude} images={posts1.images} amenities={posts1.amenities} />}
                </div>
                <div>
                    <ClassStudioSearch />
                </div>
                <div>
                    <h1>Available Classes:</h1>
                    {posts2.map((posts2, i) => (
                        <ClassDetailComponents key={i} pk={posts2.pk} name={posts2.name} description={posts2.description} coach={posts2.coach} keywords={posts2.keywords} capacity={posts2.capacity} currently_enrolled={posts2.currently_enrolled} class_date={posts2.class_date} start_time={posts2.start_time} end_time={posts2.end_time} />
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

export default StudioDetail;
