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

////////// 3. Back Button Click Listener

$('#back-button').click(function(evt) {
	setTimeout(function(){
		$("#search-results-wrapper").hide();
		$("#search-results").html('');
	}, 800);
	$('html, body').animate({
        scrollTop: $("#main-container").offset().top 
    }, 750);
});

////////// 4. Advanced Search Plus Button Listener

var	plusIconHtml = '<i class="fa fa-2x fa-plus-circle search-term-button add-search-term-button" aria-hidden="true"></i>',
	minusIconHtml = '<i class="fa fa-2x fa-minus-circle search-term-button remove-search-term-button" aria-hidden="true"></i>';

$(document).on("click", '.add-search-term-button', function(evt) {
	var $evtTarget = $(evt.target),
		$submitRow = $evtTarget.parents('#advanced-search-form').find('#submit-button-row'),
		isFirstRow = $evtTarget.parents('.filter-row').find('label').length === 1,
		fieldHtml = $('#termName').html(),
		rowHtml = '<div class="form-group row filter-row"><div class="col-1"><select class="form-control" id="operatorType"><option>AND</option><option>OR</option></select></div><div class="col-2"><select class="form-control" id="termName">'+fieldHtml+'</select></div><div class="col-2"><select class="form-control" id="comparisonType"><option>CONTAINS</option><option>IS</option><option>NOT CONTAINS</option><option>NOT</option></select></div><div class="col-sm-6"><input class="form-control" id="value"></div><div class="col-sm-1 text-left alter-search-term-col">'+minusIconHtml+plusIconHtml+'</div></div>';

	if (!isFirstRow) {
		$evtTarget.parent().html(minusIconHtml);
	} else {
		$evtTarget.parent().html('');
	}
	$submitRow.before(rowHtml);
})

$(document).on("click", '.remove-search-term-button', function(evt) {
	var $evtTarget = $(evt.target),
		$row = $evtTarget.parents('.filter-row'),
		isLastRow = $row.next().attr('id') === 'submit-button-row',
		isSecondRow = $row.prev().find('label').length === 1;

	if ((isLastRow && isSecondRow) ) {
		$(evt.target).parents('.filter-row').prev().find('.alter-search-term-col').html(plusIconHtml);// Add plus icon to first row
	} else if ((isLastRow && !isSecondRow)) {
		$(evt.target).parents('.filter-row').prev().find('.alter-search-term-col').html(minusIconHtml+plusIconHtml); // Add plus and minus icon to previous row
	}
	$(evt.target).parents('.filter-row').remove(); // Remove row
})

////////// 5. Advanced Search Query Builder

$(document).on("change", "#advanced-search-form", function(evt) {
	var $form = $('#advanced-search-form'),
		$formRows = $form.find('.filter-row'),
		objectType = $form.find('#objectType').val(),
		searchQuery = 'Object = ' + objectType,
		$formRow, termName, comparisonType, value, operatorType;

	$formRows.each(function(i, formRow) {

		$formRow = $(formRow);
		termName = $formRow.find('#termName').val();
		comparisonType = $formRow.find('#comparisonType').val();
		value = $formRow.find('#value').val();
		operatorType = i === 0? 'AND' : $formRow.find('#operatorType').val(); // Return AND if first filter row, otherwise looks it up

		if (value.length > 0) {
			searchQuery = '(' + searchQuery + ') ' + [operatorType, termName, comparisonType, value].join(' ')
		}

		// console.log([$formRow.find('#termName').val(), $formRow.find('#comparisonType').val(), $formRow.find('#value').val()].join(' '));
	})

	$('#advanced-search-query').html(searchQuery);

})

