import React from 'react'

import {NavLink} from 'react-router-dom'

import '../styles/nav_bar.css'

class NavigationBar extends React.Component {

    render() {
        var active = {
            fontWeight: 'bold',
            color: '#14adb3'
        }
        return (
            <div>
                <ul>
                    <li><NavLink to="/home" activeStyle={active}>Start</NavLink></li>
                    <li><NavLink to="/about" activeStyle={active}>TBD</NavLink></li>
                    <li><NavLink to="/map2" activeStyle={active}>Map! Map! Map!</NavLink></li>
                </ul>
            </div>
        )
    }
}

export default NavigationBar;