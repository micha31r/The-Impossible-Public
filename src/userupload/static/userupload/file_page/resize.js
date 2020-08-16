function resize() {
	$("#hidden").css("display","block"); 
	var parent_height = $("#hidden").height();
	var parent_width = $("#hidden").width();
	if (parent_height <= 5) {
		parent_height = 350;
	}
    $("#file-wrapper").css("height", `${parent_height}`); 
    $("#blur").css("height", `${parent_height}`); 
    $("#blur").css("width", `${parent_width}`); 
    $("#hidden").css("display","none"); 
}

function show_spinner() {
	if ($("#id_file").val() && $("#id_description").val()) {
		$('.spinner-border').css('display','inline-block');
		$('.delete-btn').hide();
	}
}

// https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
function preview_image() {
	var accepted_formats = [
		"png",
		"jpg",
		"JPG",
		"jpeg",
		"JPEG",
		"gif",
		"svg"
	];
	var file = document.getElementById("id_file").files[0];
    var oFReader = new FileReader();
    oFReader.readAsDataURL(file);
    oFReader.onload = function (oFREvent) {
    	var extension = file.name.split(".");
    	extension = extension[extension.length-1];
    	// Only show preview if file is a type of image
    	if (accepted_formats.indexOf(extension) >= 0) {
        	document.getElementById("file-wrapper").style.backgroundImage = `url("${oFREvent.target.result}")`;
        	document.getElementById("hidden").src = oFREvent.target.result;
        	// Wait 1s for image to load then resize
			setTimeout(resize, 1000);
        } else {
        	document.getElementById("file-wrapper").style.backgroundImage = `none`;
        }
    };
};

auto_run.queue(
	function() {
		resize();
		// Set trigger
		$("#id_file").change(preview_image);
		window.addEventListener(
			"resize", 
			resize
		);
	}
);