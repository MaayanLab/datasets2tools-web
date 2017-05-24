//////////////////////////////////////////////////
//////////////////////////////////////////////////
////////// Datasets2Tools Website Scripts ////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////

///////////////////////////////////
////////// 1. Main ////////////////
///////////////////////////////////

function main() {

	homepage.main();
	keywordSearch.main();
	advancedSearch.main();
	uploadForm.main();
	help.main();

};

///////////////////////////////////
////////// 2. Scripts /////////////
///////////////////////////////////

//////////////////////////////
///// 1. Homepage //////
//////////////////////////////

var homepage = {
	main: function() {

	}
};

//////////////////////////////
///// 2. Keyword Search //////
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
///// 3. Advanced Search /////
//////////////////////////////

var advancedSearch = {

	// change selections
	changeSelections: function(object_type) {
		$('.selectpicker-term.selectpicker-'+object_type).removeClass('hidden');
		$('.selectpicker-term:not(.selectpicker-'+object_type+')').addClass('hidden');
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
				termName = $activeRow.find('.selectpicker-term:not(.hidden) option:selected').attr('value'); // get term name
				comparisonType = $activeRow.find('#comparisonType').val(); // get comparison type
				value = '"'+$activeRow.find('#value').val()+'"'; // get value

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
///// 4. Upload //////////////
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
		var $addedObjectRow = $('#added-'+objectType+'-row'),
			$addedObjectCol = $('#added-'+objectType+'-col'),
			objectSummary, objectPreviewHtml;
		$addedObjectRow.removeClass('hidden');
		if (objectType === 'dataset') {
			var datasetIdentifier;

			if (typeof objectData === 'string') {
				datasetIdentifier = objectData;
				objectSummary = JSON.parse($.ajax({ // get annotation from id
					async: false,
					url: 'http://amp.pharm.mssm.edu/datasets2tools/api/dataset',
					data: {
					  'd.id':objectData,
					},
					success: function(data) {
						return data;
					}
				}).responseText)['results'][0];
			} else if (typeof objectData === 'object') {
				datasetIdentifier = objectData['dataset_accession'];
				objectSummary = objectData;
			}

			objectPreviewHtml =`
	 		<div class="row added-object added-dataset" id="`+datasetIdentifier+`">
				<div class="col col-10 text-left">
				 <div class="added-dataset-accession"><a href="`+objectSummary['dataset_landing_url']+`">`+objectSummary['dataset_accession']+`</a></div>
				 <div class="added-dataset-title">`+objectSummary['dataset_title']+`&nbsp<sup><i class="fa fa-info-circle fa-1x" aria-hidden="true" data-toggle="tooltip" data-placement="right" data-html="true" title="`+objectSummary['dataset_description']+`"></i></sup></div>
				</div>
				<div class="col col-2 text-right">
					<a class="remove-added-dataset" href="#">Remove</a>
				</div>
			</div>
			`.replace('\n', '');;

			$addedObjectCol.append(objectPreviewHtml);
			$('[data-toggle="tooltip"]').tooltip();

		} else if (objectType === 'tool') {

			if (typeof objectData === 'string') {
				objectSummary = JSON.parse($.ajax({ // get annotation from id
					async: false,
					url: 'http://amp.pharm.mssm.edu/datasets2tools/api/tool',
					data: {
					  'id':objectData,
					},
					success: function(data) {
						return data;
					}
				}).responseText)['results'][0];
			} else if (typeof objectData === 'object') {
				objectSummary = objectData;
			}

			objectPreviewHtml =`
	 		<div class="row added-object added-tool">
				<div class="col col-12 text-left">
				<div>
	 				<img class="added-tool-icon" src="`+objectSummary['tool_icon_url']+`">
					 <a class="added-tool-name" href="`+objectSummary['tool_homepage_url']+`">`+objectSummary['tool_name']+`</a>
				</div>
				<div class="added-tool-description">`+objectSummary['tool_description']+`</div>
				</div>
			</div>
			`.replace('\n', '');

			$addedObjectCol.html(objectPreviewHtml);
			$('[data-toggle="tooltip"]').tooltip()
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

				if (analysisObject[objectType].indexOf(objectData) === -1 && objectData != "" && Object.values(objectData).indexOf('') === -1 && analysisObject['dataset'].map(function(x) {return x['dataset_accession']}).indexOf(objectData['dataset_accession']) < 1) {
					analysisObject[objectType].push(objectData);
					self.addObjectPreview(objectData, objectType);
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
					self.addObjectPreview(objectData, objectType);
				}

			}
		})

		return analysisObject;
	},

	// remove dataset
	removeDataset: function(analysisObject) {
		$(document).on('click', '.remove-added-dataset', function(evt) {
			var $addedDatasetCol = $('#added-dataset-col'),
				removedDatasetIdentifier = $(evt.target).parent().parent().attr('id');
			analysisObject['dataset'] = analysisObject['dataset'].filter(function(x){ return(typeof x === 'object' ? x['dataset_accession'] != removedDatasetIdentifier : x != removedDatasetIdentifier) });
			if ($addedDatasetCol.find('.added-dataset').length === 1) {
				$addedDatasetCol.parent().addClass('hidden');
			}
			removedDatasetIdentifier = $(evt.target).parent().parent().remove();
		})

		return analysisObject;
	},

	// preview analysis
	previewAnalysis: function(analysisObject) {

		$('#preview-analysis-button-row button').click(function(evt) {
			analysisObject['analysis'] = {'metadata': {}};

			$('#input-analysis-row').find('input').each(function(i, elem) {
				analysisObject['analysis'][$(elem).attr('id')] = $(elem).val();
			})

			if ($('.tags-input').find('.tag').length > 0) {
				analysisObject['analysis']['metadata']['keywords'] = [];
				$('.tags-input').find('.tag').each(function(i, elem){ analysisObject['analysis']['metadata']['keywords'].push($(elem).attr('data-tag')); });
			}

			$('#metadata-row-wrapper').find('.row').each(function(i, elem){ analysisObject['analysis']['metadata'][$(elem).find('.metadata-term').val()] = $(elem).find('.metadata-value').val() });

			if (analysisObject['dataset'] != [] && analysisObject['tool'] != '' && Object.values(analysisObject['analysis']).indexOf('') === -1) {
				$.ajax({ // get preview html from api
					url: 'http://amp.pharm.mssm.edu/datasets2tools/api/get_analysis_preview',
					data: {
					  'data': JSON.stringify(analysisObject),
					},
					success: function(data) {
						$('#preview-analysis-row').find('.col-12').html(data);
						$('#add-analysis-wrapper').addClass('hidden');
						$('#preview-analysis-wrapper').removeClass('hidden');
						$('[data-toggle="tooltip"]').tooltip();
					}
				})
			}

		})

		return analysisObject;
	},

	// review analysis
	reviewAnalysis: function() {
		$('#review-analysis-button').click(function(evt) {
			$('#add-analysis-wrapper').removeClass('hidden');
			$('#preview-analysis-wrapper').addClass('hidden');
		})
	},

	// submit analysis
	submitAnalysis: function(analysisObject) {
		$('#submit-analysis-button').click(function(evt) {
			alert('Submit function to be added soon.')
		}) 
	},

	// main
	main: function() {
		if (window.location.pathname === '/datasets2tools/upload') {
			var self = this,
				analysisObject = {'dataset': [], 'tool': '', 'analysis': {}};
			self.changeInputMethod();
			analysisObject = self.addObject(analysisObject);
			analysisObject = self.removeDataset(analysisObject);
			analysisObject = self.previewAnalysis(analysisObject);
			analysisObject = self.reviewAnalysis(analysisObject);
			self.submitAnalysis(analysisObject);
		}
	}
};

//////////////////////////////
///// 5. Help //////////////
//////////////////////////////

var help = {

	// main
	main: function() {
		if (window.location.pathname === '/datasets2tools/help') {
			var self = this;
		}
	}

};




///////////////////////////////////
////////// 3. Call ////////////////
///////////////////////////////////

main();
