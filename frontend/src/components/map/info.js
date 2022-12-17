import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Loading from './loading'
import { useRoutingContext } from '../../context/context';

export default function RouteInfo({graph, distance, elevation}) {
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo]= useRoutingContext();
  const sent = routingInfo.sent;
  return (
    <div>  
      {!sent ? null :
        <Box sx={{ zIndex: 1000, position: 'absolute', right: 20,  bottom: 20, backgroundColor: '#FAF9F6', width: '220px', height: '130px'}}>
          <Typography variant="h5" align="center" gutterBottom sx={{fontFamily: "Gill Sans",}}>
            Route Statistics
          </Typography>
          {!graph ? 
            <Loading />
            :
            <div>
              <Typography variant="body1" align="center" sx={{fontFamily: "Gill Sans", marginLeft: '4px'}}>
                Total Distance: {distance > 1000 ? `${Math.floor(distance) / 1000} km` : `${Math.floor(distance)} m`}
              </Typography>
              <Typography variant="body1" align="center" sx={{fontFamily: "Gill Sans", marginLeft: '4px'}}>
                Elevation Gain: {elevation} meters
              </Typography>
            </div>
          }
        </Box>
      }
    </div>
  )
}