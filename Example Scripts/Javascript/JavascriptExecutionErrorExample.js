function failOnCall() {
    log('This is about to fail!');
    throw new Error();
};

failOnCall();