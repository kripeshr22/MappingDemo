import React, { useState, useRef } from "react";
import useSwr from "swr";
import ReactMapGL, { Marker, NavigationControl, Popup, FullscreenControl,
    ScaleControl,
    GeolocateControl, FlyToInterpolator } from "react-map-gl";
import useSupercluster from "use-supercluster";

import "../styles/main.css"
import "../styles/home.css"

const fetcher = (...args) => fetch(...args).then(response => response.json());
const heroku = process.env.REACT_APP_API_URL;
export default function App() {
    const [showPopup, setShowPopup] = useState(false);
    const[popupInfo, setPopupInfo] = useState('');
    const [viewport, setViewport] = useState({
        latitude: 34.0522,
        longitude: -118.2437,
        width: "100vw",
        height: "100vh",
        zoom: 12
    });
    const mapRef = useRef();

    const url =
        heroku+"server/testGet";
    const { data, error } = useSwr(url, { fetcher });
    const parcels = data && !error ? data["results"] : [];
    console.log('parcels',parcels);
    const points = parcels.map(parcel => ({
        type: "Feature",
        properties: { cluster: false, prop_id: parcel.prop_id, zipcode: parcel.zipcode,
        address: parcel.address, sqft: parcel.sqft, assd_value: parcel.recorded_value,
        estmd_value: parcel.estimated_value},
        geometry: {
            type: "Point",
            coordinates: [
                parseFloat(parcel.long),
                parseFloat(parcel.lat)
            ]
        }
    }));
    console.log('points',points);

    const bounds = mapRef.current
        ? mapRef.current
            .getMap()
            .getBounds()
            .toArray()
            .flat()
        : null;

    const { clusters, supercluster } = useSupercluster({
        points,
        bounds,
        zoom: viewport.zoom,
        options: { radius: 75, maxZoom: 20 }
    });

    return (
        <div>
            <ReactMapGL
                {...viewport}
                maxZoom={20}
                mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
                onViewportChange={newViewport => {
                    setViewport({ ...newViewport });
                }}
                ref={mapRef}
            >
                <GeolocateControl position="top-right" />
                <FullscreenControl/>
                <NavigationControl position="top-right" />
                <ScaleControl unit={'imperial'}/>
                {clusters.map(cluster => {
                    const [longitude, latitude] = cluster.geometry.coordinates;
                    const {
                        cluster: isCluster,
                        point_count: pointCount
                    } = cluster.properties;

                    if (isCluster) {
                        return (
                            <Marker
                                key={`cluster-${cluster.id}`}
                                latitude={latitude}
                                longitude={longitude}
                            >
                                <div
                                    className="cluster-marker"
                                    style={{
                                        width: `${10 + (pointCount / points.length) * 20}px`,
                                        height: `${10 + (pointCount / points.length) * 20}px`
                                    }}
                                    eventHandlers={{
                                        click: () => {
                                            const expansionZoom = Math.min(
                                                supercluster.getClusterExpansionZoom(cluster.id),
                                                20
                                            );
                                            setViewport({
                                                ...viewport,
                                                latitude,
                                                longitude,
                                                zoom: expansionZoom,
                                                transitionInterpolator: new FlyToInterpolator({
                                                    speed: 2
                                                }),
                                                transitionDuration: "auto"
                                            });
                                        }
                                    }}
                                >
                                    {pointCount}
                                </div>
                            </Marker>
                        );
                    }

                    return (
                        <div>
                        <Marker
                            key={`crime-${cluster.properties.prop_id}`}
                            latitude={latitude}
                            longitude={longitude}
                            onClick={() => {setShowPopup(true);
                            setPopupInfo(`<h4>Address: ${cluster.properties.address} <br/>${cluster.properties.sqft} sfqt </h4>
                                <h4>Assessed value: ${cluster.properties.assd_value}</h4>
                                <h4>Estimated value: ${cluster.properties.estmd_value}</h4>`)}}
                        >
                            <button className="crime-marker">
                                <img src="/warehouse.png" alt="commercial properties" />
                            </button>
                        </Marker>
                    {showPopup && <Popup longitude={longitude} latitude={latitude}
                    onClose={() => setShowPopup(false)}>{popupInfo}</Popup>}
                        </div>
                    );
                })}
            </ReactMapGL>
        </div>
    );
}