import React from 'react'
import "./geographicalstudiocomponents.css";
import { useNavigate } from 'react-router-dom';


const Studio = ({ i, key_num, name, address, postal_code, phone_number }) => {
    const navigate = useNavigate();
    const handleClick = () => navigate(`/studios/${key_num}`);
    
    const alternatingColor = ['#3bedb7', '#FFFFFF']
    return (
        <div className="s">
            <div className='s-border' style={{ backgroundColor: alternatingColor[i % alternatingColor.length] }} >
            <div>
                <h2 className="s-title">{name}</h2>
                <h3 className="s-title">{address}</h3>
                <h3 className="s-title">{postal_code}</h3>
                <h3 className="s-title">{phone_number}</h3>
                <button type='button' onClick={handleClick} className="s-button">{"Club Details"}</button>
            </div>
            </div>
        </div>
    )
}

export default Studio
