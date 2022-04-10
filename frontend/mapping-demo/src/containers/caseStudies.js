import React, {useState, useRef, useEffect} from 'react'
import "../styles/main.css"
import "../styles/home.css"

// eslint-disable-next-line import/no-webpack-loader-syntax
import mapboxgl from "!mapbox-gl";
import CaseStudyDesign1 from "../components/CaseStudyDesign1";
import ReactDOM from "react-dom";
import caseStudies from "../components/caseStudiesData";

const token = process.env.REACT_APP_MAPBOX_ACCESS_TOKEN;
mapboxgl.accessToken = token;


const CaseStudies = () => {
    const mapContainer = useRef(null);

    async function renderMap() {
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            // See style options here: https://docs.mapbox.com/api/maps/#styles
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-118.2437, 34.0522],
            zoom: 12.5,
        });
        map.on('load', function () {
            map.resize()
        });
        map.addControl(new mapboxgl.NavigationControl(), 'top-right');

        await caseStudies.forEach(cs => {
            const placeholder = document.createElement('div');
            ReactDOM.render(<CaseStudyDesign1 properties={cs} />, placeholder);

            const currentMarker = new mapboxgl.Marker()
                .setLngLat([cs.center_lon, cs.center_lat])
                .addTo(map)
                .setPopup(new mapboxgl.Popup({offset: 25})
                    .setDOMContent(placeholder));

            currentMarker.getElement().addEventListener('click', () => {
                console.log("Clicked")})
        })

        // clean up on unmount
        return () => map.remove();
    }

    useEffect(() => {
        renderMap();
    });

    return (
        <div className="home">
            <h1 className="header"> [Project Under Construction] </h1>
            <div className="map">
                <div className="map-container" ref={mapContainer}/>
            </div>
        </div>)
}

export default CaseStudies;