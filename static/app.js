
class BoggleGame {

    constructor(board){
        this.board = $('#boggle');
        this.score = 0;
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
}

const game = new BoggleGame('boggle');