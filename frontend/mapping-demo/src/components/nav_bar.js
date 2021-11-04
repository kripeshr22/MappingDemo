import React from 'react'

import {NavLink} from 'react-router-dom'

import '../styles/nav_bar.css'

class NavigationBar extends React.Component {

    render() {
        var active = {
            fontWeight: 'bold',
            color: '#A2C613'
        }
        return (
            <div className="navbar">
                <ul>
                    <li><a href="https://techequitycollaborative.org/" target="_blank" rel="noreferrer">[TITLE]</a></li>
                    <li><NavLink to="/home" activeStyle={active}>HOME</NavLink></li>
                    <li><NavLink to="/map2" activeStyle={active}>FACTS</NavLink></li>
                    <li><NavLink to="/about" activeStyle={active}>ABOUT</NavLink></li>
                </ul>
            </div>
        )
    }
}

export default NavigationBar;