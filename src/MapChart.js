import React, {useEffect, useState} from "react";
import ReactDOM from 'react-dom';
import { Alert } from 'react-st-modal';

import { geoCentroid } from "d3-geo";
import {
    ComposableMap,
    Geographies,
    Geography,
    Marker,
    Annotation
} from "react-simple-maps";

import allStates from "./data/allstates.json";

const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

const highlight = "#f5821f";

const colors = ["#0e3b5e", "#0077c9", "#43b4ff", "#c0e6ff"];



const hexToRgb = hex => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result
        ? [
            parseInt(result[1], 16),
            parseInt(result[2], 16),
            parseInt(result[3], 16)
        ]
        : null;
};

const getTextColor = rgb => {
    const o = Math.round(
        (parseInt(rgb[0], 10) * 299 +
            parseInt(rgb[1], 10) * 587 +
            parseInt(rgb[2], 10) * 114) /
        1000
    );
    return o > 125 ? "#444444" : "#FFFFFF";
};

const offsets = {
    VT: [50, -8],
    NH: [34, 2],
    MA: [30, -1],
    RI: [28, 2],
    CT: [35, 10],
    NJ: [34, 1],
    DE: [33, 0],
    MD: [47, 10],
    DC: [49, 21]
};

const statesWithColors = allStates.map(state => ({
    fill: colors[(Math.random() * (colors.length - 1)).toFixed()],
    ...state
}));

const getData = (id) => {
    fetch('/api/plants/'.concat(id)).then(res => res.json()).then(data => {

        return Alert('Plant count :'.concat(JSON.stringify(data["abs_value"]).concat('\t')).
        concat("Percentage by State: ").concat(JSON.stringify(data["percent"])) , "State of :".concat(id));
    });

}

const MapChart = () => {
    const [activeGeo, setActiveGeo] = useState("");

    return (
        <ComposableMap projection="geoAlbersUsa">
            <Geographies geography={geoUrl} id="test">
                {({ geographies }) => (
                    <>
                        {geographies.map(geo => {
                            const cur = statesWithColors.find(s => s.val === geo.id);
                            return (
                                <Geography
                                    key={geo.rsmKey}
                                    geography={geo}
                                    onClick={() => getData(cur.id)}
                                    onMouseEnter={() => setActiveGeo(geo.id)}
                                    onMouseLeave={() => setActiveGeo(null)}
                                    fill={geo.id === activeGeo ? highlight : cur.fill}
                                    stroke="#FFFFFF"
                                />
                            );
                        })}
                        {geographies.map(geo => {
                            const centroid = geoCentroid(geo);
                            const cur = statesWithColors.find(s => s.val === geo.id);
                            const textFill = getTextColor(hexToRgb(cur.fill));
                            return (
                                <g key={geo.rsmKey + "-name"}>
                                    {cur &&
                                    centroid[0] > -160 &&
                                    centroid[0] < -67 &&
                                    (Object.keys(offsets).indexOf(cur.id) === -1 ? (
                                        <Marker coordinates={centroid}>
                                            <text
                                                y="2"
                                                fontSize={14}
                                                textAnchor="middle"
                                                onMouseEnter={() => setActiveGeo(geo.id)}
                                                onMouseLeave={() => setActiveGeo(null)}
                                                style={{ cursor: "pointer" }}
                                                fill={geo.id === activeGeo ? "#FFFFFF" : textFill}
                                            >
                                                {cur.id}
                                            </text>
                                        </Marker>
                                    ) : (
                                        <Annotation
                                            subject={centroid}
                                            dx={offsets[cur.id][0]}
                                            dy={offsets[cur.id][1]}
                                        >
                                            <text
                                                x={4}
                                                fontSize={14}
                                                alignmentBaseline="middle"
                                                onMouseEnter={() => setActiveGeo(geo.id)}
                                                onMouseLeave={() => setActiveGeo(null)}
                                                style={{ cursor: "pointer" }}
                                            >
                                                {cur.id}
                                            </text>
                                        </Annotation>
                                    ))}
                                </g>
                            );
                        })}
                    </>
                )}
            </Geographies>
        </ComposableMap>
    );
};

export default MapChart;