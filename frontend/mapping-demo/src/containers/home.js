import React, {useState, useRef, useEffect} from 'react'
import "../styles/main.css"
import "../styles/home.css"

// eslint-disable-next-line import/no-webpack-loader-syntax
import mapboxgl from "!mapbox-gl";
import CaseStudyDesign1 from "../components/CaseStudyDesign1";
import ReactDOM from "react-dom";
import caseStudies from "../components/caseStudiesData";

const token = process.env.REACT_APP_MAPBOX_ACCESS_TOKEN;
const heroku = process.env.REACT_APP_API_URL;
mapboxgl.accessToken = token;





const Home = () => {
    const mapContainer = useRef(null);
    const [markers, setMarkers] = useState([]);
    const fetchMarkers = async () => {
        try {
            const response = await fetch(heroku+"server/testGet/", {
                    headers : {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
            });
            const data = await response.json();
            return data["results"];
        } catch (err) {
            console.log(err.message);
        }
    }

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
        // const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
        //     ` <a href="https://thegrovela.com/" target="_blank">The Grove</a>
        // `
        // );
        /* await markers.forEach(marker => {
            // remove css styling for this one to look good
            const currentMarker = new mapboxgl.Marker()
                .setLngLat([marker.center_lon, marker.center_lat])
                .addTo(map)
                .setPopup(new mapboxgl.Popup({offset: 25})
                    .setHTML(`<a>${marker.nettaxablevalue}</a>`));


            // map.addControl(mark)
        }); */

        await caseStudies.forEach(cs => {
            const placeholder = document.createElement('div');
            ReactDOM.render(<CaseStudyDesign1 properties={cs} />, placeholder);

            const currentMarker = new mapboxgl.Marker()
                .setLngLat([cs.center_lon, cs.center_lat])
                .addTo(map)
                .setPopup(new mapboxgl.Popup({offset: 25})
                    .setDOMContent(placeholder));
            // .setHTML(`<a>${marker.nettaxablevalue}</a>`));


            // map.addControl(mark)
            currentMarker.getElement().addEventListener('click', () => {
                console.log("Clicked")})
        })



        // const marker = new MapboxGl.Popup()
        //     .setDOMContent(placeholder)
        //     .setLngLat({lng: lng, lat: lat})
        //     .addTo(map);

        // map.addControl(new mapboxgl.Marker()
        //     .setLngLat([-118.3581, 34.0722])
        //     .addTo(map)
        //     .setPopup(popup));

        // clean up on unmount
        return () => map.remove();
    }

    useEffect(() => {
        const getMarkers = async () => {
            let data = await fetchMarkers();
            await setMarkers(data);
        }
        getMarkers();
    }, []);

    useEffect(() => {
        renderMap();
    });

    return (
        <div className="home">
            <h1 className="header"> [Project Under Construction] </h1>
            {/*{(popup !== null) ? <CaseStudyDesign1 properties={initialProperties[0]} /> : null}*/}
            <div className="map">
                <div className="map-container" ref={mapContainer}/>
            </div>
        </div>)
}

export default Home;