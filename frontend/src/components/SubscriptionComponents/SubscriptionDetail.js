import React from 'react'

// user = models.OneToOneField(User, on_delete=models.CASCADE) # A user can only be on one subscription plan at a time
// parent_subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.CASCADE)
// renewal_date = models.DateField(blank=False, null=False)
// cancelled = models.BooleanField(default=False)
const Subscription = ({key_num, price, occurance }) => {
    const alternatingColor = ['#3bedb7', '#FFFFFF']

    return (
        <div className="s">
            <div className='s-border' style={{ backgroundColor: alternatingColor[key_num % alternatingColor.length] }}>
                <div className="s-right">
                    <h2 className="s-title">Price: ${price}</h2>
                    <h3 className="s-title">Billing Cycle: {occurance}</h3>
                </div>
            </div>
        </div>
    )
}

export default Subscription