import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Subscription from '../../components/SubscriptionComponents/SubscriptionDetail'
import { Pagination } from 'antd';
import "./subscriptions.css"

const SubscriptionList = () => {
    const [loading1, setLoading1] = useState(true)
    const [posts1, setPosts1] = useState([])
    const [count, setCount] = useState(0);
    const [offset, setOffset] = useState(0);
    const [msg, setMsg] = useState("")

    useEffect(() => {
        const getSubscriptionList = async () => {
            axios.get(`http://localhost:8000/subscriptions/?limit=10&offset=${offset}`)
                .then(res => {
                    setPosts1(res.data.results)
                    setCount(res.data.count)
                    setLoading1(false)
                })
                .catch(err => {
                    console.log(err)
                    setLoading1(false)
                })
        };
        getSubscriptionList();
    }, [offset])

    function handleChange(value) {
        setOffset((value - 1) * 10);
    };

    // click the unsub button
    const handleClick = async() => {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${localStorage.getItem('access')}`
            }
        };
        axios.patch(`http://localhost:8000/subscriptions/edit/`, {"cancelled": true}, config)
        .then(res => {
            setMsg("Successfully cancelled")
            console.log(res);
        })
        .catch(err => {
            setMsg("Please log in to cancel")
        }
        )
    }

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


    if (loading1) {
        return <div className="App">Loading...</div>;
    } else {
        return (
            <div>
                <h3 className='title'>Subscription Plan Options:</h3>
                <div className='subs'>
                    {posts1.map((posts1) => (
                        <Subscription key_num={posts1.pk} price={posts1.price} occurance={posts1.occurance}/>
                    ))}
                </div>               
            <Pagination className='page'
                defaultCurrent={50}
                defaultPageSize={50} //default size of page
                onChange={handleChange}
                total={count} //total number of card data available
            />
            <div>
                <button onClick={handleClick} type='button' className='unsub-button'>Cancel current plan</button>
            </div>
                <h4>{msg}</h4>
            </div>
        )
    }
};

export default SubscriptionList;