import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ClassScheduleComponents from '../../components/ClassScheduleComponents/ClassSchedule'
import { Pagination } from 'antd';
import { connect } from 'react-redux';

function ClassSchedule({isAuthenticated}) {
    const [posts, setPosts] = useState([])
    const [offset, setOffset] = useState(0);
    const [count, setCount] = useState(0);
    const [loading, setLoading] = useState(true);

    function handleChange(value) {
        setOffset((value - 1) * 10);
    };

    useEffect(() => {
        const getSchedule = async () => {
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('access')}`
                }
            };

            axios.get(`http://localhost:8000/users/classes/?limit=10&offset=${offset}`, config)
                .then(res => {
                    setPosts(res.data.results)
                    setCount(res.data.count)
                    setLoading(false)
                    console.log(res.data.results);
                })
                .catch(err => {
                    setLoading(false)
                })
        };
        getSchedule();
    }, [offset])

    if (!isAuthenticated) {
        return (<h1>Please login to continue.</h1>)
    } else if (loading) {
        return (<h1>Loading...</h1>)
    } else {
        return (
            <div>
                <div>
                    {posts.map((posts, i) => (
                        <ClassScheduleComponents key={i} pk={posts.pk} name={posts.name} studio={posts.studio} description={posts.description} coach={posts.coach} keywords={posts.keywords} capacity={posts.capacity} class_date={posts.class_date} start_time={posts.start_time} end_time={posts.end_time} />
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

export default connect(mapStateToProps, {})(ClassSchedule);
