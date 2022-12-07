import React from 'react';
import { Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { logout } from '../../actions/auth';

const Logout = ({ logout, isAuthenticated }) => {
    
    if (!isAuthenticated) {
        return <Navigate to='/login'/>
    } else {
        logout();
    }

    return(
        <div>
            Logout
        </div>
    )
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { logout })(Logout);
