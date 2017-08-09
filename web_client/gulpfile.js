var gulp       = require('gulp');
// var sourcemaps = require('gulp-sourcemaps');
var source     = require('vinyl-source-stream');
var buffer     = require('vinyl-buffer');
var browserify = require('browserify');
var watchify   = require('watchify');
var babel      = require('babelify');
var sass       = require('gulp-sass');
var jsmin = require('gulp-jsmin');

var conf = {
  // JavaScript
  appName:  ['shop_detail.js' , 'category_detail.js', 'globalcategory_detail.js', 'product_list.js'],
  srcJs:    './',
  destName: ['shop_detail.js', 'category_detail.js', 'globalcategory_detail.js', 'product_list.js'],
  destJs:   '../static/js/',
};

function compile(watch) {
  conf.appName.forEach(function (value) {
    var bundler = watchify(
    browserify(conf.srcJs + '/' + value, { debug: true })
      .transform(babel.configure({ presets: ['es2015', 'react'] })
      )
    );

  function rebundle() {
    bundler.bundle()
      .on('error', function(err) { console.error(err); this.emit('end'); })
      .pipe(source(value))
      .pipe(buffer())
      // .pipe(sourcemaps.init({ loadMaps: true }))
      // .pipe(sourcemaps.write('./'))
      .pipe(jsmin())
      .pipe(gulp.dest(conf.destJs));
  }



  if (watch) {
    bundler.on('update', function() {
      console.log('-> building...');
      rebundle();
      console.log('->done');
    });
  }

  rebundle();
  });
}

function watch() {
  return compile(true);
};


gulp.task('build', function() { return compile(); });
gulp.task('watch', ['build'], function() { return watch();  });
gulp.task('default', ['watch']);

