import React from 'react'
import { Nav, NavLink, NavMenu, NavBtn, NavBtnLink, ContrastedNavBtnLink, NavLinkIcon } from './NavbarLoggedOutElements';
import { connect } from 'react-redux';
import tft from '../../tfc.png'

const Navbar = ({isAuthenticated}) => {
    // const [loggedIn, setLoggedIn] = useState(localStorage.getItem('access') != null);
    // const [loggedIn, setLoggedIn] = useState(isAuthenticated);
    // console.log(localStorage.getItem('access'));
    // console.log(localStorage.getItem('access') != null);
    // console.log(isAuthenticated);
    return (
        <>
            <Nav >
                <NavLinkIcon to="/">
                    <img src={tft} alt='' style={{ width: "10%", position: 'absolute'}}/>
                </NavLinkIcon>
                
                <NavMenu>
                    <NavLink to='/findstudio'>
                        Find a Studio Near Me
                    </NavLink>
                    <NavLink to='/mapstudio'>
                        Locations
                    </NavLink>
                    <NavLink to='/subscriptions'>
                        Subscription Plan
                    </NavLink>
                    <NavLink to='/studios/search'>
                        Search Studios
                    </NavLink>
                    <NavLink to='/amenities/search'>
                        Search Amenities
                    </NavLink>
                    <NavLink to='/classes/search'>
                        Search Classes
                    </NavLink>
                </ NavMenu>

                {!isAuthenticated ? (
                    <NavBtn>
                    <NavBtnLink to='login'>Login</NavBtnLink>
                    <ContrastedNavBtnLink to='Signup'>Register</ContrastedNavBtnLink>
                    </NavBtn>
                ) : 
                    <NavBtn>
                    <NavLink to='/schedule'>
                        My Schedule
                    </NavLink>
                    <NavBtnLink to='logout'>Logout</NavBtnLink>
                    <ContrastedNavBtnLink to='profile'>User Profile</ContrastedNavBtnLink>
                    </NavBtn>
                }
            </Nav> 
        </>
    )
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps)(Navbar);
