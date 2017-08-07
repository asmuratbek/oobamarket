var gulp         	= require('gulp'),
    gutil           = require('gulp-util'),
    browserify      = require('browserify'),
    sass         	= require('gulp-sass'),
    source          = require('vinyl-source-stream'),
    autoprefixer 	= require('gulp-autoprefixer'),
    cleanCSS    	= require('gulp-clean-css'),
    rename       	= require('gulp-rename'),
    browserSync  	= require('browser-sync').create(),
    uglify       	= require('gulp-uglify'),

    del 			= require('del');
    rename = require('gulp-rename');

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
            extensions: ['.jsx'],
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

//     return browserify({
//             entries: './web_client/app.jsx',
//             extensions: ['.js'],
//             debug: true
//         })
//         .transform('babelify', {
//             presets: ['es2015', 'react'],
//             plugins: ['transform-class-properties']
//         })
//         .bundle()
//         .on('error', function(err){
//             gutil.log(gutil.colors.red.bold('[browserify error]'));
//             gutil.log(err.message);
//             this.emit('end');
//         })
//         .pipe(source('app.js'))
//         .pipe(gulp.dest('static/js'));
});

gulp.task('shop', function(){
    module.exports = {
        entry: ["babel-polyfill", "./web_client/shop_detail.js"]
    };
   return browserify({
            entries: './web_client/shop_detail.js',
            extensions: ['.jsx'],
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
        .pipe(source('shop_detail.js'))
        .pipe(gulp.dest('static/js'));

});

gulp.task('category', function(){
   return browserify({
            entries: './web_client/category_detail.js',
            extensions: ['.jsx'],
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
        .pipe(source('category_detail.js'))
        .pipe(gulp.dest('static/js'));

});

gulp.task('globalcategory', function(){
   return browserify({
            entries: './web_client/globalcategory_detail.js',
            extensions: ['.jsx'],
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
        .pipe(source('globalcategory_detail.js'))
        .pipe(gulp.dest('static/js'));

});

gulp.task('min', function () {
    gulp.src('static/js/globalcategory_detail.js')
        .pipe(jsmin())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('static/js'));
    gulp.src('static/js/category_detail.js')
        .pipe(jsmin())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('static/js'));
    gulp.src('static/js/shop_detail.js')
        .pipe(jsmin())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('static/js'));
});


gulp.task('watch', function () {
    gulp.watch('gulp/sass/*.sass', ['styles']);
});

gulp.task('removedist', function() { return del.sync('dist'); });

gulp.task('default', ['watch']);
