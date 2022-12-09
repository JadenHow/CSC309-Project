import React from 'react'
import './paymenthistorycomponents.css'

const PaymentHistoryComponents = ({ amount, card_info, date }) => {
    let date2 = date.split('T')
    let date3 = String(date2[1]).split('.')
    return (
        <div className="ps">
            <div className="ps-border">
                <h3>Amount: ${amount}</h3>
                <h3>Card_Info: {card_info}</h3>
                <h3>Date: {date2[0]} {date3[0]}</h3>
            </div>
        </div>
    )
}

export default PaymentHistoryComponents;
