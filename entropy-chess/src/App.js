import { useState, useEffect, CSSProperties } from 'react'
import * as React from 'react';
import { Button } from '@mui/material';
import EvaluationSlider from './components/slider/evaluationslider';
import MaterialSlider from './components/slider/materialslider';
import Popup from './Pages/Popup';


function App() {

  const [data, setData] = useState([{}])
  const [fenString, setFenString] = useState('start')

  const [buttonPopup, setButtonPopup] = useState(false)

  const [whiteMaterialValue, setWhiteMaterialValue] = useState(39)
  const [blackMaterialValue, setBlackMaterialValue] = useState(39)
  const [engineEvaluationValue, setEngineEvaluationValue] = useState('')
  const [evaluationThresholdValue, setEvaluationThresholdValue] = useState(10)
  const [zeroEvaluationValue, setZeroEvaluationValue] = useState(true)
  const [forcedMateValue, setForcedMateValue] = useState(true)


  useEffect(() => {
    fetch('/members').then(res => res.json()).then(data => {setData(data);
        console.log(data)
      }
    );
  }, [])

  const handleSubmit = () => {

    setFenString('start')

    const chess = {'whiteMaterialValue': whiteMaterialValue, 'blackMaterialValue': blackMaterialValue, 'evaluationThresholdValue': evaluationThresholdValue, 'zeroEvaluationValue': zeroEvaluationValue, 'forcedMateValue': forcedMateValue}
    fetch('http://localhost:3000/members', {
      method: 'POST',
      headers: {"Content-Type": "application/json"}, 
      body: JSON.stringify(chess)
    },
    ).then((result) => result.text(),
    // ).then((result) => console.log(result)
    ).then((result) => setFenString(result),
                      console.log(fenString),
                      setButtonPopup(true),
    )
  }

  return(
    <div>
      <MaterialSlider
      title = {"White Material"} callback={setWhiteMaterialValue}/>
      <MaterialSlider
      title = {"Black Material"} callback={setBlackMaterialValue}/>
      <EvaluationSlider
      title = {"Computer Evaluation"} evaluationValueCallback = { setEvaluationThresholdValue } zeroEvaluationValueCallback = { setZeroEvaluationValue } forcedMateValueCallback = { setForcedMateValue }/>
      <div className='generate-position-button'>
        <Button  variant="contained" onClick={() => {
            handleSubmit();
        }}>Generate Position  
        </Button>
      </div>
          <Popup trigger={buttonPopup} setTrigger={setButtonPopup} fenString={fenString}>
          </Popup>
    </div>
  )
}

export default App