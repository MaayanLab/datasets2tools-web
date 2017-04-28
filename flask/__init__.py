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
sys.path.append('scripts')
from CannedAnalysisDatabase import CannedAnalysisDatabase

##############################
##### 1.3 Setup App
##############################
# Initialize Flask App
app = Flask(__name__)

# Read data
with open('../../datasets2tools-database/f1-mysql.dir/conn.json') as openfile:
	connectionDict = json.loads(openfile.read())['phpmyadmin']
os.environ['DB_USER'] = connectionDict['username']
os.environ['DB_PASS'] = connectionDict['password']
os.environ['DB_HOST'] = connectionDict['host']
os.environ['DB_NAME'] = 'datasets2tools2'

# Initialize database
uriString = 'mysql://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + '@' + os.environ['DB_HOST'] + '/' + os.environ['DB_NAME']
app.config['SQLALCHEMY_DATABASE_URI'] = uriString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = SQLAlchemy(app).engine

#######################################################
########## 2. Setup Web Page ##########################
#######################################################

##############################
##### 2.1 Homepage
##############################

### 2.1.1 Main
@app.route('/datasets2tools')
def index():
	return render_template('index.html')

@app.route('/datasets2tools/search')
def search():
	return render_template('search.html')

@app.route('/datasets2tools/advanced_search')
def advanced_search():
	Database = CannedAnalysisDatabase(engine)
	if 'query' in request.args.keys():
		query = request.args.get('query')
		object_type = query.split('object IS ')[-1].split(')')[0]
		try:
			ids = Database.advanced_search(request.args.get('query'))
			if len(ids) > 0:
				if object_type == 'analyses':
					result_html = Database.make_canned_analysis_table(ids)
				elif object_type == 'datasets':
					result_html = Database.make_dataset_table(ids)
				elif object_type == 'tools':
					result_html = Database.make_tool_table(ids)
			else:
				result_html = 'Sorry, no search results found for specified query.'
		except:
			result_html = 'Sorry, there was an error.'
		return render_template('advanced_search_results.html', result_html=result_html)
	else:
		return render_template('advanced_search.html')

@app.route('/datasets2tools/advanced_search_terms')
def advanced_search_terms():
	Database = CannedAnalysisDatabase(engine)
	return Database.get_term_names(request.args.get('object_type'))

@app.route('/datasets2tools/keyword_search')
def keyword_search():
	Database = CannedAnalysisDatabase(engine)
	obj = request.args.get('obj', 'None', type=str)
	keywords = request.args.get('keywords', 'None', type=str).split(',')
	if obj == 'analyses':
		ids = Database.search_analyses_by_keyword(keywords)
		table_html = Database.make_canned_analysis_table(ids)
		return str(table_html)
	elif obj == 'datasets':
		ids = Database.search_datasets_by_keyword(keywords)
		table_html = Database.make_dataset_table(ids)
		return str(table_html)
	elif obj == 'tools':
		ids = Database.search_tools_by_keyword(keywords)
		table_html = Database.make_tool_table(ids)
		return str(table_html)

@app.route('/datasets2tools/manual_upload')
def manual_upload():
	Database = CannedAnalysisDatabase(engine)
	stored_data = Database.get_stored_data()
	return render_template('manual_upload.html', stored_data=stored_data)

@app.route('/datasets2tools/help')
def help():
	return render_template('help.html')

@app.route('/datasets2tools/object_search')
def object_search():
	Database = CannedAnalysisDatabase(engine)
	request_dict = dict(request.args)
	object_type = request_dict.pop('object_type')[0]
	column = request_dict.keys()[0]
	value = request_dict[column][0]
	print object_type, column, value
	return Database.object_search(object_type, column, value)

@app.route('/datasets2tools/stored_terms')
def stored_terms():
	Database = CannedAnalysisDatabase(engine)
	stored_data = Database.get_stored_data()
	return '\n'.join(stored_data['term']['term_name'])


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