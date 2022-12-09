import React from 'react'
import "./studio.css";
import Logo from '../../logo512.png'
import { useNavigate } from 'react-router-dom';


const Studio = ({ key_num, name, address, postal_code, image, url }) => {
    const split_url = url.split("/")
    const navigate = useNavigate();
    const handleClick = () => navigate(`/studios/${split_url[4]}`);

    const alternatingColor = ['#3bedb7', '#FFFFFF']
    if (!image) {
        return (
            <div className="s">
                <div className='s-border' style={{ backgroundColor: alternatingColor[key_num % alternatingColor.length] }}>
                    <div className="s-left">
                        <img src={Logo} alt="" className="s-img" />
                    </div>
                    <div className="s-right">
                        <h2>{name}</h2>
                        <h3>{address}</h3>
                        <h3>{postal_code}</h3>
                        <button type='button' onClick={handleClick} className="s-button">{"Club Details"}</button>
                    </div>
                </div>
            </div>
        )
    } else {
        return (
            <div className="s">
                <div className='s-border' style={{ backgroundColor: alternatingColor[key_num % alternatingColor.length] }}>
                    <div className="s-left">
                        <img src={"http://localhost:8000" + image} alt="" className="s-img" />
                    </div>
                    <div className="s-right">
                        <h2>{name}</h2>
                        <h3>{address}</h3>
                        <h3>{postal_code}</h3>
                        <button type='button' onClick={handleClick} className="s-button">{"Club Details"}</button>
                    </div>
                </div>
            </div>
        )
    }
}

export default Studio
