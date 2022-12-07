import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Subscription from '../components/SubscriptionDetail'
import { Pagination } from 'antd';

const SubscriptionList = () => {
    const [loading1, setLoading1] = useState(true)
    const [posts1, setPosts1] = useState([])
    const [count, setCount] = useState(0);
    const [offset, setOffset] = useState(0);

    // useEffect(() => {
    //     getSubscriptionList();
    // }, []);

    useEffect(() => {
        const getSubscriptionList = async () => {
            axios.get(`http://localhost:8000/subscriptions/?limit=10&offset=${offset}`)
                .then(res => {
                    setPosts1(res.data.results)
                    setCount(res.data.count)
                })
                .catch(err => {
                    console.log(err)
                })
        };
        getSubscriptionList();
    }, [offset])

    function handleChange(value) {
        setOffset((value - 1) * 10);
    };

    // const getSubscriptionList = async () => {
    //     await axios.get(`http://localhost:8000/subscriptions/`)
    //         .then(res => {
    //             setPosts1(res.data)
    //             setLoading1(false)
    //         })
    //         .catch(err => {
    //             console.log(err)
    //             setLoading1(false)
    //         })
    // };


    // if (loading1) {
    //     return <div className="App">Loading...</div>;
    // } else {
        return (
            <div>
                <div>
                    {posts1.map((posts1, i) => (
                        <Subscription key_num={i} price={posts1.price} occurance={posts1.occurance}/>
                    ))}
                </div>
                <br/>
            <Pagination
                defaultCurrent={1}
                defaultPageSize={10} //default size of page
                onChange={handleChange}
                total={count} //total number of card data available
            />
            </div>
            
        )
    //}
};

export default SubscriptionList;