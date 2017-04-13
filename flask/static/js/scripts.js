$('#analyses').click();

$('#search-button').click(function(evt) {

	var objects = [];

	$('.btn.btn-primary.active').each(function(i, elem) {
		objects.push($(elem).attr('id'));
	});

	var keywords = [];

	$('.tags-input').find('span').each(function(i, elem) {
		keywords.push($(elem).text());
	});

	var alertdiv = '<div class="form-alert justify-content-center"><i class="fa fa-exclamation-circle fa-2x" aria-hidden="true"></i>Please fill in the following information.</div>'

	if (objects.length === 0) {
		$('#object-select-text .form-alert').hide();
		$('#object-select-text').prepend(alertdiv);
	}

	if (keywords.length === 0) {
		$('#keyword-input-text .form-alert').hide();
		$('#keyword-input-text').prepend(alertdiv);
	}

	if (objects.length > 0 && keywords.length == 0) {
		$('#object-select-text .form-alert').hide();
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
		      'obj': objects.join(','),
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
