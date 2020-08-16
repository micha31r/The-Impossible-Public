function message_container_resize() {
	var parent_height = $(".notification-container").height();
	var h2_height = $(".notification-container h2").outerHeight(true);
	$(".message-container").height(parent_height - h2_height);
}

auto_run.queue( 
	function() {
		message_container_resize();
		window.addEventListener(
			"resize", 
			message_container_resize
		);
	}
);