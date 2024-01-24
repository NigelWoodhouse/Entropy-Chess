import React from "react";
import { useState } from 'react'
import './Popup.css'
import { Button } from "@mui/material";
import DisplayChessboard from "../components/Board/DisplayChessboard";

function Popup(props){
    const displayFen = props.fenString

    return (props.trigger) ? (
        
        <div className="popup">
            <div className="popup-inner">
                <Button variant="contained" className="close-btn" onClick={() => props.setTrigger(false)}>Close</Button>
                {props.children}
            </div>

            <h1>Entropy Chess Position</h1>
            <DisplayChessboard position={props.fenString} />

            {displayFen != 'start' &&
            <div>
                
                <h5>Fen Position: </h5>
                <br></br>
                <p>{props.fenString}</p>
                <Button
                    onClick={() =>  navigator.clipboard.writeText(props.fenString)}>
                    Copy
                    </Button>
            </div>
            }

            {displayFen != 'start' &&   
            <div>
            <Button
                    variant="contained" onClick={() =>  window.open("https://lichess.org/analysis/fromPosition/"+props.fenString)}>
                    LiChess
                    </Button>
            </div>
            }

        </div>       
    ) : "";
}

export default Popup