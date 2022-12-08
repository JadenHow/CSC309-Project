import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StudioComponents from '../../components/StudioComponents/Studio'
import { Pagination } from 'antd';

function Studio() {
    const [posts, setPosts] = useState([])
    const [offset, setOffset] = useState(0);
    const [count, setCount] = useState(0);

    function handleChange(value) {
        setOffset((value - 1) * 10);
    };

    useEffect(() => {
        const getStudios = async () => {
            axios.get(`http://localhost:8000/studios/?limit=10&offset=${offset}`)
                .then(res => {
                    setPosts(res.data.results)
                    setCount(res.data.count)
                })
                .catch(err => {
                    console.log(err)
                })
        };
        getStudios();
    }, [offset])

    return (
        <div>
            <div>
                {posts.map((posts, i) => (
                    <StudioComponents key={i} key_num={i} name={posts.name} address={posts.address} postal_code={posts.postal_code} image={posts.images[0]?.image} url={posts.url}/>
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
}

export default Studio;
