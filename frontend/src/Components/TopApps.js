import React, { useEffect, useState ,useContext } from "react";
import axios from "axios";
import AppTile from "./AppTile";
import '../Scss/TopApps.scss'
import { baseUrlContext } from "../App";

function headerValue(value){
    switch(value.toLowerCase()){
        case 'topfreeapps':
            return 'Top Free Apps'
        case 'toppaidapps':
            return 'Top Paid Apps'
        case 'topgrossingapps':
            return 'Top Grossing Apps'
        case 'topfreegame':
            return 'Top Free Games'
        case 'toppaidgames':
            return 'Top Paid Games'
        case 'topgrossinggames':
            return 'Top Grossing Games'
        default:
            return 'Top Apps'
    }
}
function TopApps({route}){
    const [topApps , setTopApps] = useState([])
    const base_url = useContext(baseUrlContext)
    useEffect(()=>{
        axios.get(`${base_url}/${route}`)
        .then((response)=>{
            setTopApps(response.data)
        })
    },[])
    return(
        <div className="TopApps">
            <header>
                <h1>{headerValue(route)}</h1>
            </header>
            <div className="apps">
                {
                    topApps.map((app)=>{
                        return <AppTile name={app.name} company={app.company} logo={app.logo} pkg_name={app.pkg_name} />
                    })
                }
            </div>
            
        </div>
    )
}

export default TopApps