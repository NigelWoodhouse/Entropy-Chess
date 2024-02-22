import * as React from 'react';
import { useState } from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import Checkbox from '@mui/material/Checkbox';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Tooltip from '@mui/material/Tooltip';

const marks = [
  { value: 1, label: '1' },
  { value: 2, label: '2' },
  { value: 3, label: '3' },
  { value: 4, label: '4' },
  { value: 5, label: '5' },
  { value: 6, label: '6' },
  { value: 7, label: '7' },
  { value: 8, label: '8' },
  { value: 9, label: '9' },
  { value: 10, label: '10' },
  { value: 11, label: '11' },
  { value: 12, label: '12' },
  { value: 13, label: '13' },
  { value: 14, label: '14' },
  { value: 15, label: '15' },
  { value: 16, label: '16' },
];

function valuetext(value) {
  return `${value}`;
}

export default function EvaluationSlider({title, evaluationValueCallback, zeroEvaluationValueCallback, forcedMateValueCallback}) {
  const [value, setValue] = React.useState(10);
  const [isCheckedZeroEvaluation, setIsCheckedZeroEvaluation] = useState(true)
  const [isCheckedForcedMate, setIsCheckedForcedMate] = useState(true)

  const handleChangeSlider = (event, newValue) => {
    setValue(newValue)
    evaluationValueCallback(newValue)
  };

  const checkHandlerZeroEvaluation = () => {
    setIsCheckedZeroEvaluation(!isCheckedZeroEvaluation)
    zeroEvaluationValueCallback(!isCheckedZeroEvaluation)
  }

  const checkHandlerForcedMate = () => {
    setIsCheckedForcedMate(!isCheckedForcedMate)
    forcedMateValueCallback(!isCheckedForcedMate)
  }

  return (

    <div className='slider-container'>
    <h1>{title}
    </h1>

    <div className='zero-eval-checkbox'>
        <FormGroup className='zero-eval-checkbox'>
          <Tooltip title="Allowing 0 evaluation may produce a perpetual check position." placement="top">
            <FormControlLabel control={<Checkbox onChange={checkHandlerZeroEvaluation} checked={isCheckedZeroEvaluation}/>} label="Allow 0 Evaluation" />
          </Tooltip>
        </FormGroup>
        <FormGroup className='forced-mate-checkbox'>
          <Tooltip title="Allows a forced mate positions." placement="top">
            <FormControlLabel control={<Checkbox onChange={checkHandlerForcedMate} checked={isCheckedForcedMate}/>} label="Allow Forced Mate" />
          </Tooltip>
        </FormGroup>
    </div>

    <Box sx={{ width: 500 }}>
      <Slider
          sx={{color: 'white',
        }}
        getAriaLabel={() => ''}
        value={value}
        max={16}
        min={1}
        marks={marks}
        onChange={handleChangeSlider}
        valueLabelDisplay="auto"
        getAriaValueText={valuetext}
      />
    </Box>

    </div>



  );
}