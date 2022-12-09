import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { GoogleMap, useLoadScript, MarkerF } from "@react-google-maps/api";
import { useNavigate } from 'react-router-dom';
import './MapComponent1.css'


const MapComponent1 = () => {
    const { isLoaded } = useLoadScript({
        googleMapsApiKey: "AIzaSyBQiSRGh5Cm0tHmsNPoNZSaAT6FlkGfne0"
    })

    if (!isLoaded) return <div>Loading...</div>

    return  (
        <Map/>
    )
}

const Map = () => {
    const navigate = useNavigate();
    // const handleClick = (pk) => navigate(`/studios/${pk}}`);
    function handleClick(pk) {
        console.log(pk);
        navigate(`/studios/${pk}/`);
    }

    const center = useMemo(() => ({lat: 43.6532, lng: -79.3832}), [])
    // console.log(center);

    const [posts1, setPosts] = useState([])

    useEffect(() => { 
      const getStudioLocations = () => {
        axios.get(`http://localhost:8000/studios/`)
        .then(response => {
            console.log(response.data.results);
            setPosts(response.data.results)
  
        })
        .catch(err => {
            console.log(err)
        })
      }
  
      getStudioLocations()
      }, []);

    return (
        <GoogleMap zoom={10} center={center} mapContainerClassName="map-container">
            {/* posts1.map() */}
            {posts1.map((posts1, i) => (
                        <MarkerF key={posts1.pk} position={{lat: parseInt(posts1.latitude), lng: parseInt(posts1.longitude)}} onClick={() => handleClick(posts1.pk)} />
                ))}
        </GoogleMap>
    );
}

export default MapComponent1