function layout_resize() {
	var container_width = $(".search-user-content").innerWidth();
	if ($(window).width() < 1020) {
		$(".search-user-content").prepend($(".search-profile-container"));
		$(".search-profile-container").width(container_width); // 2 is border width (L & R)
		$(".recent-idea-container").width(container_width);
	} else {
		$(".search-user-content").append($(".search-profile-container")); 
		$(".recent-idea-container").width(); 
		var sibling_width = $(".recent-idea-container").outerWidth();
		// Minus extra 10px just in case
		$(".search-profile-container").width(container_width-sibling_width-30);
	}

	if ($(window).width() < 720) {
		$(".wrapper").prepend($(".right"));
	} else {
		$(".wrapper").append($(".right"));
	}
}

auto_run.queue( 
	function() {
		layout_resize();
		window.addEventListener(
			"resize", 
			layout_resize
		);
	}
);