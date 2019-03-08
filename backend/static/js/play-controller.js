"use strict";

function Controller() {

  let backendModel = sessionStorage.getItem("modelName");
  let playerColor = sessionStorage.getItem("userColor");

  // TODO: better error handling.
  if (!backendModel) {
    backendModel = "random";
  }

  if (playerColor !== "w" && playerColor !== "b") {
    playerColor = "w";
  }

  let model = new Model({
    backendModel,
    pgn: null,
    playerColor,
  });

  let view;

  function mouseoverEntryHandler(square) {
    if (!model.canPlayerMove())
      return;

    const moves = model.getAllowedMoves(square);

    if (moves.length === 0)
      return;

    // Highlight the square the user moused over, if there is a
    // movable piece there.
    view.highlightSquare(square);

    // Highlight the squares it can move to.
    for (let move of moves) {
      view.highlightSquare(move.to);
    }
  }

  function mouseoverExitHandler(square) {
    view.unhighlightAllSquares();
  }

  function dragStartHandler(piece) {
    return model.canPlayerMove() && model.doesPlayerOwnPiece(piece);
  }

  function dragFinishHandler(fromSquare, toSquare) {
    view.unhighlightAllSquares();
    return model.tryMakingMove(fromSquare, toSquare);
  }

  function updateViewFromMove() {
    view.setBoardFEN(model.getGameFEN());
    view.setStatusText(model.getGameStatus());
  }

  function moveFinishHandler() {
    updateViewFromMove();

    if (model.canComputerMove()) {
      apiRequest({
        command: "get_move",
        model: model.getBackendModel(),
        pgn: model.getGamePGN(),
      }, (response) => {
        // TODO: better error handling.
        model.setGamePGN(response.pgn);
        updateViewFromMove();
      });
    }
  }

  view = new View({
    boardOrientation: playerColor,
    fen: model.getGameFEN(),
    mouseoverEntryHandler,
    mouseoverExitHandler,
    dragStartHandler,
    dragFinishHandler,
    moveFinishHandler,
  });
  updateViewFromMove();

}

// Kick everything off.
const controller = new Controller();
