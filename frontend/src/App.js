import {useState, useEffect} from 'react';
import './App.css';

function App() {
  const [result, setResult] = useState({ppms: {}, weights: {}})

  useEffect(() => console.log(result), [])

  return (
    <div className="App">
    <head>
      <meta charSet="utf-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1"/>
      <title>Brewing</title>
    </head>
      <h1 class="title mt-5"> Brewing - Salts </h1>
      <Ions ions={ions} ppms={result.ppms} setResult={setResult}/>
      <Salts salts={salts} weights={result.weights}/>
    </div>
  );
}

const ions = [
  {"ion": "cl", "desired": 212, "plusminus":10, "multiplyer": 1, "actual": null},
  {"ion": "s04", "desired": 212, "plusminus":10, "multiplyer": 1, "actual": null},
  {"ion": "ca", "desired": 212, "plusminus":10, "multiplyer": 1, "actual": null},
  {"ion": "mg", "desired": 212, "plusminus":10, "multiplyer": 1, "actual": null},
  {"ion": "na", "desired": 212, "plusminus":10, "multiplyer": 1, "actual": null},
  {"ion": "hc03", "desired": 212, "plusminus":10, "multiplyer": 1, "actual": null}

]

const salts = [
  {"name": "CaCl2", "weight": 10}
]

function calculate (setResult){
  console.log("calculating")
  let response =  fetch("http://localhost:5000/calculate",
    {method: "POST",
    headers: {
      // 'Content-Type': 'application/json'
    },
    body: JSON.stringify(ions)})
    .then((response) => response.json())
    .then(setResult)


}

function Salts({salts, weights}){
  return (
    <section class="section">
      <h2 class="subtitle"> Salts in 10L </h2>
      <div class="columns is-centered">
        <table class="table card column is-flex-grow-0">
          <th>
            Salt
          </th>
          <th>
            Weight(g)
          </th>


          {Object.entries(weights).map(([name, weight], _)  =>
            <tr>
              <td>{name}</td>
              <td>{weight}</td>

            </tr>)}

        </table>
        </div>

    </section>
  )
}

function Ions({ions, setResult, ppms}) {
  return (
    <section class="section">
      <h2 class="subtitle">Ion Configuration</h2>
      <div class="columns is-centered">
        <table class="table card column is-flex-grow-0">

          <th>
            Ion
          </th>
          <th>
            Desired
          </th>
          <th>
            +/-
          </th>
          <th>
            multiplyer
          </th>
          <th>
            Actual
          </th>

          {ions.map(ion =>
            <tr>
              <td>{ion.ion}</td>
              <td> <input type="text" value={ion.desired}/> </td>
              <td> <input type="text" value={ion.plusminus}/> </td>
              <td> <input type="text" value={ion.multiplyer}/> </td>
              <td>{ppms[ion.ion]}</td>
            </tr>)}

        </table>
        </div>
      <button class="button" onClick={() => calculate(setResult)}> Calculate </button>
    </section>
  )
}

export default App;
