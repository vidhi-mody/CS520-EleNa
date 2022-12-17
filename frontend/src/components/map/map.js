import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import Routing from "./route";
import { useRoutingContext } from '../../context/context';
import RouteInfo from './info';

export default function Map() {
  const position = [42.3883746, -72.52545997302758];
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo]= useRoutingContext();
  const graph = routingInfo.graph;
  const distance = routingInfo.distance;
  const elevation = routingInfo.elevation;

  return (
    <MapContainer center={position} zoom={13} style={{ height: "83vh" }}>
      <div> 
        <RouteInfo graph={graph} distance={distance} elevation={elevation}/>
      
      </div>
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Routing />
    </MapContainer>
  );
}

