import React from 'react'
import "./studiodetail.css";
// import Logo from '../logo512.png'

const StudioDetail = ({ name, phone_number, address, postal_code, latitude, longitude, images, amenities }) => {
    // console.log(amenities.type)
    return (
        <div className="sd">
            <div className='sd-border'>
                <div className="sd-left">
                    {images.map((images, i) => (
                        <img key={i} src={"http://localhost:8000" + images.image} alt="" className="sd-img" />
                    ))}
                </div>
                <div className="sd-right">
                    <h1 className="sd-title">{name}</h1>
                    <h2><a className="sd-title" href={`https://www.google.com/maps/place/(${latitude}, ${longitude})`}>{address}</a></h2>
                    <h2 className="sd-title">{postal_code}</h2>
                    <h2 className="sd-title">{phone_number}</h2>
                    <h1>Amenities:</h1>
                    {amenities.map((amenities, i) => (
                        <h2 key={i}>{amenities.type}: {amenities.quantity}</h2>
                    ))}
                </div>
            </div>
        </div>
    )
    }

export default StudioDetail
