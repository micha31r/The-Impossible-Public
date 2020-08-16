function newsletter_resize() {
	$(".vertical-card-img").height($(".vertical-card-body").outerHeight()); 	
}


auto_run.queue( 
	function() {
		newsletter_resize();
		window.addEventListener(
			"resize", 
			newsletter_resize
		);
	}
);