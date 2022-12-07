import React, { useState } from 'react';
import algoliasearch from 'algoliasearch/lite';
import { InstantSearch, SearchBox, Hits, Highlight, Pagination, Configure } from 'react-instantsearch-hooks-web';
import "./studio.css";
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ClassDetailComponents from '../components/ClassDetail'
import "./studiosearch.css";

const searchClient = algoliasearch('2SE5TN8IRT', 'aa72026cb29188c2018f9011071e18e5');

function StudioHit({ hit }) {
    const navigate = useNavigate();
    function handleClick() {navigate(`/studios/${hit.objectID}`)};

    return (
        <div className="s-border" style={{ cursor: 'pointer' }} onClick={handleClick}>
            <div className="s-content">
                <h2><Highlight attribute="name" hit={hit} /></h2>
                <h4>{hit.address}</h4>
                <h4>{hit.postal_code}</h4>
                <h4>{hit.phone_number}</h4>
            </div>
        </div>
    );
}

function AmenityHit({ hit }) {
    const split_studio = hit.studio.split("(")
    // console.log(split_studio[1][0])
    const navigate = useNavigate();
    function handleClick() { navigate(`/studios/${split_studio[1][0]}`) };

    return (
        <div className="s-border" style={{ cursor: 'pointer' }} onClick={handleClick}>
            <div className="s-content">
                <h2>{hit.studio}</h2>
                <h4><Highlight attribute="type" hit={hit} /></h4>
                <h4>{hit.quantity}</h4>
            </div>
        </div>
    );
}

function ClassInstanceHit({ hit }) {
    const split_studio = hit.studio.split("(")
    // console.log(split_studio[1][0])
    const navigate = useNavigate();
    function handleClick() { navigate(`/studios/${split_studio[1][0]}`) };

    return (
        <div className="s-border" style={{ cursor: 'pointer' }} onClick={handleClick}>
            <div className="s-content">
                <h2><Highlight attribute="name" hit={hit} /></h2>
                <h4><Highlight attribute="coach" hit={hit} /></h4>
                <h4>{hit.description}</h4>
                <h4>{hit.keywords}</h4>
                <h4>{hit.capacity}</h4>
                <h4>{hit.start_date}</h4>
                <h4>{hit.start_time}</h4>
                <h4>{hit.end_time}</h4>
            </div>
        </div>
    );
}

const StudioSearch = () => {
    return (
        <InstantSearch searchClient={searchClient} indexName="backend_Studio">
            <Configure hitsPerPage={10} />
            <br />
            Search for Studios: <SearchBox />
            <Hits hitComponent={StudioHit} />
            <Pagination></Pagination>
        </InstantSearch>
    )
};

const AmenitiesSearch = () => {
    return (
        <InstantSearch searchClient={searchClient} indexName="backend_StudioAmenities">
            <Configure hitsPerPage={10} />
            <br />
            Search for Studios: <SearchBox />
            <Hits hitComponent={AmenityHit} />
            <Pagination></Pagination>
        </InstantSearch>
    )
};

const ClassInstanceSearch = () => {
    const [posts, setPosts] = useState([])

    function class_search(search, start_date, end_date, start_time, end_time) {
        axios.get(`http://localhost:8000/classes/search/?q=${search}&start=${start_date}&end=${end_date}&starttime=${start_time}&endttime=${end_time}`)
            .then(res => {
                setPosts(res.data.results)
                console.log(res)
            })
            .catch(err => {
                console.log(err)
            })
    };

    const [searchData, setSearchData] = useState({
        search: '',
        start_date: '',
        end_date: '',
        start_time: '',
        end_time: '',
    });

    const { search, start_date, end_date, start_time, end_time } = searchData;

    const onChange = e => setSearchData({ ...searchData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();

        class_search(search, start_date, end_date, start_time, end_time);
    };
    return (
        <div>
            <div className='form'>
                <h1>Search for classes:</h1>
                <form onSubmit={e => onSubmit(e)}>
                    <div className='form-group'>
                        <input
                            className='class-instance-search-bar'
                            type='search'
                            placeholder='Search'
                            name='search'
                            value={search}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='form-group'>
                        <input
                            className='search-control'
                            type='start_date'
                            placeholder='Start Date (optional) In this format: 2022-12-20'
                            name='start_date'
                            value={start_date}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='form-group'>
                        <input
                            className='search-control'
                            type='end_date'
                            placeholder='End date (optional) In this format: 2022-12-22'
                            name='end_date'
                            value={end_date}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='form-group'>
                        <input
                            className='search-control'
                            type='start_time'
                            placeholder='Start Time (optional) In this format: 01:55:00'
                            name='start_time'
                            value={start_time}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='form-group'>
                        <input
                            className='search-control'
                            type='end_time'
                            placeholder='End Time (optional) In this format: 02:55:00'
                            name='end_time'
                            value={end_time}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <button className='btn btn-primary' type='submit'>Search</button>
                </form>
            </div>
            <div>
                {posts.map((posts, i) => (
                    <ClassDetailComponents key={i} pk={posts.objectID} name={posts.name} description={posts.description} coach={posts.coach} keywords={posts.keywords} capacity={posts.capacity} currently_enrolled={posts.currently_enrolled} class_date={posts.class_date} start_time={posts.start_time} end_time={posts.end_time} />
                ))}
            </div>
        </div>
    )
};



const ClassStudioSearch = () => {

    const [posts, setPosts] = useState([])
    const current_url = window.location.pathname

    function class_studio_search(search, studio_id) {
        axios.get(`http://localhost:8000/studios/search/?q=${search}&studio=${studio_id}`)
            .then(res => {
                setPosts(res.data.results)
                console.log(res)
            })
            .catch(err => {
                console.log(err)
            })
    };

    const [searchData, setSearchData] = useState({
        search: '',
    });

    const { search } = searchData;

    const onChange = e => setSearchData({ ...searchData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();

        class_studio_search(search, current_url.split('/')[2]);
    };

    return (
        <div>
            <div className='container mt-5'>
                <h1>Search for classes:</h1>
                <form onSubmit={e => onSubmit(e)}>
                    <div className='form-group'>
                        <input
                            className='form-control'
                            type='search'
                            placeholder='Search'
                            name='search'
                            value={search}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <button className='btn btn-primary' type='submit'>Search</button>
                </form>
            </div>
            <div>
                {posts.map((posts, i) => (
                    <ClassDetailComponents key={i} pk={posts.pk} name={posts.name} description={posts.description} coach={posts.coach} keywords={posts.keywords} capacity={posts.capacity} currently_enrolled={posts.currently_enrolled} class_date={posts.class_date} start_time={posts.start_time} end_time={posts.end_time} />
                ))}
            </div>
        </div>
    )
};

export default ClassInstanceSearch;
