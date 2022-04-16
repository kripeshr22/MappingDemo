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
            return data["results"];
        } catch (err) {
            console.log(err.message);
        }
    }

    async function renderMap() {
        const map = new mapboxgl.Map({
            container: mapContainer.current,
            // See style options here: https://docs.mapbox.com/api/maps/#styles
            style: 'mapbox://styles/mapbox/streets-v11?optimize=true',
            center: [-118.2437, 34.0522],
            zoom: 12.5,
        });
        map.on('load', () => {
            map.resize()
            // map.addLayer({
            //     id: 'clusters',
            //     type: 'circle',
            //     source: ,//insert heroku markers,
            //     paint: {
            //         // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
            //         // with three steps to implement three types of circles:
            //         //   * Blue, 20px circles when point count is less than 100
            //         //   * Yellow, 30px circles when point count is between 100 and 750
            //         //   * Pink, 40px circles when point count is greater than or equal to 750
            //         'circle-color': [
            //             'step',
            //             ['get', 'point_count'],
            //             '#51bbd6',
            //             100,
            //             '#f1f075',
            //             750,
            //             '#f28cb1'
            //         ],
            //         'circle-radius': [
            //             'step',
            //             ['get', 'point_count'],
            //             20,
            //             100,
            //             30,
            //             750,
            //             40
            //         ]
            //     }
            // });
            // Add a new source from our GeoJSON data and
            // set the 'cluster' option to true. GL-JS will
            // add the point_count property to your source data.
            // map.addSource('earthquakes', {
            //     type: 'geojson',
            //     // Point to GeoJSON data. This example visualizes all M1.0+ earthquakes
            //     // from 12/22/15 to 1/21/16 as logged by USGS' Earthquake hazards program.
            //     // data: 'https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson',
            //     data: 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ca_california_zip_codes_geo.min.json',
            //     cluster: true,
            //     clusterMaxZoom: 14, // Max zoom to cluster points on
            //     clusterRadius: 50 // Radius of each cluster when clustering points (defaults to 50)
            // });
            //
            // map.addLayer({
            //     id: 'clusters',
            //     type: 'circle',
            //     source: 'earthquakes',
            //     filter: ['has', 'point_count'],
            //     paint: {
            // // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
            // // with three steps to implement three types of circles:
            // //   * Blue, 20px circles when point count is less than 100
            // //   * Yellow, 30px circles when point count is between 100 and 750
            // //   * Pink, 40px circles when point count is greater than or equal to 750
            //         'circle-color': [
            //             'step',
            //             ['get', 'point_x'],
            //             '#51bbd6',
            //             100,
            //             '#f1f075',
            //             750,
            //             '#f28cb1'
            //         ],
            //         'circle-radius': [
            //             'step',
            //             ['get', 'point_x'],
            //             20,
            //             100,
            //             30,
            //             750,
            //             40
            //         ]
            //     }
            // });
            //
            // map.addLayer({
            //     id: 'cluster-count',
            //     type: 'symbol',
            //     source: 'earthquakes',
            //     filter: ['has', 'point_x'],
            //     layout: {
            //         'text-field': '{point_count_abbreviated}',
            //         'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
            //         'text-size': 12
            //     }
            // });
            //
            // map.addLayer({
            //     id: 'unclustered-point',
            //     type: 'circle',
            //     source: 'earthquakes',
            //     filter: ['!', ['has', 'point_x']],
            //     paint: {
            //         'circle-color': '#11b4da',
            //         'circle-radius': 4,
            //         'circle-stroke-width': 1,
            //         'circle-stroke-color': '#fff'
            //     }
            // });
        });
        map.addControl(new mapboxgl.NavigationControl(), 'top-right');

        await markers.splice(-50).forEach(marker => {
            let subsidy = (marker.estimated_value.replace("$", "").replaceAll(",", "")) -
                (marker.recorded_value.replace("$", "").replaceAll(",", ""));
            subsidy = subsidy / marker.sqft;
            const el = document.createElement('div');
            el.className = 'marker';
            if (subsidy >= 50) {
                el.className += ' red'
            } else {
                el.className += ' green'
            }

            new mapboxgl.Marker(el)
                .setLngLat([marker.long, marker.lat])
                .addTo(map)
                .setPopup(new mapboxgl.Popup({offset: 25})
                    .setHTML(`<h4>Address: ${marker.address} <br/>${marker.sqft} sfqt </h4>
                                <h4>Assessed value: ${marker.recorded_value}</h4>
                                <h4>Estimated value: ${marker.estimated_value}</h4>
                                <h3>Estimated subsidy per sqft: ${"$" + new Intl.NumberFormat().format(subsidy)}</h3>`));
        });

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
            <div className="map">
                <div className="map-container" ref={mapContainer}/>
            </div>
        </div>)
    // return (
    //     <div>THANK YOU FOR VISITING!</div>
    // )
}

export default Home;