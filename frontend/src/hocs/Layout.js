import React, { useEffect } from 'react';
import Navbar from '../components/Navbar/NavbarLoggedOut';
import { connect } from 'react-redux';
import { checkAuthenticated } from '../actions/auth';

const Layout = (props) => {
    useEffect(() => {
        props.checkAuthenticated();
        // eslint-disable-next-line
    }, []);

    return (
        <div>
            <Navbar />
            {props.children}
        </div>
    )
};

export default connect(null, { checkAuthenticated })(Layout);
