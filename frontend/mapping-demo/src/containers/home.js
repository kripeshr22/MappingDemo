
import React, { useState, useRef, useEffect} from 'react'
import "../styles/main.css"
import "../styles/home.css"

// eslint-disable-next-line import/no-webpack-loader-syntax
import mapboxgl from "!mapbox-gl";

// const accessToken = 'pk.eyJ1Ijoia3JpcGVzaHIiLCJhIjoiY2t0OHg0MDMwMTZzaTJvcTJjYnlvZGFmaCJ9.Dfgb6MDEBqbvraywys_j9g';
const token = process.env.REACT_APP_MAPBOX_ACCESS_TOKEN;
mapboxgl.accessToken = token;
const Home = () => {
    const mapContainer = useRef(null);
    const [markers, setMarkers] = useState([]);
    const getMarkers = async() => {
        try {
            const response = await fetch("/server/testGet/");
            const data = await response.json();
            setMarkers(data["results"]);
        } catch (err) {
            console.log(err.message);
        }
    }
        // await fetch("/server/testGet/", {method: "GET"})
        //     .then(function(response){
        //         return response.json()
        //             .then(function(data){
        //                 console.log("Results of test:");
        //                 console.log(data["results"][0].center_lon);
        //                 console.log(data["results"])
        //
        //                 let resultsArray = data["results"];
        //                 return resultsArray;
        //             })
        //     })
        //     .catch(function(error){
        //         console.log('Request failed', error)
        //     })
    function renderMap() {
        getMarkers();
        console.log("markers", markers);
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            // See style options here: https://docs.mapbox.com/api/maps/#styles
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-118.2437, 34.0522],
            zoom: 12.5,
        });
        map.on('load', function() {
            map.resize()
        });
        map.addControl(new mapboxgl.NavigationControl(), 'top-right');
        // const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
        //     ` <a href="https://thegrovela.com/" target="_blank">The Grove</a>
        // `
        // );
        markers.map(marker => {
            map.addControl(new mapboxgl.Marker()
                .setLngLat([marker.center_lon, marker.center_lat])
                .addTo(map)
                .setPopup(new mapboxgl.Popup({ offset: 25 })
                    .setHTML(`<a>${marker.nettaxablevalue}</a>`))
        )});
        // map.addControl(new mapboxgl.Marker()
        //     .setLngLat([-118.3581, 34.0722])
        //     .addTo(map)
        //     .setPopup(popup));

        // clean up on unmount
        return () => map.remove();
    }
    useEffect(() => {
        renderMap();
    }, []);
        return (
            <div className="home">
                <h1 className="header"> [Project Under Construction] </h1>
            <div className="map">
        <div className="map-container" ref={mapContainer} />
        </div>
        </div>)
}

export default Home;