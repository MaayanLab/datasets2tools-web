############################################################
############################################################
############### Datasets2Tools Web Interface ###############
############################################################
############################################################

#######################################################
########## 1. Setup Python ############################
#######################################################

##############################
##### 1.1 Python Libraries
##############################
import sys, json, os, urllib
import pandas as pd
from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy

##############################
##### 1.2 Custom Libraries
##############################
if os.path.exists('/datasets2tools/flask/scripts'):
	sys.path.append('/datasets2tools/flask/scripts')
else:
	sys.path.append('scripts')
from CannedAnalysisDatabase import CannedAnalysisDatabase

##############################
##### 1.3 Setup App
##############################
# Initialize Flask App
if os.path.exists('/datasets2tools/flask/static'):
	app = Flask(__name__, static_url_path='/datasets2tools/flask/static')
else:
	app = Flask(__name__)


# Read data
connection_file = '../../datasets2tools-database/f1-mysql.dir/conn.json'
if os.path.exists(connection_file):
	with open(connection_file) as openfile:
		connectionDict = json.loads(openfile.read())['phpmyadmin']
	os.environ['DB_USER'] = connectionDict['username']
	os.environ['DB_PASS'] = connectionDict['password']
	os.environ['DB_HOST'] = connectionDict['host']
	os.environ['DB_NAME'] = 'datasets2tools'

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + '@' + os.environ['DB_HOST'] + '/' + os.environ['DB_NAME']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 290
engine = SQLAlchemy(app).engine

#######################################################
########## 2. Platform ################################
#######################################################

##############################
##### 1. Templates
##############################

#########################
### 1. Homepage
#########################

@app.route('/datasets2tools/')
@app.route('/datasets2tools')

def index():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get object count
	object_count = Database.get_object_count()

	# Get featured objects
	featured_objects = Database.get_featured_objects()

	# Get news
	news_list = Database.get_news_list()
	
	# Render template
	return render_template('index.html', object_count=object_count, featured_objects=featured_objects, news_list=news_list)

#########################
### 2. Keyword Search
#########################

@app.route('/datasets2tools/search')

def search():

	# Check if query
	if all([x in request.args.keys() for x in ['object_type', 'keywords']]):

		# Connect to Database
		Database = CannedAnalysisDatabase(engine)

		# Get query arguments
		object_type = request.args.get('object_type', 'None', type=str)
		keywords_list = request.args.get('keywords', 'None', type=str).split(',')
		size = request.args.get('size', 10, type=int)

		# Get IDs
		ids = Database.keyword_search(object_type, keywords_list, size)

		# Get result table
		table_html = Database.table_from_ids(ids, object_type)

	else:

		# Return empty string
		table_html = ''

	# Render template
	return render_template('search.html', table_html=table_html)

#########################
### 3. Advanced Search
#########################

@app.route('/datasets2tools/advanced_search')

def advanced_search():
	
	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Check if query exists
	if all([x in request.args.keys() for x in ['object_type', 'query']]):

		# Get query arguments
		query = request.args.get('query')
		object_type = request.args.get('object_type')

		# Get IDs
		ids = Database.advanced_search(query, object_type)

		# Get result table
		table_html = Database.table_from_ids(ids, object_type)
		
		# Render template
		return render_template('advanced_search_results.html', table_html=table_html)

	else:

		# Get search terms
		available_search_terms = Database.get_available_search_terms()

		# Render template
		return render_template('advanced_search.html', available_search_terms=available_search_terms, number_of_rows=10)

#########################
### 4. Upload
#########################

@app.route('/datasets2tools/upload')

def upload():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get stored data
	stored_data = Database.get_stored_data()
	
	# Render template
	return render_template('upload.html', stored_data=stored_data)

#########################
### 5. Help
#########################

@app.route('/datasets2tools/help')

def help():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get available search terms
	available_search_terms = Database.get_available_search_terms(pretty=False)
	
	# Render template
	return render_template('help.html', available_search_terms=available_search_terms)

#########################
### 6. Collections
#########################

@app.route('/datasets2tools/collections')

def collections():
	
	# Render template
	return render_template('collections.html')

#########################
### 7. Metadata Explorer
#########################

@app.route('/datasets2tools/metadata')

def metadata():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)
	
	# Render template
	return render_template('metadata.html')

##############################
##### 2. Search APIs
##############################

#########################
### 1. Keyword Search
#########################

@app.route('/datasets2tools/api/keyword_search')

def keyword_search_api():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get query arguments
	object_type = request.args.get('object_type', 'None', type=str)
	keywords_list = request.args.get('keywords', 'None', type=str).split(',')
	size = request.args.get('size', 10, type=int)

	# Get IDs
	ids = Database.keyword_search(object_type, keywords_list, size)

	# Get summary JSON
	summary_json = Database.get_annotations(ids, object_type, output='json')
	
	# Return summary JSON
	
	# Return summary JSON
	return summary_json

#########################
### 2. Advanced Search
#########################

@app.route('/datasets2tools/api/advanced_search')

def advanced_search_api():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get query arguments
	object_type = request.args.get('object_type', 'None', type=str)
	query = request.args.get('query', 'None', type=str)

	# Get IDs
	ids = Database.advanced_search(query, object_type)

	# Get summary JSON
	summary_json = Database.get_annotations(ids, object_type, output='json')
	
	# Return summary JSON
	return summary_json

#########################
### 3. Object APIs
#########################

##########
# Analysis
##########

@app.route('/datasets2tools/api/analysis')

def analysis_api():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get IDs
	ids = Database.analysis_api(request.args.to_dict())

	# Get summary JSON
	summary_json = Database.get_annotations(ids, 'analysis', output='json')
	
	# Return summary JSON
	return summary_json

##########
# Dataset
##########

@app.route('/datasets2tools/api/dataset')

def dataset_api():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get IDs
	ids = Database.dataset_api(request.args)

	# Get summary JSON
	summary_json = Database.get_annotations(ids, 'dataset', output='json')
	
	# Return summary JSON
	return summary_json

##########
# Tool
##########

@app.route('/datasets2tools/api/tool')

def tool_api():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get IDs
	ids = Database.tool_api(request.args)

	# Get summary JSON
	summary_json = Database.get_annotations(ids, 'tool', output='json')
	
	# Return summary JSON
	return summary_json

#########################
### 4. Extension APIs
#########################

@app.route('/datasets2tools/api/chrome_extension')

def chrome_extension_api():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get interface JSON
	interface_json = Database.chrome_extension_api(request.args.to_dict())

	# Return interface JSON
	return interface_json

#########################
### 5. Explorer API
#########################

@app.route('/datasets2tools/api/metadata_explorer')

def metadata_explorer():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get query and query type
	query = request.args.get('query', '{}', type=str)
	query_type = request.args.get('query_type', 'd3', type=str)

	# Check query type
	if query_type == 'd3':

		# Get D3 query
		metadata_explorer_json = json.dumps({'d3': Database.get_d3_dict(query, 500), 'select': Database.get_select_dict(query, 1000)})
	elif query_type == 'results':

		# Get results query
		metadata_explorer_json = Database.get_explorer_results(query, 25)

	# Return JSON
	return metadata_explorer_json

#########################
### 6. ARCHS4 API
#########################

@app.route('/datasets2tools/api/archs4')

def archs4_api():

	# Get query
	query = request.args.get('q', '', type=str)

	# Return query
	return send_from_directory('static/clustergrammer', query+'.json')

##############################
##### 3. Upload API
##############################

#########################
### 1. Upload Analysis
#########################

@app.route('/datasets2tools/api/upload', methods=['POST'])

def upload_api():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get canned analysis list
	canned_analysis_list = request.get_json()['canned_analyses']
	print 'Loading Canned Analyses...'
	status = Database.upload_canned_analysis(canned_analysis_list)
	print status
	return status

#########################
### 2. Upload Dataset
#########################

@app.route('/datasets2tools/api/upload_dataset', methods=['POST'])

def upload_dataset():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get dataset list
	dataset_list = request.get_json()['datasets']

	# Return dataset list
	return 'dataset_list'

#########################
### 3. Upload Tool
#########################

@app.route('/datasets2tools/api/upload_tool', methods=['POST'])

def upload_tool():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)
	canned_analysis_list = request.get_json()['canned_analyses']
	print 'Loading Canned Analyses...'
	status = Database.upload_canned_analysis(canned_analysis_list)
	print status
	return status

#########################
### 4. Analysis Preview
#########################

@app.route('/datasets2tools/api/get_analysis_preview')

def analysis_preview_api():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Get analysis preview
	analysis_preview = Database.get_analysis_preview(json.loads(request.args.get('data')))

	# Return analysis preview
	return analysis_preview

#########################
### 5. Manual Upload
#########################

@app.route('/datasets2tools/api/manual_upload')

def manual_upload():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)
	upload_result_json = Database.manual_upload(request.args.get('data'))
	return upload_result_json

##############################
##### 4. Miscellaneous
##############################

#########################
### 1. Search Terms
#########################

# Gets list of terms which are to be used in the advanced search form,
# appearing in the selection menu.

@app.route('/datasets2tools/advanced_search_terms')

def advanced_search_terms():

	# Connect to Database
	Database = CannedAnalysisDatabase(engine)

	# Return search terms
	return Database.get_term_names(request.args.get('object_type'))

#########################
### 2. ARCHS4
#########################

@app.route('/datasets2tools/archs4')

def archs4():
	
	# Render template
	return render_template('archs4.html')


#######################################################
########## 3. Run Flask App ###########################
#######################################################
# Run App
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')