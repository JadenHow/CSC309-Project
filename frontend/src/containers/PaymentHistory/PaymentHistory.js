import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Pagination } from 'antd';
import PaymentHistoryComponents from '../../components/PaymentHistoryComponents/PaymentHistoryComponents'
import { connect } from 'react-redux';

function PaymentHistory({ isAuthenticated }) {
    const [posts1, setPosts1] = useState([])
    const [posts, setPosts] = useState([])
    const [offset, setOffset] = useState(0);
    const [count, setCount] = useState(0);

    function handleChange(value) {
        setOffset((value - 1) * 10);
    };

    useEffect(() => {
        if (localStorage.getItem('access')) {
            const getNextPayment = async () => {
                const config = {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${localStorage.getItem('access')}`
                    }
                };

                axios.get(`http://localhost:8000/users/nextpayment/`, config)
                    .then(res => {
                        setPosts1(res.data)
                    })
                    .catch(err => {
                        console.log(err)
                    })
            };
            const getPaymentHistory = async () => {
                const config = {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${localStorage.getItem('access')}`
                    }
                };

                axios.get(`http://localhost:8000/users/paymenthistory/?limit=10&offset=${offset}`, config)
                    .then(res => {
                        console.log(res.data.results)
                        setPosts(res.data.results)
                        setCount(res.data.count)
                    })
                    .catch(err => {
                        console.log(err)
                    })
            };
            getNextPayment();
            getPaymentHistory();
        }
    }, [offset])
    
    if (!isAuthenticated) {
        return (<h1>Please log in to view page.</h1>)
    } else {
        return (
            <div>
                <div>
                    <h1>Next Payment:</h1>
                    <h3>Next Payment Due: {String(posts1.next_payment_due)}</h3>
                    <h3>Amount Due: {String(posts1.amount_due)}</h3>
                    <h3>Cancelled: {String(posts1.cancelled)}</h3>
                </div>
                <div>
                    <h1>Payment History:</h1>
                    {posts.map((posts, i) => (
                        <PaymentHistoryComponents key={i} amount={posts.amount} card_info={posts.card_info} date={posts.date} />
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

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, {})(PaymentHistory);
