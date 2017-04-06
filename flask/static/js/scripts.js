$('#search-button').click(function(evt) {

	var tools = [];

	$('.btn.btn-primary.active').each(function(i, elem) {
		tools.push($(elem).attr('id'));
	});

	var keywords = [];

	$('.tags-input').find('span').each(function(i, elem) {
		keywords.push($(elem).text());
	});

	var alertstring = 'Searching ' + tools.join(', ') + ' for keywords: ' + keywords.join(', ');

	alert(alertstring)
});