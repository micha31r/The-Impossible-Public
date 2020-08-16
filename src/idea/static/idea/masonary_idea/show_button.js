auto_run.queue(
	function() {
		$(".card").hover(
			function() {
				var element_id = $(this).attr('id').split("-");
				var id_number = element_id[element_id.length-1];
				$(`#card-like-${id_number}`).css("display","inline");
				$(`#card-like-${id_number}`).css("animation-name","show-card-button");
				$(`#card-bookmark-${id_number}`).css("display","inline");
				$(`#card-bookmark-${id_number}`).css("animation-name","show-card-button");
			},
			function() {
				var element_id = $(this).attr('id').split("-");
				var id_number = element_id[element_id.length-1];
				$(`#card-like-${id_number}`).css("animation-name","hide-card-button");
				$(`#card-bookmark-${id_number}`).css("animation-name","hide-card-button");
			}
		)
	}
);