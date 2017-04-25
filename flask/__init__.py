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
import sys, json, os
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

@app.route('/datasets2tools/help')
def help():
	return render_template('help.html')

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






#######################################################
########## 3. Run Flask App ###########################
#######################################################
# Run App
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')