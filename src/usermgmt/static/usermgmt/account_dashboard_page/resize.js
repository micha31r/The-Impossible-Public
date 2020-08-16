function notification_resize() {
	// Width 
	var container_width = $(".user-info").innerWidth() - 80; // 80 is wrapper padding (L & R)
	var user_info_container = $(".user-info-container").outerWidth();
	var padding = 40;
	var new_width = container_width - user_info_container - padding - 20; // 20px spacing
	$(".notification-container").width(new_width);
	// Height
	var padding_top = parseInt($(".notification-container").css("padding-top").replace("px",""));
	var new_height = $(".user-info").height() - padding_top;
	$(".notification-container").height(new_height);
}

auto_run.queue( 
	function() {
		notification_resize();
		window.addEventListener(
			"resize", 
			notification_resize
		);
	}
);