let timeleft = 10;
let timer;
$( function() {
    $('#progressbar').progressbar({ 
        value: timeleft,
        max: 10,
    });
} );

start_timer = () => {
    timeleft = 10;
    timer = setInterval(() => {
        timeleft--;
        $('#progressbar').progressbar('option', 'value', timeleft);
        if(timeleft <= 0) {
            // Question not answered
            clearInterval(timer);
            evaluate_answer();
        }
    },1000);
    return timer;
}

stop_timer = () => {
    if(timer) {
        clearInterval(timer);
    }
}