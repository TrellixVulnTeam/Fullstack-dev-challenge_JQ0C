import React, {useEffect, useState ,useContext} from "react";
import axios from "axios";
import AppTile from "./AppTile";
import '../Scss/TopCharts.scss'
import { Link } from "react-router-dom";
import { baseUrlContext } from "../App";

function TopCharts(){
    const[topChart , setTopChart] = useState({})
    const base_url = useContext(baseUrlContext)
    useEffect(()=>{
        axios.get(`${base_url}/topcharts`)
        .then((response)=>{
            console.log(response.data['TOP_FREE_APPS'])
            setTopChart(response.data)

        })
    },[])
    var renderApps = (type)=>{
        
        if(topChart.hasOwnProperty(type)){
            return topChart[type].map((app , idx)=>{
                return <AppTile key={idx} name={app.name} company={app.company} logo={app.logo} pkg_name={app.pkg_name} ></AppTile>
            })
        }
        return null
    }
    return(
        <div className="top-charts">
            <header>
                <h1>Top Charts</h1>
            </header>
            <div className="top-free-apps">
                <header>
                    <h3><Link to='topfreeapps'>Top Free Apps</Link></h3>
                </header>
                <div className="apps_section">
                    {
                        renderApps('TOP_FREE_APPS')
                    }
                </div>
            </div>        
            <div className="TopPaidApps">
                <header>
                    <h3><Link to='toppaidapps'>Top Paid Apps</Link></h3>
                </header>
                <div className="apps_section">
                    {
                        renderApps('TOP_PAID_APPS')
                    }
                </div>
                
            </div>
            <div className="TopGrossingApps">
                <header>
                    <h3><Link to='topgrossingapps'>Top Grossing Apps</Link></h3>
                </header>
                <div className="apps_section">
                    {
                        renderApps('TOP_GROSSING_APPS')
                    }
                </div>
                
            </div>
            <div className="TopFreeGames">
                <header>
                    <h3><Link to='topfreegames'>Top Free Games</Link></h3>
                </header>
                <div className="apps_section">
                    {
                        renderApps('TOP_FREE_GAMES')
                    }    
                </div>
                
            </div>
            <div className="TopPaidGames">
                <header>
                    <h3><Link to='toppaidgames'>Top Paid Games</Link></h3>
                </header>
                <div className="apps_section">
                    {
                        renderApps('TOP_PAID_GAMES')
                    }
                </div>
                
            </div>
            <div className="TopGrossingGames">
                <header>
                    <h3><Link to='topgrossinggames'>Top Grossing Games</Link></h3>
                </header>
                <div className="apps_section">
                    {
                        renderApps('TOP_GROSSING_GAMES')
                    }
                </div>
            </div>
        </div>
    )
}

export default TopCharts