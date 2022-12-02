import React from 'react'
import "./studio.css";
import Logo from '../logo512.png'

const Studio = ({ key_num, name, address, postal_code, image, url }) => {
    const alternatingColor = ['#73C356', '#FFFFFF']
    if (!image) {
        return (
            <div className="s" style={{ backgroundColor: alternatingColor[key_num % alternatingColor.length] }}>
                <div className="s-left">
                    <img src={Logo} alt="" className="s-img" />
                </div>
                <div className="s-right">
                    <h2 className="s-title">{name}</h2>
                    <h3 className="s-title">{"Address: " + address}</h3>
                    <h3 className="s-title">{"Postal Code: " + postal_code}</h3>
                    <h3 className="s-title">{url}</h3>
                </div>
            </div>
        )
    } else {
        return (
            <div className="s" style={{ backgroundColor: alternatingColor[key_num % alternatingColor.length] }}>
                <div className="s-left">
                    <img src={"http://localhost:8000" + image} alt="" className="s-img" />
                </div>
                <div className="s-right">
                    <h2 className="s-title">{name}</h2>
                    <h3 className="s-title">{"Address: " + address}</h3>
                    <h3 className="s-title">{"Postal Code: " + postal_code}</h3>
                </div>
            </div>
        )
    }
}

export default Studio
