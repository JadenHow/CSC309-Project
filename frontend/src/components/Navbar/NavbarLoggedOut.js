import React, { useState } from 'react'
import { Nav, NavLink, NavMenu, NavBtn, NavBtnLink, ContrastedNavBtnLink, OpenLinksButton, NavbarExtendedContainer, NavLinkExtended } from './NavbarLoggedOutElements';
import {FaBars, FaTimes} from 'react-icons/fa'
import { connect } from 'react-redux';
import getUserLocation from '../../containers/FindStudio/FindStudio';
import tft from '../../tfc.png'

const Navbar = ({isAuthenticated}) => {
    const [extendNavbar, setExtendNavbar] = useState(false);
    // const [loggedIn, setLoggedIn] = useState(localStorage.getItem('access') != null);
    // const [loggedIn, setLoggedIn] = useState(isAuthenticated);
    // console.log(localStorage.getItem('access'));
    // console.log(localStorage.getItem('access') != null);
    // console.log(isAuthenticated);
    return (
        <>
            <Nav extendNavbar={extendNavbar}>
                <NavLink to="/">
                    <img src={tft} alt='' style={{ width: "10%", position: 'absolute'}}/>
                </NavLink>

                <OpenLinksButton onClick={() => {setExtendNavbar((curr) => (!curr))}}>
                    {extendNavbar ? <FaTimes/> : <FaBars />}
                </OpenLinksButton>

                <NavMenu>
                    <NavLink to='/'>
                        Home
                    </NavLink>
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
                    <NavBtnLink to='logout'>Logout</NavBtnLink>
                    <ContrastedNavBtnLink to='profile'>User Profile</ContrastedNavBtnLink>
                    </NavBtn>
                }


                {extendNavbar && !isAuthenticated && (
                    <NavbarExtendedContainer>
                        <NavLinkExtended to='/'>
                            Home
                        </NavLinkExtended>
                        <NavLinkExtended to='/studios'>
                            Studios
                        </NavLinkExtended>
                        <NavLinkExtended to='/subscriptions'>
                            Subscription Plan
                        </NavLinkExtended>
                        
                        <ContrastedNavBtnLink to='login'>Login</ContrastedNavBtnLink>
                        <ContrastedNavBtnLink to='signup'>Register</ContrastedNavBtnLink>
                    </NavbarExtendedContainer>
                )}

                {extendNavbar && isAuthenticated && (
                    <NavbarExtendedContainer>
                        <NavLinkExtended to='/'>
                            Home
                        </NavLinkExtended>
                        <NavLinkExtended to='/studios'>
                            Studios
                        </NavLinkExtended>
                        <NavLinkExtended to='/subscriptions'>
                            Subscription Plan
                        </NavLinkExtended>
                        
                        <ContrastedNavBtnLink to='logout'>Logout</ContrastedNavBtnLink>
                        <ContrastedNavBtnLink to='signup'>User Profile</ContrastedNavBtnLink>
                    </NavbarExtendedContainer>
                )}
            </Nav> 
        </>
    )
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps)(Navbar);
