import { useEffect } from "react";
import L from "leaflet";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import "leaflet-routing-machine";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";
import "leaflet-control-geocoder/dist/Control.Geocoder.js";
import { useMap } from "react-leaflet";
import { useRoutingContext } from '../../context/context';

L.Marker.prototype.options.icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// icons from https://github.com/pointhi/leaflet-color-markers
const sourceIcon = L.icon({
  iconUrl: 'https://toppng.com/uploads/preview/map-marker-pin-icon-symbol-vector-black-place-icon-11553495811735w0ozyjq.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const destinationIcon = L.icon({
  iconUrl: 'https://toppng.com/uploads/preview/map-marker-pin-icon-symbol-vector-black-place-icon-11553495811735w0ozyjq.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function Routing() {
  const map = useMap();
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo]= useRoutingContext();
  const markers = routingInfo.markers;
  const graph = routingInfo.graph;
  const sourceCoords = routingInfo.sourceCoords;
  const sourceName = routingInfo.sourceName;
  const destinationCoords = routingInfo.destinationCoords;
  const destinationName = routingInfo.destinationName;

  console.log(routingInfo);
  // add optimal route onto map
  useEffect(() => {
    if (!map || !graph) {
      markers.current.forEach(marker => map.removeLayer(marker));
      markers.current.length = 0;
      return;
    };
    const nodesForRoute = graph.map((coordinates) => [coordinates.y, coordinates.x])
    // set markers
    markers.current.forEach(marker => map.removeLayer(marker));
    markers.current.length = 0;
    const route = L.polyline(nodesForRoute);

    route.setStyle({
      color: 'black'
    });
    map.addLayer(route);
    markers.current.push(route);
    const sourceMarker = L.marker(nodesForRoute[0], {icon: sourceIcon}).bindPopup(sourceName);
    map.addLayer(sourceMarker);
    const destinationMarker = L.marker(nodesForRoute[nodesForRoute.length - 1], {icon: destinationIcon}).bindPopup(destinationName);
    map.addLayer(destinationMarker);
    markers.current.push(sourceMarker);
    markers.current.push(destinationMarker);
  }, [destinationName, graph, map, markers, sourceName]);

  // auto-focus map
  useEffect(() => {
    const boundary = [];
    const newMarkers = [];

    markers.current.forEach(marker => map.removeLayer(marker));
    markers.current.length = 0
    console.log(markers)
    if (sourceCoords) {
      const sourceMarker = L.marker(sourceCoords, {icon: sourceIcon}).bindPopup(sourceName);
      newMarkers.concat(sourceMarker);
      markers.current.push(sourceMarker);
      map.addLayer(sourceMarker);
      boundary.push(sourceCoords)
    }
    if (destinationCoords) {
      const destinationMarker = L.marker(destinationCoords, {icon: destinationIcon}).bindPopup(destinationName);
      newMarkers.concat(destinationMarker);
      markers.current.push(destinationMarker);
      map.addLayer(destinationMarker);
      boundary.push(destinationCoords)
    }
    if (boundary.length !== 0) {
      map.fitBounds(L.latLngBounds([boundary]));
    }
  }, [sourceCoords, destinationCoords, map, sourceName, destinationName, markers]);
  
  return null;
}
