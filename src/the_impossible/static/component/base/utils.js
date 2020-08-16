// Get the current week
// https://gist.github.com/IamSilviu/5899269
Date.prototype.getWeek = function () {
    var onejan = new Date(this.getFullYear(), 0, 1);
    return Math.floor((((this - onejan) / 86400000) + onejan.getDay() + 1) / 7);
};

function current_date(element=null) {
	var today = new Date();
	var date = `${today.getFullYear()}-${today.getMonth()+1}-${today.getDate()}`;	
	if (element) {
		$(`#${element}`).html(date);
	} else {
		return date;
	}
}