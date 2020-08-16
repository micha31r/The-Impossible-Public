// This file should be linked to the end of the HTML of the newsletter form 
function newsletter_fade() {
	$(".subscribe-blur, .subscribe-wrapper, #hide-subscribe-form").css("animation-name","newsletter-form-hide");
}

function newsletter_unfade() {
	$(".subscribe-blur, .subscribe-wrapper, #hide-subscribe-form").css("animation-name","newsletter-form-show");
}

// Hide element 
// If function is called by window.onload then user can see the form dissapear
$(".subscribe-blur, .subscribe-wrapper, #hide-subscribe-form").css("visibility","hidden");

auto_run.queue( 
	function() {
		form_action();
	}
);

function form_action() {
	var interval_id = setInterval(
		function() {
			newsletter_unfade();
			$("#hide-subscribe-form").css("display","block");
			clearInterval(interval_id);
		},
		10000 // Delay 10 seconds before showing form
	);
}