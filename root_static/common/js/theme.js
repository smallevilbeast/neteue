/**
 * @author Chine
 */

function switchTheme(theme) {
 	$.cookie('blog_theme', theme, { expires: 30 });
	location.href = location.href;
}
