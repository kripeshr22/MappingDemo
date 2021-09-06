
import React, { useRef, useEffect} from 'react'
import "../styles/main.css"
import "../styles/home.css"
import mapboxgl from 'mapbox-gl';

mapboxgl.accessToken = 'pk.eyJ1Ijoia3JpcGVzaHIiLCJhIjoiY2t0OHg0MDMwMTZzaTJvcTJjYnlvZGFmaCJ9.Dfgb6MDEBqbvraywys_j9g';

const Home = () => {
    const mapContainer = useRef(null);
    useEffect(() => {
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
        map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');

    // clean up on unmount
    return () => map.remove();
  }, []); 
        return (
            <div>
                <h1 className="header">SOME MAP </h1>
            <div className="map">
        <div className="map-container" ref={mapContainer} />
        </div>
        </div>)
}

export default Home;