var gulp         	= require('gulp'),
    sass         	= require('gulp-sass'),
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

gulp.task('watch', function () {
    gulp.watch('gulp/sass/*.sass', ['styles']);
});

gulp.task('removedist', function() { return del.sync('dist'); });

gulp.task('default', ['watch']);
