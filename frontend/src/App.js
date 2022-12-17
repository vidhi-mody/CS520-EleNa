import Map from "./components/map/map";
import Header from './components/header/head'
import UserInput from "./components/form/inputs"
import Box from '@mui/material/Box';
import {RoutingContextProvider} from './context/context';

export default function App() {
  return (
    <div className="App">
      <Box>
        <Header/>
      </Box>
      <Box
        sx={{
          display: 'grid',
          bgcolor: '#FAF9F6',
          gridAutoColumns: '1fr'
        }}
      >
        <RoutingContextProvider>
          <Box>
          <Map/>
          </Box>
          <Box sx={{ gridColumn: '2 / 2' }}>
          <UserInput/>
           
          </Box>
        </RoutingContextProvider>
      </Box>
    </div>
  );
}


