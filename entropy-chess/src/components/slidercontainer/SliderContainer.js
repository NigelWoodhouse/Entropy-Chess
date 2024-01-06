import EvaluationSlider from '../slider/evaluationslider'
import MaterialSlider from '../slider/materialslider'

function SliderContainer({title, type}) {

  console.log(type)
  if (type === "material"){
    return (
      <div className='app-container'>
        <h1>{title}
        </h1>
        <MaterialSlider />
      </div>
  )}

  if (type === "evaluation"){
    return (
      <div className='app-container'>
        <h1>{title}
        </h1>
        <EvaluationSlider />
      </div>
  )}
}

export default SliderContainer