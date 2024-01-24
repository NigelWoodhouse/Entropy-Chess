import * as React from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

const marks = [
  { value: 1, label: '1' },
  { value: 39, label: '39' },
  { value: 60, label: '60' },
];

function valuetext(value) {
  return `${value}`;
}

export default function MaterialSlider({title, callback}) {
  
  const [value, setValue] = React.useState(39);
  const handleChange = (event, newValue) => {
    setValue(newValue)
    callback(newValue)
  };
    
  return (

    <div className='slider-container'>
      <h1>{title}
      </h1>

      <Box sx={{ width: 500}}>
        <Slider
          sx={{color: 'white', 
        }}
        aria-label="Custom marks"
        value={value}
        getAriaValueText={valuetext}
        step={1}
        valueLabelDisplay="auto"
        marks={marks}
        min={1}
        max={60}
        onChange={handleChange}
        valueLabelFormat={valuetext}
        />
      </Box>

    </div>


  );
}