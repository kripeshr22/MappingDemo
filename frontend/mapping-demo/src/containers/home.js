import React, {useState, useRef, useEffect} from 'react'
import "../styles/main.css"
import "../styles/home.css"

// eslint-disable-next-line import/no-webpack-loader-syntax
import mapboxgl from "!mapbox-gl";
import CaseStudyDesign1 from "../components/CaseStudyDesign1";
import ReactDOM from "react-dom";

const token = process.env.REACT_APP_MAPBOX_ACCESS_TOKEN;
const heroku = process.env.REACT_APP_API_URL;
mapboxgl.accessToken = token;

const initialProperties = [
    {
        city1: "Santa Clarita",
        address1: "21070 Centre Point Parkway",
        address1line2: "Santa Clarita CA 91350",
        landvalue1: 1.60,
        sqft1: 6664,
        photo1: "https://images1.loopnet.com/i2/zg5NPRe5Ws9ia3I-ldrmJyhR36o3QFvjYT5VIJzxf6w/112/image.jpg",
        city2: "Santa Clarita",
        address2: "26415 Summit Circle",
        address2line2: "Santa Clarita CA 91350",
        landvalue2: 140,
        sqft2: 7863,
        photo2: "https://images1.loopnet.com/i2/isy0EBCPWTwEHbih2zzgbauKXR_5Kg5j4jC7064O5-E/110/image.jpg",
        center_lat: -118.2437,
        center_lon: 34.0522,
    }
    ];



const Home = () => {
    const mapContainer = useRef(null);
    const [markers, setMarkers] = useState([]);
    const [popup, setPopup] = useState(null);
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
        await markers.forEach(marker => {

            const placeholder = document.createElement('div');
            ReactDOM.render(<CaseStudyDesign1 properties={initialProperties[0]} />, placeholder);

            const currentMarker = new mapboxgl.Marker()
                .setLngLat([marker.center_lon, marker.center_lat])
                .addTo(map)
                .setPopup(new mapboxgl.Popup({offset: 25})
                    .setDOMContent(placeholder));
                    // .setHTML(`<a>${marker.nettaxablevalue}</a>`));


            // map.addControl(mark)
            currentMarker.getElement().addEventListener('click', () => {
                console.log("Clicked");
                // setPopup(initialProperties[0]);
                console.log(marker)})
        });



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