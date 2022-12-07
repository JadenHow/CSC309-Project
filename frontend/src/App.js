import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Home from './containers/Home';
import Signup from './containers/Signup';
import Login from './containers/Login';
import Logout from './containers/Logout';
import EditUser from './containers/EditUser';
import StudioSearch from './components/StudioSearch';
import SubscriptionList from './containers/Subscriptions';
import ClassSchedule from './containers/ClassSchedule';

import { Provider } from 'react-redux';
import store from './store';

import Layout from './hocs/Layout';
import StudioDetail from './containers/StudioDetail';
//import Subscription from './components/SubscriptionDetail';

const App = () => (
  <Provider store={store}>
    <Router>
      <Layout>
        <Routes>
          <Route exact path='/' element={<Home />} />
          <Route exact path='/signup' element={<Signup />} />
          <Route exact path='/login' element={<Login />} />
          <Route exact path='/logout' element={<Logout />} />
          <Route exact path='/studios/:id/' element={<div><StudioDetail /><StudioSearch /></div>} />
          <Route exact path='/edit' element={<EditUser />} />
          <Route exact path='/subscriptions' element={<SubscriptionList />} />
          <Route exact path='/schedule' element={<ClassSchedule />} />
        </Routes>
      </Layout>
    </Router>
  </Provider>
);

export default App;
