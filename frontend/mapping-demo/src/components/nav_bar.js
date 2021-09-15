import React from 'react'

import {NavLink} from 'react-router-dom'

import '../styles/nav_bar.css'

class NavigationBar extends React.Component {

    render() {
        var active = {
            fontWeight: 'bold',
            color: '#6b000e'
        }
        return (
            <div>
                <ul>
                    <li><NavLink to="/home" activeStyle={active}>Home</NavLink></li>
                    <li><NavLink to="/about" activeStyle={active}>About</NavLink></li>
                    <li><NavLink to="/map2" activeStyle={active}>Map2</NavLink></li>
                </ul>
            </div>
        )
    }
}

export default NavigationBar;