import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Home from './containers/Home';
import Signup from './containers/Signup';
import Login from './containers/Login';

import { Provider } from 'react-redux';
import store from './store';

import Layout from './hocs/Layout';
import StudioDetail from './containers/StudioDetail';

const App = () => (
  <Provider store={store}>
    <Router>
      <Layout>
        <Routes>
          <Route exact path='/' element={<Home />} />
          <Route exact path='/signup' element={<Signup />} />
          <Route exact path='/login' element={<Login />} />
          <Route exact path='/studios/:id/' element={<StudioDetail />} />
        </Routes>
      </Layout>
    </Router>
  </Provider>
);

export default App;
