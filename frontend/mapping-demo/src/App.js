import React from 'react'
import './App.css';

import Home from './containers/home'
import About from './containers/about'
import Map2 from './containers/map2'

import NavigationBar from './components/nav_bar'
import { Route, Redirect, Switch, HashRouter } from 'react-router-dom'


function App() {
  return (
    <div className ="app">
      <HashRouter>
      <NavigationBar></NavigationBar>
      <Switch>
        <Route exact path='/' render={() => (
          <Redirect to='/home'/>
        )}/>
        <Route path='/home' component={Home}></Route>
        <Route path='/about' component={About}></Route>
        <Route path='/map2' component={Map2}></Route>
        <Home>
        </Home>
        <About></About>
        <Map2></Map2>
      </Switch>
      </HashRouter>
    </div>
  );
}

export default App;
