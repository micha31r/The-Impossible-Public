function container_resize() {
	var height = $(".content-wrapper").height() - $(".tab-switcher").outerHeight();
	$(".following-container").height(height);
	$(".follower-container").height(height);
}

auto_run.queue( 
	function() {
		container_resize();
		window.addEventListener(
			"resize", 
			container_resize
		);
	}
);