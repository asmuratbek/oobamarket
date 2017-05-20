var gulp         	= require('gulp'),
    gutil           = require('gulp-util'),
    browserify      = require('browserify'),
    babelify        = require('babelify'),
    sass         	= require('gulp-sass'),
    source          = require('vinyl-source-stream'),
    autoprefixer 	= require('gulp-autoprefixer'),
    cleanCSS    	= require('gulp-clean-css'),
    rename       	= require('gulp-rename'),
    browserSync  	= require('browser-sync').create(),
    uglify       	= require('gulp-uglify'),

    del 			= require('del');

gulp.task('styles', function () {
    return gulp.src('gulp/sass/*.sass')
        .pipe(sass({
            includePaths: require('node-bourbon').includePaths
        }).on('error', sass.logError))
        .pipe(rename({suffix: '.min', prefix : ''}))
        .pipe(autoprefixer({browsers: ['last 15 versions'], cascade: false}))
        .pipe(cleanCSS())
        .pipe(gulp.dest('static/css'))
        .pipe(browserSync.stream());
});

gulp.task('js', function(){
   return browserify({
            entries: './web_client/app.js',
            extensions: ['.js'],
            debug: true
        })
        .transform('babelify', {
            presets: ['es2015', 'react'],
            plugins: ['transform-class-properties']
        })
        .bundle()
        .on('error', function(err){
            gutil.log(gutil.colors.red.bold('[browserify error]'));
            gutil.log(err.message);
            this.emit('end');
        })
        .pipe(source('app.js'))
        .pipe(gulp.dest('static/js'));
});

gulp.task('watch', function () {
    gulp.watch('gulp/sass/*.sass', ['styles']);
});

gulp.task('removedist', function() { return del.sync('dist'); });

gulp.task('default', ['watch']);
