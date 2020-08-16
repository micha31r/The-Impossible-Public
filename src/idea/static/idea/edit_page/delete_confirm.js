var click_count = 3;

function click_confirm(element_id,button_id) {
	click_count -= 1;
	$(`#${button_id}`).html(`Confirm ${click_count}`);
	if (click_count <= 0) {
		$(`#${element_id}`).css("display","block");
		$(`#${button_id}`).remove();
	}
}
