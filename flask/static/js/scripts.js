////////////////////////////
////////// Search //////////
////////////////////////////

////////// 1. Object Button Listener

$('input[type="radio"]').click(function(evt) {
	var objects = $(evt.target).attr('id');

	if (objects === 'analyses') {
		$('#search-example').html('Examples: <a class="search-example-link" href="#">enrichment, prostate cancer, upregulated</a>; or <a class="search-example-link" href="#">small molecule, reverse, myocardial infarction</a>.')
	} else if (objects === 'datasets') {
		$('#search-example').html('Examples: <a class="search-example-link" href="#">breast cancer, estrogen positive</a>; or <a class="search-example-link" href="#">GSE10325</a>.')
	} else if (objects === 'tools') {
		$('#search-example').html('Examples: <a class="search-example-link" href="#">enrichment</a>; or <a class="search-example-link" href="#">L1000</a>; or <a class="search-example-link" href="#">image data</a>.')
	}

	$('.search-example-link').click(function(evt) {
		var $tags_input = $('#keyword-input-row').find('.tags-input');
		$tags_input.find('.tag').remove();
		$.each($(evt.target).text().split(', ').reverse(), function(index, value) {
			$tags_input.prepend('<span class="tag" data-tag="'+value+'">'+value+'</span>')
		})
		$('#search-button').click()
	})
});

$('#analyses').click();

////////// 2. Search Button Click Listener

$('#search-button').click(function(evt) {

	var objects = $('input[type="radio"][name="radio"]:checked').attr('id');
	var keywords = [];
	$('.tags-input').find('span').each(function(i, elem) {
		keywords.push($(elem).text());
	});

	if (keywords.length === 0) {
		console.log('asd');
	} else {

	$.ajax({
	url: 'http://localhost:5000/datasets2tools/keyword_search',
	data: {
	  'obj': objects,
	  'keywords': keywords.join(','),
	},

	success: function(data) {
		$("#search-results").html(data);
		$(function() {$('[data-toggle="tooltip"]').tooltip()});
	},

	error: function() {
		$("#search-results").html('Sorry, there was an error.');
	}
	});

	setTimeout(function() {
		$("#search-results-wrapper").show();
		$('html, body').animate({
		        scrollTop: $("#search-results-wrapper").offset().top
		    }, 750);	
	}, 750)
}

});

$('#back-button').click(function(evt) {
	setTimeout(function(){
		$("#search-results-wrapper").hide();
		$("#search-results").html('');
	}, 800);
	$('html, body').animate({
        scrollTop: $("#main-container").offset().top 
    }, 750);
});

