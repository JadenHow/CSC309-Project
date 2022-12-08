import React from 'react'
import axios from 'axios';
import "./subscriptiondetail.css";

// user = models.OneToOneField(User, on_delete=models.CASCADE) # A user can only be on one subscription plan at a time
// parent_subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.CASCADE)
// renewal_date = models.DateField(blank=False, null=False)
// cancelled = models.BooleanField(default=False)
const Subscription = ({key_num, price, occurance }) => {
    const alternatingColor = ['#3bedb7', '#FFFFFF']
    const [message, setMessage] = React.useState({});
    const handleClick = async() => {
        if (localStorage.getItem('access')){
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${localStorage.getItem('access')}`
                }
            };
            // subscribe
            console.log(key_num)
            axios.post(`http://localhost:8000/subscriptions/${key_num}/subscribe/`, {}, config)
                .then(res => {
                    console.log(res);
                    //message = res.data["msg"];
                    setMessage({ msg: res.data["msg"] });
                })
                .catch(res => { // update subscriptions if already subbed
                    console.log("error, will try updating instead", res);
                    axios.patch(`http://localhost:8000/subscriptions/edit/`, { "parent_subscription": key_num }, config)
                        .then(res => {
                            console.log(res);
                            setMessage({ msg: res.data["msg"] });
                            console.log(message)
                        })
                })
        } else {
            setMessage({ msg: "Please log in to subscribe." });
        }
    }

    return (
        <div className="sub-box">
            <div className='s-border' style={{ backgroundColor: alternatingColor[key_num % alternatingColor.length] }}>
                <div className="s-right">
                    <h2 className="s-title">Price: ${price}</h2>
                    <h3 className="s-title">Billing Cycle: {occurance}</h3>
                    <h3>
                    <button type='button' onClick={handleClick} className="s-button">{"Subscribe"}</button>
                    </h3>
                </div>
            </div>
            <div>
                <p className='message'>{message.msg}</p>
            </div>
        </div>
    )
}

export default Subscription