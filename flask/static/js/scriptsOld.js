
////////// 1. Object Button Listener

$('input[type="radio"]').click(function(evt) {
	var objects = $(evt.target).attr('id');



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
	url: 'http://amp.pharm.mssm.edu/datasets2tools/datasets2tools/keyword_search',
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
	url: 'http://amp.pharm.mssm.edu/datasets2tools/datasets2tools/advanced_search_terms',
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
	// Show
	$('#new-dataset').show();

	// Reset
	$('#new-dataset select').val('').selectpicker('refresh');
	$('[data-id="repositoryNameSelect"]').prop('disabled', false).css('background-color', 'white').attr('title', 'Select repository...');
	$('[data-id="repositoryNameSelect"] .filter-option').css('color', '');
	$('#new-dataset .form-control').prop('disabled', false).val('');
}

function fillDatasetInputs() {

	var selectedDatasetId = $('#datasetAccessionSelect option:contains('+$('[data-id="datasetAccessionSelect"]').attr('title')+')').attr('value');

	$.ajax({
		url: 'http://amp.pharm.mssm.edu/datasets2tools/datasets2tools/object_search',
		data: {
		  'object_type': 'dataset',
		  'd.id': selectedDatasetId
		},

		success: function(data) {
			var datasetMetadata = JSON.parse(data);
			$('#new-dataset').attr('data-dataset-id', selectedDatasetId);
			$('#dataset_accession').val(datasetMetadata['dataset_accession']).prop('disabled', true);
			$('#dataset_title').val(datasetMetadata['dataset_title']).prop('disabled', true);
			$('#dataset_description').val(datasetMetadata['dataset_description']).prop('disabled', true);
			$('#dataset_landing_url').val(datasetMetadata['dataset_landing_url']).prop('disabled', true);
			$('[data-id="repositoryNameSelect"] .filter-option').text(datasetMetadata['repository_name']).css('color', 'black');
			$('[data-id="repositoryNameSelect"]').prop('disabled', true).css('background-color', 'transparent').attr('title', '');
			$('[data-id="repositoryNameSelect"]').parent().css('background-color', 'transparent');
			// $('[data-id="repositoryNameSelect"]').val(datasetMetadata['repository_name']).prop('disabled', true);
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
	$('#new-dataset').removeAttr('data-dataset-id');
	$('#dataset-accession-select-col select').val('').selectpicker('refresh');
})

////////// 10. Add Tool

function addToolInputs() {
	// Show
	$('#new-tool').show();

	// Reset
	$('#new-tool .form-control').prop('disabled', false).val('');
	$('#manual-upload-tool-icon').hide();
}

function fillToolInputs() {

	var selectedToolId = $('#toolNameSelect option:contains('+$('[data-id="toolNameSelect"]').attr('title')+')').attr('value');

	$.ajax({
		url: 'http://amp.pharm.mssm.edu/datasets2tools/datasets2tools/object_search',
		data: {
		  'object_type': 'tool',
		  'id': selectedToolId
		},

		success: function(data) {
			var toolMetadata = JSON.parse(data);
			$('#new-tool').attr('data-tool-id', selectedToolId);
			$('#selectedToolIcon').html('<img id="manual-upload-tool-icon" src="'+toolMetadata['tool_icon_url']+'">')
			$('#tool_name').val(toolMetadata['tool_name']).prop('disabled', true)
			$('#tool_description').val(toolMetadata['tool_description']).prop('disabled', true)
			$('#tool_homepage_url').val(toolMetadata['tool_homepage_url']).prop('disabled', true)
			$('#tool_icon_url').val(toolMetadata['tool_icon_url']).prop('disabled', true)
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
	addToolInputs();
	$('#upload-tool-form select').val('').selectpicker('refresh');
	$('#new-tool').removeAttr('data-tool-id');
})

////////// 10. Add Metadata Tags

if (window.location.pathname === '/datasets2tools/manual_upload') {

	var $metadataRowWrapper = $('#metadata-row-wrapper')
		rowHtml = '<div class="form-group row metadata-row"><label class="col-3 col-form-label lesspadding alter-tag-col-left"><i class="fa fa-1x fa-plus-circle alter-tag-button add-tag-button" aria-hidden="true"></i>&nbsp<i class="fa fa-1x fa-minus-circle alter-tag-button remove-tag-button" aria-hidden="true"></i></label><div class="col-4 lesspadding metadata-term-selectpicker"><input class="form-control" type="text" placeholder="Insert term..." id="metadataTerm"></div><div class="col-4 lesspadding"><input class="form-control" type="text" placeholder="Insert value..." id="metadataValue"></div></div>';

}

$(document).on('click', '.add-tag-button', function(evt) {
	$(evt.target).hide();
	$metadataRowWrapper.append(rowHtml);
})

$(document).on('click', '.remove-tag-button', function(evt) {
	var $evtTarget = $(evt.target),
		$parentRow = $(evt.target).parents('.metadata-row'),
		$previousRow = $parentRow.prev(),
		isLastRow = $parentRow.next().length === 0,
		isSecondRow = $previousRow.find('label').text() === 'Tags';

	if ((isLastRow)) {
		$previousRow.find('.add-tag-button').show();
	}
	$parentRow.remove();
})

////////// 11. Submit Analysis

function getFormData($formWrapper) {

	var formData = {};

	$formWrapper.find('.form-group input').each(function(i, elem) {
		var $elem = $(elem),
			id = $elem.attr('id'),
			value = $elem.val();
		formData[id] = value;
	})

	return formData
}

function getAnalysisMetadata($metadataWrapper) {

	var metadata = {},
		$keywordTags = $metadataWrapper.find('.tags-input .tag'),
		$tagRows = $metadataWrapper.find('#metadata-row-wrapper .metadata-row');

	if ($keywordTags.length > 0) {
		metadata['keywords'] = [];
		$keywordTags.each(function(i, elem) {
			metadata['keywords'].push($(elem).text());
		})
	}

	$tagRows.each(function(i, elem) {
		var $elem = $(elem),
			termName = $elem.find('#metadataTerm').val(),
			termValue = $elem.find('#metadataValue').val();
		if ((termName.length > 0) && (termValue.length > 0)) {
			metadata[termName] = termValue;
		}
	})
	return metadata
}

function prepareCannedAnalysisJSON() {

	var datasetId = $('#new-dataset').attr('data-dataset-id'),
	toolId = $('#new-tool').attr('data-tool-id'),
	objectData = {};

	// Dataset
	objectData['dataset'] = getFormData($('#new-dataset'));
	if (datasetId) {
		objectData['dataset']['id'] = datasetId;
	}

	// Tool
	objectData['tool'] =  getFormData($('#new-tool'));
	if (toolId) {
		objectData['tool']['id'] = toolId;
	}

	// Analysis
	objectData['analysis'] = getFormData($('#analysis-data-wrapper'));

	// Analysis Metadata
	objectData['analysis_metadata'] = getAnalysisMetadata($('#analysis-metadata-wrapper'));

	// Convert to JSON
	jsonObject = JSON.stringify(objectData);

	// Return
	return jsonObject
}

$(document).on('click', '#submit-analysis-button', function(evt) {

	var cannedAnalysisJson = prepareCannedAnalysisJSON();

	$.ajax({
		url: 'http://amp.pharm.mssm.edu/datasets2tools/datasets2tools/prepare_canned_analysis_table',
		data: {
		  'canned_analysis_json': encodeURIComponent(cannedAnalysisJson)
		},

		success: function(data) {
			$('#upload-results').html(data);
			$('#results').show(easing='swing');
			$('#form-upload-row').hide();
			$(function() {$('[data-toggle="tooltip"]').tooltip()})
		},

		error: function() {
			console.log('Sorry, there has been an error.');
		}
	});
})

$(document).on('click', '#review-submission-button', function(evt) {
	$('#results').hide();
	$('#form-upload-row').show(easing='linear');
})

