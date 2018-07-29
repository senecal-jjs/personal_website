title: MiniMax & Game Playing AI
date: 2018-07-12
link: min

Instructions:
<ol>
    <li>Click on either first player or second player</li>
    <li>If you choose first player click a location on the board to begin playing</li>
    <li>When the game is finished click reset to clear the board</li>
</ol>

Disclaimer: I haven't implemented any exception handling so at the beginning of each game you must 
select a player, and at the end of each game you must hit reset, or the game logic will break. 

<p></p>

<style media="screen" type="text/css">
    #buttons {
    text-align: center;
    padding-bottom: 10px;
    }

    button {
    font-size: 18px;
    background-color: rgb(163, 163, 163);
    border-radius: 5px;
    }

    #endgame {
        background-color: #82caca;
        margin: 0 auto;
        font-family: "Helvetica", sans-serif;
        display: none;
        font-size: 3em;
        text-align: center;
        margin-bottom: 10px;
    }

    .game-container {
        max-width: 600px;
        max-height: 600px;
        background-color: #f1f0ef;
        display: grid;
        grid-template: repeat(3, 1fr) / repeat(3, 1fr);
        margin: 0 auto;
        font-family: "Helvetica", sans-serif;
    }
    
    .game-container .box {
        border-style: solid;
        border-color: rgb(143, 143, 143);
        color: rgb(107, 107, 107);
        min-width: 200px;
        min-height: 200px;
        background-color: #82caca;
        text-align: center;
        vertical-align: middle;
        line-height: 200px;
        font-size: 80px;
    }
    
    .game-container #um {
        grid-area: 1 / 2 / span 1 / span 1;
    }
    
    .game-container #ur {
        grid-area: 1 / 3 / span 1 / span 1;
    }
    
    .game-container #ml {
        grid-area: 2 / 1 / span 1 / span 1;
    }
    
    .game-container #mm {
        grid-area: 2 / 2 / span 1 / span 1;
    }
    
    .game-container #mr {
        grid-area: 2 / 3 / span 1 / span 1;
    }
    
    .game-container #ll {
        grid-area: 3 / 1 / span 1 / span 1;
    }
    
    .game-container #lm {
        grid-area: 3 / 2 / span 1 / span 1;
    }
    
    .game-container #lr {
        grid-area: 3 / 3 / span 1 / span 1;
    }
</style>

<script src="{{ url_for('static', filename="js/Node.js") }}" type="text/javascript"></script>
<script src="{{ url_for('static', filename="js/Tree.js") }}" type="text/javascript"></script>

<div id="buttons">
    <button onclick="first()">First Player</button> 
    <button onclick="second()">Second Player</button> 
    <button onclick="reset()">Reset</button>
</div>

<div id="endgame">You win!</div>

<div class="game-container" id="gameBoard">
    <div class="box" id="ul"></div>
    <div class="box" id="um"></div>
    <div class="box" id="ur"></div>
    <div class="box" id="ml"></div>
    <div class="box" id="mm"></div>
    <div class="box" id="mr"></div>
    <div class="box" id="ll"></div>
    <div class="box" id="lm"></div>
    <div class="box" id="lr"></div>
</div>

<script type="text/javascript" src="{{ url_for('static', filename="js/boardDisplay.js") }}"></script>

<script>
        // If human chooses to go second the AI will make an initial random move
        function second() {
            let gameBoard = ["", "", "", "", "", "", "", "", ""];
            gameBoard = randomMove("O", gameBoard); 
            gameAI = new AI(gameBoard, "X", false);
        }
        
        // If human chooses to go first we wait for the human to make a move
        // then update the game board and initialize the AI 
        firstVal = false;
        function first() {
            let gameBoard = ["", "", "", "", "", "", "", "", ""];
            firstVal = true;
        }

        // reset the game board
        function reset() {
            document.getElementById("endgame").style.display = "none";
            let boxes = document.querySelectorAll('.box');
            boxes.forEach((box) => {
                box.textContent = "";
                box.classList.remove('X');
                box.classList.remove('O');
            })
        }
        
        // Add event listener for when a box is clicked by user
        const buttons = document.querySelectorAll('.box');
        buttons.forEach((button) => {
        button.addEventListener('click', function(e){
            let id = e.target.id;
            let box = document.querySelector('#' + id);
            if (box.textContent != 'X' && box.textContent != 'O') {
                // Draw human move
                draw(id, 'X');

                // If human played first we need to initialize the game AI with the initial game board
                if (firstVal) {
                    console.log('check');
                    gameBoard = translate(true, null);
                    gameAI = new AI(gameBoard, "O", true);
                    firstVal = false; 
                }
                
                // Translate the current game board to an array and update the current root of the game 
                // possibilities tree
                let nextBoard = translate(true, null);
                gameAI.updateRoot(nextBoard);

                // Check for human win
                if (gameAI.currentRoot.isLeaf && gameAI.currentRoot.value !=0) {
                    let replace = document.getElementById("endgame");
                    replace.innerHTML = "You win!";
                    replace.style.display="block";
                } else if(gameAI.currentRoot.isLeaf && gameAI.currentRoot.value == 0){
                    let replace = document.getElementById("endgame");
                    replace.innerHTML = "Draw!";
                    replace.style.display="block";
                }
                
                // Choose AI action based on minimax
                nextBoard = gameAI.chooseAction();

                // Draw the AI move 
                translate(false, nextBoard);

                // Check for AI win
                if (gameAI.currentRoot.isLeaf && gameAI.currentRoot.value != 0) {
                    let replace = document.getElementById("endgame");
                    replace.innerHTML = "You lose!";
                    replace.style.display="block";
                } else if(gameAI.currentRoot.isLeaf && gameAI.currentRoot.value == 0) {
                    let replace = document.getElementById("endgame");
                    replace.innerHTML = "Draw!";
                    replace.style.display="block";
                }
                
            } else {
                alert("This location has already been played!");
            }
        })
        })
</script>

Game playing AI's have achieved a great deal of sucess recently. I'm talking about agents like AlphaGo that are capable of defeating world class GO players, or more recently the agent from agent from OpenAI, that they call <a target="_blank" href="https://blog.openai.com/openai-five/">OpenAI Five</a>. An agent trained using reinforcement learning that has begun to beat amateur human teams at the video game Dota 2. As OpenAI puts it, "Dota 2 is one of the most popular and complex esports games in the world, with creative and motivated professionals who train year-round to earn part of Dota’s annual $40M prize pool (the largest of any esports game)." 

A variety of strategies and algorithms for game playing AI's and algorithms exist. AlphaGo uses a combination of reinforcement learning and Monte Carlo Tree Search, while OpenAI Five uses a reinforcement learning algorithm known as proximal policy gradients. 

Algorithms for playing games have quite a long history. IBM's chess playing program Deep Blue, was one of the first well known algorithms to achieve success against a human player, defeating the chess grand master Gary Kasparov. Deep Blue used a form of tree search, where many possible sequences of games moves are calculated in advance, and the nodes of the tree, which correspond to game states, are evaluated for "goodness" in some manner.  

I find game playing agents and algorithms to be very interesting, so I've started to create some of my own implementations of existing algorithms. In a previous post I implemented an Atari game playing deep q-learning algorithm. Now I've started looking into a different class of algorithms. Namely, tree search algorithms like minimax and monte carlo tree search. 

The minimax algorithm, can be used for two player games like chess or tic-tac-toe. From Wikipedia, "The minimax value of a player is the smallest value that the other players can force the player to receive, without knowing the player's actions; equivalently, it is the largest value the player can be sure to get when they know the actions of the other players". 

Essentially, the minimax algorithm assumes that your opponent will choose moves that minimize your own gain, while you will choose moves that maximize your gain. In a simple game like tic-tac-toe the space of possible games is small enough that every possible way a tic-tac-toe game could be played out can be enumerated in a tree.

<div class="img_row">
    <img class="col-8" src="{{ url_for('static', filename="img/game-tree.png") }}">
</div>

<div class="col-12 caption">
    A limited enumeration of a game tree. From the intial starting node the tree would branch off to
    nine other nodes. One for each possible location you could play on the board. From each of those nodes there would be eight branches, one for each location that your opponent could play.
    <a target="_blank" href="http://www.flyingmachinestudios.com/programming/minimax/">Figure credit</a>
</div>

At end states (states where one player wins or there is a draw) a value can be assigned. For example a state where you win could be assigned a 1, a draw could be assigned a 0, and a loss could be assigned -1. Starting from these end states the values can be propagated back up to the root of the tree. Which values propagate depend on whose turn it is at a particular node in the tree. For example a node where it is your opponent's turn and they can make a move to win would be assigned -1 because this would result in a loss for you. This is what the mini in minimax refers to. When it is your opponent's turn the algorithm assumes they will choose a move that minimizes your gain. 

Try your luck against my implementation of the minimax algorithm up above. In tic-tac-toe a player following the minimax algorithm is guaranteed to at worst draw, so if you manage to win there is a bug in my implementation.
