import * as React from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

const marks = [
  {
    value: 0,
    label: '0',
  },
  {
    value: 2,
    label: '2',
  },
  {
    value: 4,
    label: '4',
  },
  {
    value: 6,
    label: '6',
  },
  {
    value: 8,
    label: '8',
  },
  {
    value: 10,
    label: '10',
  },

  {
    value: -2,
    label: '-2',
  },
  {
    value: -4,
    label: '-4',
  },
  {
    value: -6,
    label: '-6',
  },
  {
    value: -8,
    label: '-8',
  },
  {
    value: -10,
    label: '-10',
  },
];

function valuetext(value) {
  return `${value}`;
}

export default function EvaluationSlider() {
  const [value, setValue] = React.useState([-2, 2]);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: 500 }}>
      <Slider
          sx={{color: 'white',
        }}
        getAriaLabel={() => 'Temperature range'}
        value={value}
        max={10}
        min={-10}
        marks={marks}
        onChange={handleChange}
        valueLabelDisplay="auto"
        getAriaValueText={valuetext}
      />
    </Box>
  );
}