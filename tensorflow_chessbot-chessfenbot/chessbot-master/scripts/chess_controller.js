var targets = '.game-controls.game.playing div.notationVertical a.gotomove'

function lookup() {
    // $.ajax({
    //     type: "GET",
    //     url: "https://localhost:8000/index.txt",
    //     async: false,
    //     success: function(data){
    //         result = data;
    //         console.log("SUCCESS");
    //         console.log(data);
    //         window.result = result;
    //     }
    // });
}
setInterval(lookup, 1000)
var moveList = [];
window.moveList = moveList;

var movesMaded = 0;
var getNextMove = function(movesArray) {
    window.arraylength = movesArray.length;
    // console.log("GET NEXT MOVE: " + window.arraylength);

    if (window.arraylength > 0) {
        for (var i = 0; i < movesArray.length; i++) {
            if (i === movesMaded && movesArray[i].innerText !== '' && movesArray[i].innerText.indexOf('0') === -1) {
                console.log("ARRAY PUSHED");
                window.moveList.push(movesArray[i].innerText);
                movesMaded++;
                // b_console.log("Move: " + move);
                return movesArray[i].innerText.replace('O-O+', 'O-O').replace('х', 'x'); // Sometimes it was happened
            }
        }
    }
    return false;
};


function makeLiveSuggest(movesArray) {
    // Terminate engine
    // console.log("MOVES ARRAY: " + movesArray)
    // console.log(JSON.stringify(movesArray)
    var nextMove = getNextMove(movesArray);
    console.log("NEXT MOVE: " + nextMove);
    while (nextMove) {
        nextMove = getNextMove(movesArray);
    }
}

function moveLookup() {
    var joinMoves = window.moveList.join();
    console.log("WINDOW LIST: " + window.moveList);
    $.ajax({
        url: 'https://echecservice.000webhostapp.com/phpmoves.php',
        type: 'POST',
        data: { somebody: joinMoves},
        success: function(data){
            // console.log("SENT MOVE")
        }
    });
}

function movecount() {

    var currentMovesCount = $(targets).filter(function() {
        return !!this.innerText;
    }).length;
    // console.log("MOVE COUNT: " + currentMovesCount)
    // console.log("TARGETS: " + targets)
    window.currentMovesCount = currentMovesCount
}

movecount();

function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var size = Math.floor(Math.random() * 30) + 10;

    for (var i = 0; i < size; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    text = possible.charAt(Math.floor(Math.random() * 25)) + text;

    return text;
}

greenSquareId = makeid(),
    pinkSquareId = makeid(),

    $greenSquare = $('<div>', {
        'id': greenSquareId,
        'style': 'position: absolute; z-index: 1; opacity: 0.5; background-color: #7ef502; color: #7ef502'
    }),
    $pinkSquare = $('<div>', {
        'id': pinkSquareId,
        'style': 'position: absolute; z-index: 1; opacity: 0.5; background-color: #f55252; color: #f55252'
    });

previousMovesCount = 0;

function madeMachineMove(move) {
    // console.log("MACHINE MOVED")
    var fromSquare = "z1";
        toSquare = "z1";
        // Find board container
        $boardcontainer = $('.tab-pane.active:not(.ng-hide) .game-board-container')
    $board = $boardcontainer.find('.chessboard')
    // Calculate sizes
    boardHeight = $board.height(),
        boardWidth = $board.width(),
        pieceHeight = (boardHeight) / 8,
        pieceWidth = (boardWidth) / 8,
        // console.log("BOARD HEIGHT: " + boardHeight),
        // console.log("BOARD WIDTH: " + boardWidth),
        // console.log("PIECE HEIGHT: " + pieceHeight),
        // console.log("PIECE WIDTH: " + pieceWidth),
        // Is flipped?
        betaPositionFix = 0,
        $boardArea = $board.find("div[id^=chessboard_][id$=_boardarea]")

    if (window.currentMovesCount > 0) {
        if (window.currentMovesCount != previousMovesCount) {
            currentColor = window.currentMovesCount % 2 == 0 ? 1 : 2;
            window.currentColor = currentColor
            console.log("CURRENT COLOR: " + currentColor)
            previousMovesCount = window.currentMovesCount;
            // Possible new at each fire.
            // var subtargetName = isBetaDesign ? '.dijitVisible #moves div.notation' : '.dijitVisible #moves div.notation';
        }
    }

    if (window.currentColor == 1)
    {
        console.log("PLAYER IS WHITE")
        $.ajax({
            url: 'https://echecservice.000webhostapp.com/phpcolor.php',
            type: 'POST',
            data: { ignition: "WHITE"},
        });
    }

    if (window.currentColor == 2)
    {
        console.log("PLAYER IS BLACK")
        $.ajax({
            url: 'https://echecservice.000webhostapp.com/phpcolor.php',
            type: 'POST',
            data: { ignition: "BLACK"},
        });
    }

    // Move pinkSquares to the right place
    function placeSquareToPointChessCom($square, point) {
        $('#' + $square.attr('id')).remove(); // Fix for: https://github.com/recoders/chessbot/issues/20
        var pinkTop, pinkLeft;
        // console.log("TO SQUARE: " + toSquare)
        // console.log("FROM SQUARE: " + fromSquare)
        //Point is a multiplier from 1 to 8 for each square of the board. Ex: (h = 8, 8 * (length of one square))

        var rect = $board[0].getBoundingClientRect();
        // console.log(rect.top, rect.right, rect.bottom, rect.left)
        var topoff = $board.offset().top;
        var leftoff = $board.offset().left
        var rightoff = $board.offset().right;
        var botoff = $board.offset().bottom;
        // console.log("TOP OFFSET: " + topoff + " LEFT OFFSET: " + leftoff + " RIGHT OFFSET: " + rightoff + " BOTTOM OFFSET: " + botoff);

        var TOPOFFSETFIX = pieceHeight/2
        var slightfix = pieceWidth/32
        var slighterfix = pieceHeight/64

        // console.log("PINKTOP SET: " + pieceHeight * (parseInt(point[1], 8)))
        // console.log(parseInt(point[1], 8))

        pinkTop = $boardArea[0].offsetTop + (boardHeight - pieceHeight * (parseInt(point[1], 10))); // 1 pixel from border
        pinkLeft = $boardArea[0].offsetLeft + pieceWidth * (point.charCodeAt(0) - 97); // 'a'.charCodeAt(0) == 97
        // console.log("PINK TOP : " + pinkTop)
        // console.log("PINK LEFT: " + pinkLeft)

        var pinkTopOff = $board.offset();
        // console.log("BOARD AREA OFFSET: " + $boardArea[0].offsetTop + " " + $boardArea[0].offsetLeft);
        // console.log("BOARD TOP OFF: " + (pinkTopOff.top + window.screenTop) + " " + (pinkTopOff.left+window.screenLeft));
        window.boardTopOff = (pinkTopOff.top + window.screenTop);
        window.boardLeftOff = (pinkTopOff.left + window.screenLeft);
        window.pinkTop = pinkTop + (pinkTopOff.top + window.screenTop);
        window.pinkLeft = pinkLeft + (pinkTopOff.left+  window.screenLeft);
        window.boardX = $board.width();
        window.boardY = $board.height();
        // console.log("BOARD DIMS: " + window.boardX + " " + window.boardY);

        var GreenTop, GreenLeft;
        GreenTop = $boardArea[0].offsetTop + (boardHeight - pieceHeight * (parseInt(fromSquare[1], 10) + betaPositionFix)); // 1 pixel from border
        GreenLeft = $boardArea[0].offsetLeft + pieceWidth * (fromSquare.charCodeAt(0) - 97); // 'a'.charCodeAt(0) == 97

        window.greenTop = GreenTop + (pinkTopOff.top+window.screenTop);
        window.greenLeft = GreenLeft + (pinkTopOff.left+window.screenLeft);


        $square.css({
            'width': pieceWidth,
            'height': pieceHeight,
            'top': pinkTop,
            'left': pinkLeft
        });
        $square.appendTo($board);

    }

    placeSquareToPointChessCom($greenSquare, fromSquare);
    placeSquareToPointChessCom($pinkSquare, toSquare);
    // console.log("PLACE SQUARE")
}
function startLiveSuggestion() {
    makeLiveSuggest($(targets))
}
window.starliver = 500;

// function logMove(movecount){
//     var prevCount = movecount;
// }

function refreshThis() {
    console.log("STARLIVER : " + window.starliver);
    console.log("GAME MOVES: " + window.arraylength);
    if(window.arraylength == 0 && window.moveList > 0){
        window.starliver = 1000;
        location.reload();
        setTimeout(refreshThis, 1000);
        console.log("RESET MOVE LIST");
    }
    else if(window.arraylength == undefined){
        setTimeout(refreshThis, 500);
        console.log("GAME NOT FOUND")
    }
    else if(window.arraylength > 0){
        window.starliver = 500;
        setTimeout(refreshThis, 500);
        console.log("NO NEW GAME");
    }
    else if(window.arraylength == 0 && window.moveList == 0){
        setTimeout(refreshThis, 500);
        console.log("BOTH ZERO")
    }

}

function update(){
    if(window.pinkLeft != undefined && window.greenLeft != undefined){
        $.ajax({
            url: 'https://echecservice.000webhostapp.com/phpsave.php',
            type: 'POST',
            data: { something: window.pinkLeft + " " + window.pinkTop + " " + window.greenLeft + " " + window.greenTop },
        });

    }

    $.ajax({
        url: 'https://echecservice.000webhostapp.com/dimensions.php',
        type: 'POST',
        data: { dimensions: window.boardX + " " + window.boardY },
    });

    $.ajax({
        url: 'https://echecservice.000webhostapp.com/offset.php',
        type: 'POST',
        data: { offset: window.boardLeftOff + " " + window.boardTopOff },
    });


    // if (window.currentColor == 0)
    // {
    //
    //     console.log("PLAYER IS WHITE")
    //     $.ajax({
    //         url: 'https://echecservice.000webhostapp.com/phpcolor.php',
    //         type: 'POST',
    //         data: { ignition: "WHITE"},
    //     });
    // }
    // else if (window.currentColor == 1)
    // {
    //     console.log("PLAYER IS BLACK")
    //     $.ajax({
    //         url: 'https://echecservice.000webhostapp.com/phpcolor.php',
    //         type: 'POST',
    //         data: { ignition: "BLACK"},
    //     });
    // }
    // lookup();
    // madeMachineMove();
    // movecount();
    // moveLookup();
    // startLiveSuggestion();
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

console.log("READY");
// setInterval(lookup, 1200);
setInterval(madeMachineMove, 1000);
setInterval(movecount, 800);
setInterval(moveLookup, 600);
setInterval(startLiveSuggestion, 400);
// logmove(window.arraylength);
setInterval(update, 200);
refreshThis();

$.ajax({
    url: 'https://localhost:8000/',
    type: 'POST',
    data: { ignition: "WHITE"},
});


// setInterval(heightalert, 2000)