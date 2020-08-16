// Create a task queue for window.onload
class AutoRun {
	constructor() {
		this.tasks = [];
	}

	// Add task
	queue(func) {
		this.tasks.push(func);
	}

	// Remove task
	unqueue(func) {
		for (var i=0; i<this.tasks.length; i++) {
			if (this.tasks[i] === func) {
				this.tasks.push(func);
			}
		}
	}

	// Execute all tasks
	execute() {
		for (var i=0; i<this.tasks.length; i++) {
			this.tasks[i]();
		}
	}
}

// Aspect ratio difference, x - y
function aspect_diff() {
	return Math.abs($(window).width() - $(window).height())
}

function active_link() {
	$(document).ready(
		function() {
		    $("[href]").each(
		    	function() {
			        if (this.href == window.location.href) {
			            $(this).addClass("active-link");
			        }
		    	}
		    );
		}
	);
}

