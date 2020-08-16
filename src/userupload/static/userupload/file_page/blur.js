$(document).ready(
	function() { 
	    $("#file-wrapper").hover(
	    	function() { 
		        $("#blur").css("opacity", "0.5"); 
		        $("#file-button").css("opacity", "1"); 
		    }, 
		    function() { 
		        $("#blur").css("opacity", "0"); 
		        $("#file-button").css("opacity", "0"); 
		    }
		); 
	}
); 