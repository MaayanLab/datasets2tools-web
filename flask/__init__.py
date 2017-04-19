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
def main():
	return render_template('index.html')

@app.route('/datasets2tools/cannedanalyses')
def cannedanalyses():
	cannedAnalysisData = '''{"tools": {"1": {"tool_icon_url": "http://amp.pharm.mssm.edu/Enrichr/images/enrichr-icon.png", "tool_homepage_url": "http://amp.pharm.mssm.edu/Enrichr", "doi": "10.1186/1471-2105-14-128", "tool_name": "Enrichr", "tool_description": "An intuitive web-based gene list enrichment analysis tool with 90 libraries"}, "11": {"tool_icon_url": "http://amp.pharm.mssm.edu/L1000CDS2/CSS/images/sigine.png", "tool_homepage_url": "http://amp.pharm.mssm.edu/L1000CDS2", "doi": null, "tool_name": "L1000CDS2", "tool_description": "An ultra-fast LINCS L1000 Characteristic Direction signature search engine"}, "13": {"tool_icon_url": "http://amp.pharm.mssm.edu/g2e/static/image/targetapp/paea.png", "tool_homepage_url": "http://amp.pharm.mssm.edu/PAEA", "doi": "10.1109/BIBM.2015.7359689", "tool_name": "PAEA", "tool_description": "Enrichment analysis tool implementing the principal angle method"}}, "canned_analyses": {"GDS5621": {"1": {"85504": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jhpc"}, "85505": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jhpd"}, "85506": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jhpe"}, "85507": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jhph"}, "85508": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jhpi"}, "85509": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jhpj"}, "85510": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jwud"}, "85511": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jwue"}, "85512": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jwuf"}, "85513": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=rjfo"}, "85514": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=rjfp"}, "85515": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=rjfq"}, "85516": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=rjft"}, "85517": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=rjfu"}, "85518": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=rjfv"}, "85519": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=ty15"}, "85520": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=ty16"}, "85521": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=ty17"}, "85522": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=ty1d"}, "85523": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=ty1e"}, "85524": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=ty1f"}, "85525": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j430"}, "85526": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j431"}, "85527": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j432"}, "86298": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=k0kn"}, "86299": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=k0ko"}, "86300": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=k0kq"}, "85495": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j42r"}, "85496": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j42s"}, "85497": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j42t"}, "85498": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j886"}, "85499": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j887"}, "85500": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=j888"}, "85501": {"cutoff": "500.0", "direction": "1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jan9"}, "85502": {"cutoff": "500.0", "direction": "-1.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 most underexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=jana"}, "85503": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset=janb"}}, "11": {"87048": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/58207e0f4760621c0177edff"}, "85930": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/57fe73614760621c0177e21d"}, "85931": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/580154114760621c0177e2dd"}, "85932": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/58065ac04760621c0177e473"}, "85933": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/580a37d24760621c0177e6ed"}, "85934": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/580a38744760621c0177e6ef"}, "85935": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/581a0b234760621c0177ed15"}, "85936": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/5857cf27e467bea600f5bd10"}, "85937": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/5857cf90e467bea600f5bd12"}, "85938": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/58653ab1e467bea600f74a6c"}, "85939": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/58653d9de467bea600f74a70"}, "85940": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Signature search of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/L1000CDS2/#/result/57fe788c4760621c0177e21f"}}, "13": {"86155": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=1746695"}, "86156": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=1752074"}, "86157": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=1755209"}, "86158": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=1764356"}, "86159": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=1764361"}, "86160": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=1783978"}, "86161": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=2139849"}, "86162": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=2139854"}, "86163": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=2252078"}, "86164": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=2252086"}, "86165": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=1746704"}, "87284": {"cutoff": "500.0", "direction": "0.0", "diff_exp_method": "chdir", "description": "Principal angle enrichment analysis of the top 500 combined underexpressed and overexpressed genes, chdir diff_exp_method", "canned_analysis_url": "http://amp.pharm.mssm.edu/PAEA?id=1788812"}}}}}'''
	return render_template('cannedanalyses.html', cannedAnalysisData=cannedAnalysisData)

@app.route('/datasets2tools/search.html')
def search():
	return render_template('search.html')

@app.route('/datasets2tools/explore.html')
def explore():
	return render_template('explore.html')

@app.route('/datasets2tools/test.html')
def test():
	return render_template('test.html')

@app.route('/datasets2tools/about.html')
def about():
	return render_template('about.html')

@app.route('/datasets2tools/upload.html')
def upload():
	return render_template('upload.html')

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

@app.route('/datasets2tools/keyword_tree')
def keyword_tree():
	Database = CannedAnalysisDatabase(engine)
	keyword_dict = Database.get_keyword_json()
	return json.dumps(keyword_dict)

@app.route('/datasets2tools/flare.json')
def flare():
	with open('static/flare.json', 'r') as openfile:
		return openfile.read()





#######################################################
########## 3. Run Flask App ###########################
#######################################################
# Run App
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')