import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import {
  CircularInput,
  CircularTrack,
  CircularProgress,
  CircularThumb
} from "react-circular-input";

export default function DistanceInput({percentageElevation, setpercentageElevation}) {
  function convertToInteger(value) {
    const val = Math.round(value*100)+100
    return val;
  }

  const handleElevationChange = (setPrecentage) => {
    setpercentageElevation(setPrecentage);
  };


  return (
    <Box sx={{ marginTop: '30px' }}>
      <Typography sx={{fontFamily: "Gill Sans"}} variant="h7" id="distance-percentage-slider" gutterBottom>
        Percentage Increase From Shortest Distance:
      </Typography>
       <Grid container spacing={2} alignItems="center">
        <Grid item xs sx={{ marginTop: '30px' }} style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
        }}>
          <CircularInput value={percentageElevation} onChange={handleElevationChange}>
          <CircularTrack stroke='lightgrey' />
          <CircularProgress stroke="#AC9362"/>
          <CircularThumb fill="#AC9362"stroke="#AC9362"/>
            <text x={100} y={100} textAnchor="middle" dy="0.3em" fontWeight="bold" sx={{fontFamily: "Gill Sans"}} >
              {convertToInteger(percentageElevation)}%
            </text>
          </CircularInput>
        </Grid>
      </Grid>
    </Box>
  );
}