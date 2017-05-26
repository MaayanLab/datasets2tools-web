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
from flask import Flask, render_template, request
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
	Database = CannedAnalysisDatabase(engine)
	object_count = Database.get_object_count()
	featured_objects = Database.get_featured_objects()
	news_list = Database.get_news_list()
	return render_template('index.html', object_count=object_count, featured_objects=featured_objects, news_list=news_list)

#########################
### 2. Keyword Search
#########################

@app.route('/datasets2tools/search')
def search():
	# query
	if all([x in request.args.keys() for x in ['object_type', 'keywords']]):

		# setup
		Database = CannedAnalysisDatabase(engine)

		# get args
		object_type = request.args.get('object_type', 'None', type=str)
		keywords_list = request.args.get('keywords', 'None', type=str).split(',')
		size = request.args.get('size', 10, type=int)

		# get results
		ids = Database.keyword_search(object_type, keywords_list, size)
		table_html = Database.table_from_ids(ids, object_type)
	else:
		table_html = ''

	return render_template('search.html', table_html=table_html)

#########################
### 3. Advanced Search
#########################

@app.route('/datasets2tools/advanced_search')
def advanced_search():
	
	# setup
	Database = CannedAnalysisDatabase(engine)

	# query
	if all([x in request.args.keys() for x in ['object_type', 'query']]):

		# get args
		query = request.args.get('query')
		object_type = request.args.get('object_type')

		# get table
		ids = Database.advanced_search(query, object_type)
		table_html = Database.table_from_ids(ids, object_type)
		return render_template('advanced_search_results.html', table_html=table_html)
	else:
		# get search terms
		available_search_terms = Database.get_available_search_terms()

		# default
		return render_template('advanced_search.html', available_search_terms=available_search_terms, number_of_rows=10)

#########################
### 4. Upload
#########################

@app.route('/datasets2tools/upload')
def upload():
	Database = CannedAnalysisDatabase(engine)
	stored_data = Database.get_stored_data()
	return render_template('upload.html', stored_data=stored_data)

#########################
### 5. Help
#########################

@app.route('/datasets2tools/help')
def help():
	Database = CannedAnalysisDatabase(engine)
	available_search_terms = Database.get_available_search_terms(pretty=False)
	return render_template('help.html', available_search_terms=available_search_terms)

#########################
### 6. Collections
#########################

@app.route('/datasets2tools/collections')
def collections():
	return render_template('collections.html')

#########################
### 7. Metadata Explorer
#########################

@app.route('/datasets2tools/metadata')
def metadata():
	Database = CannedAnalysisDatabase(engine)
	return render_template('metadata.html')

##############################
##### 2. Search APIs
##############################

#########################
### 1. Keyword Search
#########################

@app.route('/datasets2tools/api/keyword_search')
def keyword_search_api():
	# setup
	Database = CannedAnalysisDatabase(engine)

	# get args
	object_type = request.args.get('object_type', 'None', type=str)
	keywords_list = request.args.get('keywords', 'None', type=str).split(',')
	size = request.args.get('size', 10, type=int)

	# get results
	ids = Database.keyword_search(object_type, keywords_list, size)
	summary_json = Database.get_annotations(ids, object_type, output='json')
	return summary_json

#########################
### 2. Advanced Search
#########################

@app.route('/datasets2tools/api/advanced_search')
def advanced_search_api():
	#setup 
	Database = CannedAnalysisDatabase(engine)

	# get args
	object_type = request.args.get('object_type', 'None', type=str)
	query = request.args.get('query', 'None', type=str)

	# get results
	ids = Database.advanced_search(query, object_type)
	summary_json = Database.get_annotations(ids, object_type, output='json')
	return summary_json

#########################
### 3. Object APIs
#########################

@app.route('/datasets2tools/api/analysis')
def analysis_api():
	Database = CannedAnalysisDatabase(engine)
	ids = Database.analysis_api(request.args.to_dict())
	print ids
	summary_json = Database.get_annotations(ids, 'analysis', output='json')
	return summary_json

@app.route('/datasets2tools/api/dataset')
def dataset_api():
	Database = CannedAnalysisDatabase(engine)
	ids = Database.dataset_api(request.args)
	summary_json = Database.get_annotations(ids, 'dataset', output='json')
	return summary_json

@app.route('/datasets2tools/api/tool')
def tool_api():
	Database = CannedAnalysisDatabase(engine)
	ids = Database.tool_api(request.args)
	summary_json = Database.get_annotations(ids, 'tool', output='json')
	return summary_json

#########################
### 4. Extension APIs
#########################

@app.route('/datasets2tools/api/chrome_extension')
def chrome_extension_api():
	Database = CannedAnalysisDatabase(engine)
	interface_json = Database.chrome_extension_api(request.args.to_dict())
	return interface_json

#########################
### 5. Explorer API
#########################

@app.route('/datasets2tools/api/metadata_explorer')
def metadata_explorer():
	Database = CannedAnalysisDatabase(engine)
	query = request.args.get('query', '{}', type=str)
	query_type = request.args.get('query_type', 'd3', type=str)
	if query_type == 'd3':
		metadata_explorer_json = json.dumps({'d3': Database.get_d3_dict(query, 500), 'select': Database.get_select_dict(query, 1000)})
	elif query_type == 'results':
		metadata_explorer_json = Database.get_explorer_results(query, 50)
	return metadata_explorer_json


##############################
##### 3. Upload API
##############################

#########################
### 1. Upload
#########################

@app.route('/datasets2tools/api/upload', methods=['POST'])
def upload_api():
	Database = CannedAnalysisDatabase(engine)
	canned_analysis_list = request.get_json()['canned_analyses']
	print 'Loading Canned Analyses...'
	status = Database.upload_canned_analysis(canned_analysis_list)
	print status
	return status

##############################
##### 4. Miscellaneous
##############################

#########################
### 1. Analysis Preview
#########################

@app.route('/datasets2tools/api/get_analysis_preview')
def analysis_preview_api():
	Database = CannedAnalysisDatabase(engine)
	analysis_preview = Database.get_analysis_preview(request.args.get('data'))
	return analysis_preview

#########################
### 2. Search Terms
#########################

# Gets list of terms which are to be used in the advanced search form,
# appearing in the selection menu.

@app.route('/datasets2tools/advanced_search_terms')
def advanced_search_terms():
	Database = CannedAnalysisDatabase(engine)
	return Database.get_term_names(request.args.get('object_type'))

#########################
### 3. Object Search
#########################

# No idea whatsoever.

@app.route('/datasets2tools/object_search')
def object_search():
	Database = CannedAnalysisDatabase(engine)
	request_dict = dict(request.args)
	object_type = request_dict.pop('object_type')[0]
	column = request_dict.keys()[0]
	value = request_dict[column][0]
	print object_type, column, value
	return Database.object_search(object_type, column, value)

#########################
### 4. Stored Terms
#########################

# No idea whatsoever.

@app.route('/datasets2tools/stored_terms')
def stored_terms():
	Database = CannedAnalysisDatabase(engine)
	stored_data = Database.get_stored_data()
	return '\n'.join(stored_data['term']['term_name'])

#########################
### 5. Prepare CA Table
#########################

# No idea whatsoever.

@app.route('/datasets2tools/prepare_canned_analysis_table')
def prepare_canned_analysis_table():
	Database = CannedAnalysisDatabase(engine)
	canned_analysis_json = urllib.unquote(request.args.get('canned_analysis_json'))
	canned_analysis_table = Database.prepare_canned_analysis_table(canned_analysis_json)
	return canned_analysis_table


#######################################################
########## 3. Run Flask App ###########################
#######################################################
# Run App
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')