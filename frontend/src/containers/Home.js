import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Studio from '../components/Studio'
// import { logout } from '../actions/auth';

// const logout_user = () => {
//     logout();
// };

function Home() {
    const [posts, setPosts] = useState([])

    useEffect(() => {
        axios.get('http://localhost:8000/studios/')
        .then(res => {
            // console.log(res.data.results)
            setPosts(res.data.results)
        })
        .catch(err => {
            console.log(err)
        })
    }, [])

    return (
        <div>
            {posts.map((posts, i) => (
                <Studio key={i} key_num={i} name={posts.name} address={posts.address} postal_code={posts.postal_code} image={posts.images[0]?.image} url={posts.url}/>
            ))}
        </div>
    )
}

export default Home;