import React from 'react'
import "../styles/main.css"
import "../styles/about.css"

const About = () => {
    return (
        <div className="about">
            <h1 className="center">ABOUT</h1>
            <div className="card">
            <p class="answer">This website is part of a project by HMC TechEquity Collaboartive Clinic 21' Team.</p>
            <p>
                <li><a href="https://github.com/annadsinger0" class="answer">Anna Singer</a></li>
                <li><a href="https://github.com/arunramakrishna" class="answer">Arun Ramakrishna</a></li>
                <li><a href="https://github.com/mariesateo" class="answer">Mariesa Teo</a></li>
                <li><a href="https://github.com/kripeshr22" class="answer">Kripesh Ranabhat</a></li>
                <li><a href="https://github.com/yurynamgung" class="answer">Yury Namgung</a></li></p>
            <br/>
            <a href="https://github.com/kripeshr22/MappingDemo">GITHUB</a>
            </div>
        </div>
    )}

export default About;