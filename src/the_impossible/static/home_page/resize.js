function resize() {
	var height = 600 - $("nav").outerHeight() - 100;
	if ($(window).height() > 600) {
		height = $(window).height() - $("nav").outerHeight() - 100;
	}
	$(".wrapper").first().height(`${height}px`);
	$(".black").height($("body").height());
}

auto_run.queue(
	function() {
		resize();
		window.addEventListener(
			"resize", 
			function(){ resize(); }
		);
	}
);
