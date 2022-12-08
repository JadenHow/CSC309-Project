import React from 'react'
import axios from 'axios';
import "./subscriptiondetail.css";

// user = models.OneToOneField(User, on_delete=models.CASCADE) # A user can only be on one subscription plan at a time
// parent_subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.CASCADE)
// renewal_date = models.DateField(blank=False, null=False)
// cancelled = models.BooleanField(default=False)
const Subscription = ({key_num, price, occurance }) => {
    const alternatingColor = ['#3bedb7', '#FFFFFF']
    const handleClick = async() => {
        // try {
        //     let response = await fetch(`http://localhost:8000/subscriptions/${key_num}/subscribe/`, {
        //         headers: {
        //             'Accept': 'application/json',
        //             'Content-Type': 'application/json'
        //         },
        //         method: 'POST'
        //     });
        //     console.log(response);
        //     message = response.statusText;
        //     //return <Navigate to='/profile/'/>
        // } catch (err) {
        //     console.log(err)
        // }
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${localStorage.getItem('access')}`
            }
        };
        // subscribe
        axios.post(`http://localhost:8000/subscriptions/${key_num}/subscribe/`, {}, config)
        .then(res => {
            console.log(res);
            message = res.data["detail"];
        })
        .catch( res => { // update subscriptions if already subbed
            console.log("error", res);
            // axios.patch(`http://localhost:8000/subscriptions/edit/`, {}, config)
            // .then(res => {
            //     console.log(res);
            //     message = res.data["detail"];
            // })
        })
        //navigate(`/subscriptions`);
    }
    var message = "";

    return (
        <div className="sub-box">
            <p className='message'>{message}</p>
            <div className='s-border' style={{ backgroundColor: alternatingColor[key_num % alternatingColor.length] }}>
                <div className="s-right">
                    <h2 className="s-title">Price: ${price}</h2>
                    <h3 className="s-title">Billing Cycle: {occurance}</h3>
                    <button type='button' onClick={handleClick} className="s-button">{"Subscribe"}</button>
                </div>
            </div>
        </div>
    )
}

export default Subscription