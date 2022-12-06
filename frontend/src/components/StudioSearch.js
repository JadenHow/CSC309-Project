import React from 'react';
import algoliasearch from 'algoliasearch/lite';
import { InstantSearch, SearchBox, Hits, Highlight, Pagination, Configure } from 'react-instantsearch-hooks-web';
import "./studio.css";
import { useNavigate } from 'react-router-dom';

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

function ClassStudioHit({ hit }) {
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

const ClassStudioSearch = () => {
    return (
        <InstantSearch searchClient={searchClient} indexName="backend_Class" >
            <Configure hitsPerPage={10} />
            <br />
            Search for Studios: <SearchBox />
            <Hits hitComponent={ClassStudioHit} />
            <Pagination></Pagination>
        </InstantSearch>
    )
};


export default ClassStudioSearch;
