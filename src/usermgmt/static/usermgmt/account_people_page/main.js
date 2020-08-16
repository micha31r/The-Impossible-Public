function get_tab_num() {
	if (!current_tab) {
		change_tab_num(1);
	}
}

function change_tab_num(num) {
	localStorage.setItem('current_tab', num);
	current_tab = num;
}

function change_tab() {
	if (current_tab == 1) {
		$('.follower-tab').attr("name","current");
		$(".following-container").hide();
		$(".following-page-link").hide();
		$(".follower-container").show();
		$(".follower-page-link").show();
	} else {
		$('.following-tab').attr("name","current");
		$(".following-container").show();
		$(".following-page-link").show();
		$(".follower-container").hide();
		$(".follower-page-link").hide();
	}
}

var current_tab = localStorage.getItem('current_tab');
get_tab_num();

auto_run.queue(
	function() {
		change_tab();
		$(".tab-switcher *").click(
			function() {
				$('h3[name="current"]').attr("name","");
				$(this).attr("name","current");

				// Show corresponding element
				if ($(".follower-tab").attr("name") == "current") {
					change_tab_num(1);
				} else {
					change_tab_num(2);
				}
				change_tab();
				console.log(current_tab);
			}
		);
	}
);