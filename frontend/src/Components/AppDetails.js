import React, { useContext, useEffect,useState } from "react";
import axios from "axios";
import '../Scss/AppDetails.scss'
import StarRatings from 'react-star-ratings';
import { baseUrlContext } from "../App";

function AppDetails(){
    const[details , setDetails] = useState({name:'' , company:'' , logo:'' , genre:'' ,rating:0 , resources:[] , description:'' ,details_url:''})
    const base_url = useContext(baseUrlContext)
    useEffect(()=>{
        axios.get(`${base_url}${window.location.pathname + window.location.search}`)
        .then((response)=>{
            setDetails(response.data)
        })
    },[])
    return(
        <div className="app-details">
            <div className="header">
                <div className="logo">
                    <img src={details['logo']}/>
                </div>
                <div className="info">
                    <div className="name">
                        {details.name}
                    </div>
                    <div className="developer">
                    {details.company}
                    </div>
                    <div className="genre">
                        {details.genre}
                    </div>
                    <div className="rating">
                        <StarRatings rating={parseFloat(details.rating)} numberOfStars={5} starRatedColor="orange" starDimension="30px"/>
                    </div>
                </div>  
                <div className="install">
                    <a href={details.details_url} target="_blank">Install</a>
                </div>   
            </div>
            <div className="resources">
                {
                    details.resources.map((src)=>{
                        return <img src={src} referrerPolicy="no-referrer"/>
                    })
                }
            </div>     
            <div className="description">
                {
                    details.description
                }
            </div>   
        </div>

    )
}

export default AppDetails