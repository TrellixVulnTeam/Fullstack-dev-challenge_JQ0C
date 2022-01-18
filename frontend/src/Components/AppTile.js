import React from "react";
import { Link } from "react-router-dom";
import '../Scss/AppTile.scss'

function AppTile({name , company , logo , pkg_name}){
    return(
        <div className="app-tile">
            <table>
                <tbody>
                    <tr>
                        <td rowSpan={2}>
                            <img referrerPolicy="no-referrer" src={logo} alt="App logo"/>
                        </td>
                        <td colSpan={1}>
                            {/* <Link to={`appdetails?pkg=${pkg_name}`}>{name}</Link> */}
                            <a href={`appdetails?pkg=${pkg_name}`} >{name}</a>
                        </td>
                    </tr>
                    <tr>
                        <td colSpan={1}>
                            {company}
                        </td>
                    </tr>
                </tbody>

            </table>
        </div>
    )
}

export default AppTile