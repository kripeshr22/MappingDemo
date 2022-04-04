import * as React from 'react'
import "../styles/main.css"
import "../styles/map2.css"
import ReactMapGL, {Marker} from 'react-map-gl'

const MAPBOX_TOKEN = 'token-token-token-la-la-la';
const Map2 = () => {
    let [viewport, setViewport] = React.useState({
        /* I wanted to look at Seattle instead - XS */
        latitude: 47.6062,
        longitude: -122.3321,
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
                <Marker latitude={47.6065} longitude={-122.3347} offsetTop={(-viewport.zoom*10)/2}>
                    <img src={process.env.PUBLIC_URL+'/pointer2.png'}
                    height= {30}
                    alt="marker...somewhere"></img>
                </Marker>
            </ReactMapGL>
            
        </div>
    )
}

export default Map2;