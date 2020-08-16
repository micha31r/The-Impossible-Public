function label_resize() {
	if ($(window).width() < 700) {
		console.log(23)
		$(".td-label").each(
			function(index) {
				$(this).appendTo(`#append-target${index+1}`);
			}
		);
	} else {
		$(".td-label").each(
			function(index) {
				$(this).prependTo(`#append-origin${index+1}`);
			}
		);
	}
}

auto_run.queue( 
	function() {
		label_resize();
		window.addEventListener(
			"resize", 
			label_resize
		);
	}
);