function table_resize() {
	// Idea setting
	if ($(window).width() < 831) {
		$("#idea-setting").appendTo("#append-target1");
	} else {
		$("#idea-setting").appendTo("#append-origin1");
	}

	// Exsisting tag
	if ($(window).width() < 460) {
		$("#exsisting-tag").appendTo("#append-target2");
	} else {
		$("#exsisting-tag").appendTo("#append-origin2");
	}

	// Delete option
	if ($(window).width() < 460) {
		$("#delete-button").appendTo("#append-target3");
	} else {
		$("#delete-button").appendTo("#append-origin3");
	}
}

auto_run.queue( 
	function() {
		table_resize();
		window.addEventListener(
			"resize", 
			table_resize
		);
	}
);