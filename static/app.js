
class BoggleGame {

    constructor(board, secs=60){
        this.board = $('#boggle');
        this.score = 0;
        this.secs = secs;
        this.words = new Set();
        this.showTimer();

        this.timer = setInterval(this.tick.bind(this), 1000);

        $('.add_word', this.board).on('submit', this.checkWord.bind(this));
    }
   
    async checkWord(evt){
        //Grab input value
        evt.preventDefault();
        //Using jQuery, take the form value 
        const $word = $('.word', this.board);
        let word = $word.val();

        //Get word validity from the server and inform the user
        //and using axios, make an AJAX request to send it to the server. 
        const resp = await axios.get('/check-word', {params:{guess_input: word}});
        
        if(resp.data.Result === "not-word"){
            this.showMessage(`${word} is not a word!`);
        }
        else if(resp.data.Result === "not-on-board"){
            this.showMessage(`${word} is not on the board.`);
        }
        else{
            this.showMessage(`Added: ${word}`);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
        }

    }

    showMessage(msg){
        //Display message for user on front-end
        $('.display_result', this.board).text(msg);
    }

    showScore(){
        //Display Score
        $('.score', this.board).text(this.score);
    }

    showTimer(){
        //Display game timer
        $('.timer', this.board).text(this.secs);
    }

    async tick(){
        //Timer Countdown
        this.secs -= 1;
        this.showTimer();

        if(this.secs === 0){
            clearInterval(this.timer);
            //Disable future guesses
            $('.word').prop('disabled', true);
            $('button').prop('disabled', true);
        }
        await this.gameEnd();
    }

    async gameEnd(){
        //Save score to server
        const resp = await axios.post('/post-score', {score: this.score});
        if(resp.data.brokeRecord){
            this.showMessage(`New High Score: ${this.score}`);
        } 
        else{
            this.showMessage(`Final Score: ${this.score}`);
        }
    }
}

const game = new BoggleGame('boggle', 60);
