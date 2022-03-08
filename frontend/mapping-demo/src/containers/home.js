import React, {useState, useRef, useEffect} from 'react'
import "../styles/main.css"
import "../styles/home.css"

// eslint-disable-next-line import/no-webpack-loader-syntax
import mapboxgl from "!mapbox-gl";

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
            console.log(token)
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
        map.on('load', function (){            
            //  map.addSource('locality-2', {
            //     type: 'vector',
            //     url: 'mapbox://mapbox.boundaries-loc2-v3'
            //   });
            //  map.addLayer(
            //     {
            //       'id' : 'locality-2-fill',
            //       'type': 'fill',
            //       'source': 'locality-2',
            //       'source-layer': 'boundaries_locality_2',
            //       'paint': {
            //         'fill-color': '#00ffff'
            //       }
            //    },
                
                // This final argument indicates that we want to add the Boundaries layer
                // before the `waterway-label` layer that is in the map from the Mapbox
                // Light style. This ensures the admin polygons will be rendered on top of
                // the
            //    'waterway-label'
            //  );
                map.addSource('LA', {
                    type: 'geojson',
                    // Use a URL for the value for the `data` property.
                    data: 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ca_california_zip_codes_geo.min.json'
                    });
                     
                map.addLayer({
                    'id': 'LA-layer',
                    'type': 'line',
                    'source': 'LA',
                    'paint': {
                        'line-color': 'green',
                        //'line-dasharray': 0.5,
                        'line-gap-width': 0.1
                    }
                    });
            map.resize()

        });
        map.addControl(new mapboxgl.NavigationControl(), 'top-right');
        // const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
        //     ` <a href="https://thegrovela.com/" target="_blank">The Grove</a>
        // `
        // );
        await markers.forEach(marker => {
                map.addControl(new mapboxgl.Marker()
                    .setLngLat([marker.center_lon, marker.center_lat])
                    .addTo(map)
                    .setPopup(new mapboxgl.Popup({offset: 25})
                        .setHTML(`<a>${marker.nettaxablevalue}</a>`))
                )
        });
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
            <h1 className="header"> [Prop 13] </h1>
            <div className="map">
                <div className="map-container" ref={mapContainer}/>
            </div>
        </div>)
}

export default Home;