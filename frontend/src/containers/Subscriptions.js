import React from 'react';

const SubscriptionList = () => {
    const params = useParams();

    return (
        <div>
            {params.id}
        </div>
    )
};

export default SubscriptionList;