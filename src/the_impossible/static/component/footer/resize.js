function footer_resize() {
	$("#contact-td").appendTo("#footer-append-origin1");
	if ($(window).width() < 320) {
		$("#contact-td").appendTo("#footer-append-target1");
	}
}

auto_run.queue(
	function() {
		footer_resize();
		window.addEventListener(
			"resize", 
			function() {
				footer_resize();
			}
		);
	}
);