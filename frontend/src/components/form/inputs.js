import React, { useState } from 'react';
import Box from '@mui/material/Box';
import ElevationType from './elevationType';
import ElevationPercentage from './elevationPercentage';
import InputSource from './source';
import InputDestination from './destination';
import Search from './submit';
import { ROUTING_API, ROUTING_REQUEST_BODY } from '../../Config';
import post from '../../http/post';
import {useRoutingContext} from '../../context/context';


export default function Inputs() {
 
  const [source, setSource] = useState(''); 
  const [destination, setDestination] = useState('');
  const [elevationType, setElevationType] = useState('min');
  const [percentageElevation, setpercentageElevation] = useState(0.25);
  
  // finds nodes and ways
  // eslint-disable-next-line
  const [overpassAPIResponse,getAPIResponse] = useState({
      data: null,
      loading: true,
      error: null,
  });
  // eslint-disable-next-line
  const [routeInfo, getRouteInfo] = useRoutingContext();

  const routeFinder = () => {
    if (!source || !destination ) {
      alert("Please fill the source and/or destination location")
      return;
    }
  console.log(source, destination)
    getRouteInfo((data) => ({
      ...data,
      sent: true,
      graph: false
    }))
    const errorHandler = (e) => {
      console.log(e);
      getRouteInfo((data) => ({
        ...data,
        sent: false,
      }))
    }
    const successHandler = (res) => {
      console.log(res.data)
      getRouteInfo((prev) => ({
        ...prev,
        graph: res.data[0],
        distance: res.data[1],
        elevation: res.data[2]
      }))
    }
    function address(){
      //
      let address = ''
      if (source.address.city) {
        address = `${source.address.city},`
      } else if (source.address.town) {
        address = `${source.address.town},`
      } else if (source.address.municipality) {
        address = `${source.address.municipality},`
      } else if (source.address.village) {
        address = `${source.address.village},`
      }
      if (source.address.state) {
        address += ` ${source.address.state}`
      } else if (source.address.county) {
        address += ` ${source.address.county}`
      } else if (source.address.region) {
        address += ` ${source.address.region}`
      } else if (source.address.state_district) {
        address += ` ${source.address.state_district}`
      }
      return address;
    }
    post(getAPIResponse, ROUTING_API, errorHandler, successHandler, ROUTING_REQUEST_BODY(source.lat, source.lon, destination.lat, destination.lon, address(), elevationType, (Math.round(percentageElevation*100)+100) ))
  }

  return (
    
    <div>
       <br></br>
    
      <Box align="left" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <InputSource source={source} setSource={setSource} />
        <InputDestination destination={destination} setDestination={setDestination} />
        <ElevationType elevationType={elevationType} setElevationType={setElevationType}/>
        <ElevationPercentage percentageElevation={percentageElevation} setpercentageElevation={setpercentageElevation}/>
      
      </Box>
      <br></br>
      <br></br>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <Search routeFinder={routeFinder} />
      </Box>
      <br></br>
     
     
    </div>
  );
}

