import React, { useState, useRef } from "react";
import useSwr from "swr";
import ReactMapGL, { Marker, FlyToInterpolator } from "react-map-gl";
import useSupercluster from "use-supercluster";
import "../styles/main.css"
import "../styles/home.css"

const fetcher = (...args) => fetch(...args).then(response => response.json());
const heroku = process.env.REACT_APP_API_URL;
export default function App() {
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
    const crimes = data && !error ? data["results"] : [];
    console.log('crimes', crimes)
    const points = crimes.map(crime => ({
        type: "Feature",
        properties: { cluster: false, crimeId: crime.prop_id, category: crime.zipcode },
        geometry: {
            type: "Point",
            coordinates: [
                parseFloat(crime.long),
                parseFloat(crime.lat)
            ]
        }
    }));
    console.log('points', points);

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
                                    onClick={() => {
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
                                    }}
                                >
                                    {pointCount}
                                </div>
                            </Marker>
                        );
                    }

                    return (
                        <Marker
                            key={`crime-${cluster.properties.crimeId}`}
                            latitude={latitude}
                            longitude={longitude}
                        >
                            <button className="crime-marker">
                                <img src="/warehouse.png" alt="commercial properties" />
                            </button>
                        </Marker>
                    );
                })}
            </ReactMapGL>
        </div>
    );
}