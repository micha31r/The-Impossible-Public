// .reverse function
// https://stackoverflow.com/questions/1394020/jquery-each-backwards
jQuery.fn.reverse = [].reverse;

function form_resize() {
	$(".form-wrapper").css("max-width",`none`);
	var menu_width = $("#menu").width();
	if ($(window).width() < 700) {
		menu_width = 0;
	}
	var new_width = $(".table-wrapper").width() - menu_width;
	$(".form-wrapper").css("max-width",`${new_width}px`);
}

function menu_resize() {
	if ($(window).width() < 700) {
		$("#menu").children().each(
			function() {
				$(this).appendTo("#minify-menu");
			}
		);
	} else {
		$("#minify-menu").children().reverse().each(
			function() {
				$(this).prependTo("#menu");
			}
		);
	}
}

function input_resize() {
	if ($(window).width() < 700) {
		// 80 is .table-wrapper's padding (L & R)
		var new_width = $(".table-wrapper").width() - 80;
		$("input").css("width",`${new_width}px`);
	} else {
		$("input").css("width","100%");
	}
}

auto_run.queue( 
	function() {
		form_resize();
		menu_resize();
		input_resize();
		window.addEventListener(
			"resize", 
			function() {
				form_resize();
				menu_resize();
				input_resize();
			}
		);
	}
);