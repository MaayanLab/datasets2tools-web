//////////////////////////////////////////////////
//////////////////////////////////////////////////
////////// Datasets2Tools Website Scripts ////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////

///////////////////////////////////
////////// 1. Main ////////////////
///////////////////////////////////

function main() {

	keywordSearch.main();
	advancedSearch.main();
	uploadForm.main();

};

///////////////////////////////////
////////// 2. Scripts /////////////
///////////////////////////////////

//////////////////////////////
///// 1. Keyword Search //////
//////////////////////////////

var keywordSearch = {

	// navigates to search url when clicking on search button
	submitSearch: function() {
		// event listener
		$('#search-button').click(function(evt) {

			// get object type
			objectType = $('input[type="radio"][name="radio"]:checked').attr('id');

			// get keywords
			var keywords = [];
			$('.tags-input').find('span').each(function(i, elem) {
				keywords.push($(elem).text());
			});

			// navigate
			if (keywords.length > 0) {
				window.location = 'search?object_type=' + objectType + '&keywords=' + keywords.join(', ')
			}
		})
	},

	// sets example when clicking on objects
	setExample: function() {

		$('input[type="radio"]').click(function(evt) {

			// get object type
			objectType = $(evt.target).attr('id');

			// change example
			if (objectType === 'analysis') {
				$('#search-example').html('Examples: <a class="search-example-link" href="#">enrichment, prostate cancer, upregulated</a>; or <a class="search-example-link" href="#">small molecule, reverse, myocardial infarction</a>.')
			} else if (objectType === 'dataset') {
				$('#search-example').html('Examples: <a class="search-example-link" href="#">breast cancer, estrogen positive</a>; or <a class="search-example-link" href="#">GSE10325</a>.')
			} else if (objectType === 'tool') {
				$('#search-example').html('Examples: <a class="search-example-link" href="#">enrichment</a>; or <a class="search-example-link" href="#">L1000</a>; or <a class="search-example-link" href="#">image data</a>.')
			}
		})

	},

	// searches example
	searchExample: function() {

		$(document).on('click', '.search-example-link', function(evt) {
			// get tags input
			var $tagsInput = $('.tags-input');

			// remove existing tags
			$tagsInput.find('.tag').remove();

			// add tags
			$.each($(evt.target).text().split(', ').reverse(), function(index, value) {
				$tagsInput.prepend('<span class="tag" data-tag="'+value+'">'+value+'</span>')
			})

			// search
			$('#search-button').click()
		})

	},

	// go back
	goBack: function() {

		$('#back-button').click(function(evt) {
			// scroll to
			setTimeout(function() {
				$('html, body').animate({
				        scrollTop: $("html").offset().top
				    }, 750);	
			}, 100)

			// hide results
			setTimeout(function(){
				$('#search-results-wrapper').css('display', 'none');
			}, 950)
		})

	},

	// checks if page has query and fixes accordingly
	pageSetup: function() {

		if ((window.location.href.indexOf('object_type=') !== -1) && (window.location.href.indexOf('keywords=') !== -1)) {

			// get tags and object type
			var tags = decodeURIComponent(window.location.href.split('keywords=')[1]).split(', '),
				objectType = window.location.href.split('object_type=')[1].split('&')[0];

			// click button
			$('#'+objectType).click();

			// add tags
			$.each(tags.reverse(), function(index, value) {
				$('.tags-input').prepend('<span class="tag" data-tag="'+value+'">'+value+'</span>');
			})

			// scroll to
			setTimeout(function() {
				$('html, body').animate({
				        scrollTop: $("#search-results-wrapper").offset().top
				    }, 750);	
			}, 500)

		} else {

			// click analysis
			$('#analysis').click();
			$('#search-results-wrapper').css('display', 'none');
		}

	},

	// main 
	main: function() {
		if (window.location.pathname === '/datasets2tools/search') {
			var self = this;
			self.submitSearch();
			self.setExample();
			self.searchExample();
			self.goBack();
			self.pageSetup();
		}
	}
};

//////////////////////////////
///// 2. Advanced Search /////
//////////////////////////////

var advancedSearch = {

	// change selections
	changeSelections: function(object_type) {
		$('.selectpicker-term.selectpicker-'+object_type).show();
		$('.selectpicker-term:not(.selectpicker-'+object_type+')').hide();
	},

	// manage selections
	changeSelectionListener: function() {
		var self = this,
			$objectSelector = $('#objectType');

		$(document).on('change', '#objectType', function(evt) {
			self.changeSelections($objectSelector.val());
		})

		self.changeSelections($objectSelector.val());
	},

	// add row listener
	addRow: function() {
		$(document).on('click', '.add-search-term-button', function(evt) {

			var $evtTarget = $(evt.target), // get button
				$rowToAdd = $('.filter-row:not(.active)').first(); // get row to add

			// show following row
			$rowToAdd.addClass('active');
		})
	},

	// remove row listener
	removeRow: function() {
		$(document).on('click', '.remove-search-term-button', function(evt) {

			var $evtTarget = $(evt.target), // get button
				$currentRow = $evtTarget.parents('.row'); // get current row

			// hide current row
			$currentRow.removeClass('active');

			// reset selections
			$currentRow.find('.selectpicker-term select').val('').selectpicker('refresh');
			$currentRow.find('#value').val('');
			$currentRow.find('#comparisonType').val('CONTAINS');
			$currentRow.find('#operatorType').val('AND');
		})
	},

	// build query
	buildQuery: function() {
		$(document).on('change', '#advanced-search-form', function(evt) {

			// get active rows
			var $activeRows = $('.filter-row.active'),
				$queryBox = $('#advanced-search-query'),
				query = '',
				$activeRow, separatorType, termName, comparisonType, value;

			// build query
			$activeRows.each(function(i, elem) {
				$activeRow = $(elem);
				separatorType = $activeRow.find('#separatorType').length === 0 ? '' : $activeRow.find('#separatorType').val(); // get operator type, set '' if not specified
				termName = $activeRow.find('.selectpicker-term button').attr('title').replace(' ', '_').toLowerCase(); // get term name
				comparisonType = $activeRow.find('#comparisonType').val(); // get comparison type
				value = '"'+$activeRow.find('#value').val()+'"'; // get comparison type

				query = '(' + query + [separatorType, termName, comparisonType, value].join(' ') + ') ' // build query
			})

			// add
			$queryBox.html(query.replace('( ', '('));
		})
	},

	// submit search
	submitSearch: function() {
		$(document).on('click', '#advanced-search-submit-button', function(evt) {
			var objectType = $('#objectType').val(), // get object type
				query = $('#advanced-search-query').text().trim(); // get search query

			window.location = 'advanced_search?object_type=' + objectType + '&query=' + query // submit search
		})
	},

	// main
	main: function() {
		if (window.location.pathname === '/datasets2tools/advanced_search') {
			var self = this;
			self.changeSelectionListener();
			self.addRow();
			self.removeRow();
			self.buildQuery();
			self.submitSearch();
		}
	}
};

//////////////////////////////
///// 3. Upload //////////////
//////////////////////////////

var uploadForm = {

	// change input method
	changeInputMethod: function() {

		$('.change-method label').click(function(evt) {
			var $evtTarget = $(evt.target), // get event target
				method = $evtTarget.hasClass('fa') ? $evtTarget.parent().attr('class').split(' ')[2] : $evtTarget.attr('class').split(' ')[2]; // get method

			$evtTarget.parents('.col-lg-4').find('.add-object-row.'+method).removeClass('hidden');
			$evtTarget.parents('.col-lg-4').find('.add-object-row:not(.'+method+')').addClass('hidden');
		})
	},

	// add object preview
	addObjectPreview: function(objectData, objectType) {
		var $addedObjectRow = $('#added-'+objectType+'-row');
		$addedObjectRow.removeClass('hidden');
		if (objectType === 'dataset') {
			$addedObjectRow.html('asd');
		} else if (objectType === 'tool') {
			$addedObjectRow.html('asd');
		}
	},

	// add object
	addObject: function(analysisObject) {
		var self = this;
		$('.add-object-button-row button').click(function(evt) {
			var $activeAddRow = $(evt.target).parents('.add-object-button-row').parent().find('.add-object-row:not(.hidden)'), // get active row
				objectType = $activeAddRow.attr('id').split('-')[1], objectData;
			if (objectType === 'dataset') {

				if ($activeAddRow.hasClass('select-method')) {
					objectData = $activeAddRow.find('option:selected').attr('value');
				} else if ($activeAddRow.hasClass('insert-method')) {
					objectData = {};
					$activeAddRow.find('input:not([role="textbox"])').each(function(i, elem) {
						objectData[$(elem).attr('id')] = $(elem).val();
					})
					objectData['repository_fk'] = $activeAddRow.find('option:selected').attr('value');
				}

				if (analysisObject[objectType].indexOf(objectData) === -1 && objectData != "" && Object.values(objectData).indexOf('') === -1 && analysisObject['dataset'].map(function(x) {return x['dataset_accession']}).indexOf(objectData['dataset_accession']) === -1) {
					analysisObject[objectType].push(objectData);
					self.addObjectPreview(analysisObject, objectType);
				}

			} else if (objectType === 'tool') {

				if ($activeAddRow.hasClass('select-method')) {
					objectData = $activeAddRow.find('option:selected').attr('value');
				} else if ($activeAddRow.hasClass('insert-method')) {
					objectData = {};
					$activeAddRow.find('input:not([role="textbox"])').each(function(i, elem) {
						objectData[$(elem).attr('id')] = $(elem).val();
					})
				}

				if (objectData != "" && Object.values(objectData).indexOf('') === -1) {
					analysisObject[objectType] = objectData;
					self.addObjectPreview(analysisObject, objectType);
				}

			}
		})

		return analysisObject;
	},

	// preview analysis
	previewAnalysis: function(analysisObject) {

		$('#preview-analysis-button-row button').click(function(evt) {
			var analysisData = {'metadata': {'keywords': []}};

			$('#input-analysis-row').find('input').each(function(i, elem) {
				analysisData[$(elem).attr('id')] = $(elem).val();
			})

			$('.tags-input').find('.tag').each(function(i, elem){ analysisData['metadata']['keywords'].push($(elem).attr('data-tag')); });

			$('#metadata-row-wrapper').find('.row').each(function(i, elem){ analysisData['metadata'][$(elem).find('.metadata-term').val()] = $(elem).find('.metadata-value').val() });

			if (analysisObject['dataset'] != [] && analysisObject['tool'] != '' && Object.values(analysisObject['analysis']).indexOf('') === -1) {
				console.log(analysisObject);
			}

		})

		return analysisObject;
	},

	// main
	main: function() {
		if (window.location.pathname === '/datasets2tools/upload') {
			var self = this,
				analysisObject = {'dataset': [], 'tool': '', 'analysis': {}};
			self.changeInputMethod();
			analysisObject = self.addObject(analysisObject);
			analysisObject = self.previewAnalysis(analysisObject);
		}
	}

};

var uploadForm2 = {

	// change dataset input
	changeDatasetInput: function() {

		// get divs
		var $newDatasetDiv = $('#add-new-dataset'),
			$selectDatasetDiv = $('#select-dataset-row');

		$(document).on('click', '#select-dataset', function(evt) {
			$newDatasetDiv.addClass('inactive');
			$selectDatasetDiv.removeClass('inactive');
		})

		$(document).on('click', '#add-dataset', function(evt) {
			$newDatasetDiv.removeClass('inactive');
			$selectDatasetDiv.addClass('inactive');
		})
	},

	// get object annotation
	getDatasetAnnotation: function($activeDatasetInput) {
		var isSelectMode = $activeDatasetInput.attr('id') === 'select-dataset-row', // get true if select mode
			datasetSummary; // get summary
		if (isSelectMode) {
			var datasetId = $activeDatasetInput.find('option:selected').attr('value'); // get dataset id
			if (datasetId != '') { // process if dataset is selected
				var datasetSummaryJson = $.ajax({ // get annotation from id

					async: false,

					url: 'http://localhost:5000/datasets2tools/api/dataset',

					data: {
					  'd.id':datasetId,
					},

					success: function(data) {
						return data;
					}

				}).responseText;

				datasetSummary = JSON.parse(datasetSummaryJson)['results'][0]; // convert to object
			}
		} else {

			var $elem, // define element
				isSelectpicker;

			datasetSummary = {} // define empty object

			$activeDatasetInput.find('.form-group input').each(function(i, elem) { // loop through form
				$elem = $(elem);
				isSelectpicker = $elem.attr('aria-label') === 'Search';
				console.log(isSelectpicker);
				if (!isSelectpicker) {
					datasetSummary[$elem.attr('id')] = $elem.val();
				} else {
					datasetSummary['repository_fk'] = $elem.parents('.bootstrap-select').find('option:selected').attr('value');
				}
			});
		}

		return datasetSummary;
	},

	// make dataset card
	makeDatasetCard: function(datasetInfo) {
		var row = `
		<div class="row added-dataset added-dataset-info" data-variable="dataset_fk" data-value="`+datasetInfo['id']+`">
			<div class="col-10 text-left lesspadding">
			 <p class="added-dataset-accession added-dataset-info" data-variable="dataset_accession" data-value="`+datasetInfo['dataset_accession']+`"><a class="added-dataset-info" data-variable="dataset_landing_url" data-value="`+datasetInfo['dataset_landing_url']+`" href="`+datasetInfo['dataset_landing_url']+`">`+datasetInfo['dataset_accession']+`</a></p>
			 <p class="added-dataset-title added-dataset-info" data-variable="dataset_title" data-value="`+datasetInfo['dataset_title']+`">`+datasetInfo['dataset_title']+`&nbsp<sup><i class="fa fa-info-circle fa-1x" aria-hidden="true" data-toggle="tooltip" data-placement="right" data-html="true" title="`+datasetInfo['dataset_description']+`"></i></sup></p>
			 <div class="added-dataset-info" data-variable="repository_fk" data-value="`+datasetInfo['repository_fk']+`"></div>
			</div>
			<div class="col-2 text-right lesspadding">
				<a class="remove-added-dataset" href="#">Remove</a>
			</div>
		</div>
		`.replace('\n', '');

		return row;
	},

	// add dataset
	addDataset: function() {
		var self = this,
			$selectedDatasetsCol = $('#selected-dataset-col'), // get dataset box
			$addDatasetWrapper = $('#add-dataset-wrapper'), // get add wrapper
			$activeDatasetInput, datasetInfo; // other variables

		$(document).on('click', '#submit-new-dataset-button', function(evt) { // listener for click of submit button

			$activeDatasetInput = $('#upload-dataset-form .dataset-input:not(.inactive)'); // get active input

			datasetAnnotation = self.getDatasetAnnotation($activeDatasetInput); // dataset annotation object

			if (datasetAnnotation === undefined || Object.values(datasetAnnotation).indexOf('') != -1) {
			} else {
				$selectedDatasetsCol.append(self.makeDatasetCard(datasetAnnotation)); // add card html
				$(function() {$('[data-toggle="tooltip"]').tooltip()})
				// $addDatasetWrapper.hide(); // hide adding options
			}

		})
	},

	// remove dataset
	removeDataset: function() {

		$(document).on('click', '.remove-added-dataset', function(evt) {
			$(evt.target).parents('.added-dataset').remove();
		})
	},

	// change tool input
	changeToolInput: function() {

		// get divs
		var $newToolDiv = $('#add-new-tool'),
			$selectToolDiv = $('#select-tool-row');

		$(document).on('click', '#select-tool', function(evt) {
			$newToolDiv.addClass('inactive');
			$selectToolDiv.removeClass('inactive');
		})

		$(document).on('click', '#add-tool', function(evt) {
			$newToolDiv.removeClass('inactive');
			$selectToolDiv.addClass('inactive');
		})
	},

	// add tool

	// main
	main: function() {
		if (window.location.pathname === '/datasets2tools/upload') {
			var self = this;
			self.changeDatasetInput();
			self.addDataset();
			self.removeDataset();
			self.changeToolInput();
		}
	}

};

///////////////////////////////////
////////// 3. Call ////////////////
///////////////////////////////////

main();
