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
		rowHtml = '<div class="form-group row filter-row"><div class="col-1"><select class="form-control" id="operatorType"><option>AND</option><option>OR</option></select></div><div class="col-2"><select class="form-control" id="termName">'+fieldHtml+'</select></div><div class="col-2"><select class="form-control" id="comparisonType"><option>CONTAINS</option><option>IS</option><option>NOT CONTAINS</option><option>IS NOT</option></select></div><div class="col-sm-6"><input class="form-control" id="value"></div><div class="col-sm-1 text-left alter-search-term-col">'+minusIconHtml+plusIconHtml+'</div></div>';

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

function updateFilters() {
	var objectType = $('#objectType').val();

	$.ajax({
	url: 'http://localhost:5000/datasets2tools/advanced_search_terms',
	data: {
	  'object_type': objectType,
	},

	success: function(data) {
		$('#termName').html('<option>'+data.split('\n').join('</option><option>')+'</option>');
	},

	error: function() {
		$("#search-results").html('Sorry, there was an error.');
	}
	});
}

if (window.location.pathname === '/datasets2tools/advanced_search') {
	updateFilters();
}


$(document).on('change', '#objectType', function(evt) {
	updateFilters();
})

////////// 6. Advanced Search Query Builder

$('#advanced-search-form').submit(function(evt) {
	evt.preventDefault();
})

function updateQuery() {
	var $form = $('#advanced-search-form'),
	$formRows = $form.find('.filter-row'),
	objectType = $form.find('#objectType').val(),
	searchQuery = 'object IS ' + objectType.toLowerCase(),
	$formRow, termName, comparisonType, value, operatorType;

	$formRows.each(function(i, formRow) {
		$formRow = $(formRow);
		termName = $formRow.find('#termName').val();
		comparisonType = $formRow.find('#comparisonType').val();
		value = '"'+$formRow.find('#value').val()+'"';
		operatorType = i === 0? 'AND' : $formRow.find('#operatorType').val(); // Return AND if first filter row, otherwise looks it up
		searchQuery = '(' + searchQuery + ') ' + [operatorType, termName.replace(' ', '_').toLowerCase(), comparisonType, value].join(' ')
	})
	$('#advanced-search-query').html(searchQuery);
}

$(document).on("change", "#advanced-search-form", function(evt) {
	updateQuery();
})

$(document).on("click", '.remove-search-term-button', function(evt) {
	updateQuery();
})


////////// 7. Advanced Search Submission

$(document).on("click", "#advanced-search-submit-button", function(evt) {
	updateQuery();
	var searchQuery = $('#advanced-search-query').text().trim();
	if (searchQuery === 'Build an advanced search query using the options below.') {
	} else {
		window.location.href = window.location.href+'?query='+encodeURIComponent(searchQuery);
	}
})

////////// 8. Manual Upload

if (window.location.pathname === '/datasets2tools/manual_upload') {
	$('[role="combobox"]').attr('max-height', '300px')
	$(document).on(function() {
	});
}

////////// 9. Add Dataset

function addDatasetInputs() {
	var $newDatasetDiv = $('#new-dataset'),
		datasetInputsHtml = '<hr width="50%"><div class="form-group row"><label class="col-3 col-form-label lesspadding">Accession</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert accession..." id="datasetAccession"></div></div><div class="form-group row"><label class="col-3 col-form-label lesspadding">Title</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert title..." id="datasetTitle"></div></div><div class="form-group row"><label class="col-3 col-form-label lesspadding">Description</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert description..." id="datasetDescription"></div></div><div class="form-group row"><label class="col-3 col-form-label lesspadding">URL</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert URL..." id="datasetUrl"></div></div><div class="form-group row"><label class="col-3 col-form-label lesspadding">Repository</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert repository..." id="datasetRepository"></div></div>';
	$newDatasetDiv.html(datasetInputsHtml);
}

function fillDatasetInputs() {

	var selectedDatasetId = $('#datasetAccessionSelect option:contains('+$('[data-id="datasetAccessionSelect"]').attr('title')+')').attr('value');

	$.ajax({
		url: 'http://localhost:5000/datasets2tools/object_search',
		data: {
		  'object_type': 'dataset',
		  'id': selectedDatasetId
		},

		success: function(data) {
			var datasetMetadata = JSON.parse(data);
			$('#datasetAccession').val(datasetMetadata['dataset_accession']).prop('disabled', true)
			$('#datasetTitle').val(datasetMetadata['dataset_title']).prop('disabled', true)
			$('#datasetDescription').val(datasetMetadata['dataset_description']).prop('disabled', true)
			$('#datasetUrl').val(datasetMetadata['dataset_landing_url']).prop('disabled', true)
			$('#datasetRepository').val(datasetMetadata['repository_name']).prop('disabled', true)
		},

		error: function() {
			console.log('data');
		}
	});

}

$(document).on('change', '#dataset-accession-select-col', function(evt){
	addDatasetInputs();
	fillDatasetInputs();
})

$(document).on('click', '#new-dataset-button', function(evt){
	addDatasetInputs()
})

////////// 10. Add Tool

function addToolInputs() {
	var $newToolDiv = $('#new-tool'),
		toolInputsHtml = '<hr width="50%"><div class="row"><div id="selectedToolIcon" class="col-12 text-center"></div></div><div class="form-group row"><label class="col-3 col-form-label lesspadding">Name</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert name..." id="toolName"></div></div><div class="form-group row"><label class="col-3 col-form-label lesspadding">Description</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert description..." id="toolDescription"></div></div><div class="form-group row"><label class="col-3 col-form-label lesspadding">Homepage</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert homepage URL..." id="toolHomepageUrl"></div></div><div class="form-group row"><label class="col-3 col-form-label lesspadding">Icon</label><div class="col-8 lesspadding"><input class="form-control" type="text" placeholder="Insert icon URL..." id="toolIconUrl"></div></div>';
	$newToolDiv.html(toolInputsHtml);
}

function fillToolInputs() {

	var selectedDatasetId = $('#toolNameSelect option:contains('+$('[data-id="toolNameSelect"]').attr('title')+')').attr('value');

	$.ajax({
		url: 'http://localhost:5000/datasets2tools/object_search',
		data: {
		  'object_type': 'tool',
		  'id': selectedDatasetId
		},

		success: function(data) {
			var toolMetadata = JSON.parse(data);
			$('#selectedToolIcon').html('<img class="manual-upload-tool-icon" src="'+toolMetadata['tool_icon_url']+'">')
			$('#toolName').val(toolMetadata['tool_name']).prop('disabled', true)
			$('#toolDescription').val(toolMetadata['tool_description']).prop('disabled', true)
			$('#toolHomepageUrl').val(toolMetadata['tool_homepage_url']).prop('disabled', true)
			$('#toolIconUrl').val(toolMetadata['tool_icon_url']).prop('disabled', true)
		},

		error: function() {
			console.log('data');
		}
	});

}

$(document).on('change', '#tool-name-select-col', function(evt){
	addToolInputs();
	fillToolInputs();
})

$(document).on('click', '#new-tool-button', function(evt){
	addToolInputs()
})

////////// 10. Add Metadata Tags

if (window.location.pathname === '/datasets2tools/manual_upload') {

	var $metadataRowWrapper = $('#metadata-row-wrapper'),
		$metadataRowWrapperClone = $('#metadata-row-wrapper').clone(),
		$selectpicker = $('#selectpicker-original'),
		$selectpickerWrapper = $('#selectpicker-wrapper');

	$('.metadata-term-selectpicker').html($selectpickerWrapper.html());
	// $('.metadata-term-selectpicker').find('.form-control').addClass('selectpicker');

	$(document).on('click', '.add-tag-button', function(evt) {
		$metadataRowWrapper.append($metadataRowWrapperClone.html());
		$metadataRowWrapper.children().last().find('.metadata-term-selectpicker').html($selectpickerWrapper.html());
		// $metadataRowWrapper.children().last().find('.metadata-term-selectpicker').find('.form-control').addClass('selectpicker');
	})

}



