import React from 'react';
import Typography from '@mui/material/Typography';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import UpArrow from '@mui/icons-material/ArrowUpward';
import DownArrow from '@mui/icons-material/ArrowDownward';
import Box from '@mui/material/Box';

export default function ElevationInput({elevationType, setElevationType}) {

  const ctrl = {
    value: elevationType,
    onChange: (event, elevationChoice) => {
      if (elevationChoice !== null) {
        setElevationType(elevationChoice);
      }
    },
    exclusive: true,
  };

  const elevation_type = [
    <ToggleButton size="large" value="min" key="min">
      <Typography sx={{fontFamily: "Gill Sans"}} variant="h7" component="div" align='center' style={{ marginRight: '3px' }}>
        Min 
      </Typography>
      <DownArrow fontSize='medium'/>
    </ToggleButton>,
    <ToggleButton size="large" value="max" key="max">
      <Typography sx={{fontFamily: "Gill Sans"}} variant="h7" component="div" align='center' style={{ marginRight: '3px' }}>
        Max
      </Typography>
      <UpArrow fontSize='medium'/>
    </ToggleButton>,
    
  ];

  return (
    <Box sx={{ marginTop: '10px', display: 'flex', flexDirection: 'column', alignItems: 'left'}}>
      
      <p>Elevation Type:</p>
      <ToggleButtonGroup 
        sx={{backgroundColor: "white"}} 
        color="standard" 
        size="large" 
        {...ctrl}>
          {elevation_type}
      </ToggleButtonGroup>
    </Box>
  );
}