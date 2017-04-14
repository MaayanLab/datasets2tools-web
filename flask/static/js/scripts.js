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
		// var example_tags = '';
		var $tags_input = $('#keywords-label').find('.tags-input');
		$tags_input.find('.tag').remove();
		$.each($(evt.target).text().split(', ').reverse(), function(index, value) {
			$tags_input.prepend('<span class="tag" data-tag="'+value+'">'+value+'</span>')
		})
		$('#search-button').click()
	});
});

$('#analyses').click();

$('#search-button').click(function(evt) {

	var objects = $('input[type="radio"][name="radio"]:checked').attr('id');

	var keywords = [];

	$('.tags-input').find('span').each(function(i, elem) {
		keywords.push($(elem).text());
	});

	var alertdiv = '<div class="form-alert justify-content-center"><i class="fa fa-exclamation-circle fa-2x" aria-hidden="true"></i>Please fill in the following information.</div>'

	if (keywords.length === 0) {
		$('#keyword-input-text .form-alert').hide();
		$('#keyword-input-text').prepend(alertdiv);
	}

	if (objects.length == 0 && keywords.length > 0) {
		$('#keyword-input-text .form-alert').hide();
	}

	if (objects.length > 0 && keywords.length > 0) {
		$('.form-alert').hide();
		// var alertstring = 'You are searching <strong>' + objects.join('</strong>, <strong>') + '</strong> for the following keywords: <strong>' + keywords.join('</strong>, <strong>') + '</strong>.';
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
		    	$("#search-results").html('Sorry, no search results found for the specified query.');
		    }
		  });
		setTimeout(function() {
			$("#results_container").show();
			$('html, body').animate({
			        scrollTop: $("#results_container").offset().top - $('#navbar').height()
			    }, 750);	
		}, 500)
	}
});

$('#back-button').click(function(evt) {
	setTimeout(function(){
		$("#results_container").hide();
		$("#search-results").html('');
	}, 800);
	$('html, body').animate({
        scrollTop: $("#main_container").offset().top 
    }, 750);
});

