import React from 'react';
import Button from '@mui/material/Button';

export default function SearchButton({routeFinder}) {
  return (
    <Button sx={{width: '30%' }} style={{backgroundColor: "#AC9362 "}} variant="contained" size="large" onClick={routeFinder}>
     Search 
    </Button>
  );
}
