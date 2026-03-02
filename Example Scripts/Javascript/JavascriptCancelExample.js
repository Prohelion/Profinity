function sleepFor(sleepDuration) {
    var now = new Date().getTime();
    while (new Date().getTime() < now + sleepDuration) {
        /* Do nothing */
    }
}

function loop() {
    log('This is a loop!');
    while (!Profinity.ScriptCancelled)
    {
        log('About to Javascript sleep');
        sleepFor(1000);
        log('Finished the sleep');
    }    
};

loop();
log('Exiting Program');