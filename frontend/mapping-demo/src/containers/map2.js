import * as React from 'react'
import "../styles/main.css"
import "../styles/map2.css"
import ReactMapGL, {Marker} from 'react-map-gl'

const MAPBOX_TOKEN = 'pk.eyJ1Ijoia3JpcGVzaHIiLCJhIjoiY2t0OHg0MDMwMTZzaTJvcTJjYnlvZGFmaCJ9.Dfgb6MDEBqbvraywys_j9g';
const Map2 = () => {
    let [viewport, setViewport] = React.useState({
        latitude: 34.0522,
        longitude: -118.2437,
        zoom: 8,
        width: window.innerWidth,
        height: window.innerHeight,
        
    });

    return (
        <div>
            <h1>MAP TEST</h1>
            <ReactMapGL 
            mapStyle={'mapbox://styles/mapbox/dark-v9'}
            mapboxApiAccessToken = {MAPBOX_TOKEN}
            {...viewport} 
            onViewportChange={(newView) => setViewport(newView)}>
                <Marker latitude={34.0722} longitude={-118.3581} offsetTop={(-viewport.zoom*10)/2}>
                    <img src={process.env.PUBLIC_URL+'/pointer.png'}
                    height= {30}
                    alt="marker on grove"></img>
                </Marker>
            </ReactMapGL>
            
        </div>
    )
}

export default Map2;