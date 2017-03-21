$(".dropdown-menu li a").click(function(){
	  $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
	  $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
});

$('#d2t-search-form').on('submit', function(evt) {

	// Prevent default
	evt.preventDefault();

	// Get search query
	var searchQuery = $('#d2t-search-input').val().trim();

	// If search query
	if (searchQuery.length > 0) {
		// Get search type
		var searchType = $('#d2t-search-type').text().toLowerCase().replace(' ', '').trim();

		// Get search URL
		var searchURL = 'http://localhost:5000/datasets2tools/' + searchType + '?query=' + searchQuery

		// Navigate
		window.location.href = searchURL		
	}
});
