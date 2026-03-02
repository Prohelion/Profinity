module.exports = {
  style: {
    sass: {
      loaderOptions: {
        implementation: require('sass'),
        sassOptions: {
          outputStyle: 'compressed',
        },
      },
    },
  },
}; 