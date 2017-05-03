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
};

///////////////////////////////////
////////// 3. Call ////////////////
///////////////////////////////////

main();
