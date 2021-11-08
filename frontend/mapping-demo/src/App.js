import React from 'react'
import './App.css';

import Home from './containers/home'
import About from './containers/about'
import Map2 from './containers/map2'

import NavigationBar from './components/nav_bar'
import { Route, Redirect, Switch, HashRouter } from 'react-router-dom'

function App() {
    function testHerokuPg(){
        fetch("/server/testHerokuPg/", {method: "GET"})
            .then(function(response){
                return response.json()
                    .then(function(data){
                        console.log("Results of test:");
                        console.log(data);

                        let resultsArray = data["results"]
                        document.getElementById("outputBox").innerHTML = `Retrived id=${resultsArray[0].id}, name=${resultsArray[0].name}`;
                    })
            })
            .catch(function(error){
                console.log('Request failed', error)
            })
    }
  return (
    <div className ="app">
        <button onClick={() => {testHerokuPg()}}>Test Heroku Pg</button>
      <HashRouter>
      <NavigationBar></NavigationBar>
      <Switch>
        <Route exact path='/' render={() => (
          <Redirect to='/home'/>
        )}/>
        <Route path='/home' component={Home}></Route>
        <Route path='/map2' component={Map2}></Route>
        <Route path='/about' component={About}></Route>
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
