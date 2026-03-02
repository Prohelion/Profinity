function onStart() {
    log('Started Javascript Service!');
    return true;
};

function onStop() {
    log('Stoped Javascript Service!');
    return true;
};

function onPause() {
    log('Paused Javascript Service!');
    return true;
};

function onContinue() {
    log('Continue Javascript Service!');
    return true;
};

function onShutdown() {
    log('Shutdown Javascript Service!');
    return true;
};