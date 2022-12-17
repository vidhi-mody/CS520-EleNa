import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import logoWheel from './cycle.png';


export default function Title() {
  return (
    <Box sx={{ display: 'grid', gridTemplateRows: 'repeat(2)' }}>
      
      <Typography sx={{fontFamily: "Gill Sans"}} variant="h2" component="div" align='center'>
        <Typography sx={{height: '70px', width: '70px'}} src={logoWheel} component="img" align='left' />
        EleNa
      </Typography>
      <Typography sx={{fontFamily: "Gill Sans"}} variant="h5" gutterBottom component="div" align='center'>
        Elevation-based Navigation
      </Typography>
    </Box>
  );
}