function explore_height(recursion) {
	var element = document.getElementsByClassName("flex-container")[0];
	// Reset element height
	if (!recursion) { 
		element.style.height = "500px";
	}
	if (element.scrollWidth > element.clientWidth) {
		// Adjust to the new height
		var new_height = element.clientHeight += 100;
		element.style.height = `${new_height}px`;
		// Repeat process
		explore_height(true);
	} 
}

function announcement_padding() {
	var extra = $(".announcement-wrapper").outerWidth() - $(".announcement-wrapper div").outerWidth();
	if (extra > 0) {
		$(".announcement-wrapper").css("padding-left",`${extra/2}px`);
	} else {
		$(".announcement-wrapper").css("padding-left",`40px`);
	}
}

var w_width = window.innerWidth; 

auto_run.queue(
	function() {
		explore_height();
		announcement_padding();
		window.addEventListener(
			"resize", 
			function() {
		    	// Do nothing if the width is the same
			    if ($(window).width() != w_width) { 
				    // update new width value
				    w_width = $(window).width();
				    explore_height(); 
					announcement_padding();
				}
			}
		);
	}
);
