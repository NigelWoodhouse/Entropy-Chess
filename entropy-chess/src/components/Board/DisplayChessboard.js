import React from 'react';
import { Chessboard } from 'react-chessboard';
import './DisplayChessboard.css'

export default function DisplayChessboard({position}) {
  return (
    <div className="board">
      <Chessboard
        id="ChessboardWithProps"
        position={position}
        orientation="white"
        showNotation={true}
        arePiecesDraggable={false}
      />
    </div>
  );
}