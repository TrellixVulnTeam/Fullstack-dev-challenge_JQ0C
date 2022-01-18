import logo from './logo.svg';
import './App.css';
import { Routes, Route, Link } from "react-router-dom";
import TopCharts from './Components/TopCharts';
import TopApps from './Components/TopApps';
import AppDetails from './Components/AppDetails';
import React from 'react';


export const baseUrlContext = React.createContext()

function App() {
  return (
    <baseUrlContext.Provider value={'https://navneet-fullstack-backend-dot-bluestacks-cloud-beginners.uc.r.appspot.com'}>
      <div className="App">
        <Routes>
          <Route path='/' element={<TopCharts/>}/>
          <Route path='/topfreeapps' element={<TopApps route={'topfreeapps'}/>}/>
          <Route path='/toppaidapps' element={<TopApps route={'toppaidapps'}/>}/>
          <Route path='/topgrossingapps' element={<TopApps route={'topgrossingapps'}/>}/>
          <Route path='/topfreegames' element={<TopApps route={'topfreegames'}/>}/>
          <Route path='/toppaidgames' element={<TopApps route={'toppaidgames'}/>}/>
          <Route path='/topgrossinggames' element={<TopApps route={'topgrossinggames'}/>}/>
          <Route path='/appdetails' element={<AppDetails/>} />
        </Routes>
      </div>
    </baseUrlContext.Provider>

  );
}

export default App;
