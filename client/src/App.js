import React, {useState, useEffect} from 'react'
import './App.css';

function App() {
  
  const [data,setData] = useState()
  const requestOptions= {
    method: 'GET',
    headers: {'Content-type':'application/json'},
    body: JSON.stringify({data})
  }

  function handleClick(e) {
    e.preventDefault()
    fetch("/sdfs2",requestOptions)
    .then(response => {
      if(response.status === 401){
        alert("JOPA")
      }else{
        alert("neJOPA")
      }}
      )
    .then(response => response.json)
    .catch(response =>response.json)
    
    
    
  }

  function handleChange(e) {
    setData(e.target.value)
  }
  return (
    
    <form method="POST" >
      <input type="text" onChange={handleChange}/>
      <input type="submit" value="Отправить" onClick={handleClick}/>
    </form>
  );
}

export default App;
