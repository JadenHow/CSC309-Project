import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Home from './containers/Home/Home';
import Signup from './containers/Signup/Signup';
import Login from './containers/Login/Login';
import Logout from './containers/Logout/Logout';
import EditUser from './containers/EditUser/EditUser';
import { StudioSearch, AmenitiesSearch, ClassInstanceSearch } from './components/Search/StudioSearch';
import SubscriptionList from './containers/Subscriptions/Subscriptions';
import ClassSchedule from './containers/ClassSchedule/ClassSchedule';
import FindStudio from './containers/FindStudio/FindStudio';
import PaymentHistory from './containers/PaymentHistory/PaymentHistory';
import UserProfile from './containers/UserProfile/UserProfile';
import MapComponent1 from './components/Map/MapComponent1';

import { Provider } from 'react-redux';
import store from './store';

import Layout from './hocs/Layout';
import StudioDetail from './containers/StudioDetail/StudioDetail';
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
          <Route exact path='/studios/:id/' element={<StudioDetail />} />
          <Route exact path='/edit' element={<EditUser />} />
          <Route exact path='/subscriptions' element={<SubscriptionList />} />
          <Route exact path='/schedule' element={<ClassSchedule />} />
          <Route exact path='/studios/search' element={<StudioSearch />} />
          <Route exact path='/amenities/search' element={<AmenitiesSearch />} />
          <Route exact path='/classes/search' element={<ClassInstanceSearch />} />
          <Route exact path='/findstudio' element={<FindStudio />} />
          <Route exact path='/history' element={<PaymentHistory />} />
          <Route exact path='/profile' element={<UserProfile />} />
          <Route exact path='/mapstudio' element={<MapComponent1 />} />
        </Routes>
      </Layout>
    </Router>
  </Provider>
);

export default App;
