import { useState, useEffect, useRef } from 'react'
import SliderContainer from './components/slidercontainer/SliderContainer'
import * as React from 'react';

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch('/members').then(res => res.json()).then(data => {setData(data);
        console.log(data)
      }
    );
  }, [])

  

  return(
    <div>
      <SliderContainer
      title = {"White Material"} type = {"material"}/>
      <SliderContainer
      title = {"Black Material"} type = {"material"}/>
      <SliderContainer
      title = {"Computer Evaluation"} type = {"evaluation"}/>

      {/* {(typeof data.members === 'undefined') ? (
        <p>Loading...</p>
      ) : (
        data.members.map((member, i) => (
          <p key={i}>{member}</p>
        ))
      )} */}
    </div>
  )
}

export default App