import requests, json, sys
import pandas as pd
import time

############################################################
############################################################
############### 1. Canned Analysis #########################
############################################################
############################################################

class CannedAnalysis:
    
#######################################################
########## 1. Initialize ##############################
#######################################################

    def __init__(self, cannedAnalysisDict, engine):
        self.data = cannedAnalysisDict
        self.engine = engine
        self.fields = ['canned_analysis_title', 'canned_analysis_description', 'canned_analysis_url', 'canned_analysis_preview_url', 'metadata']
        if not all(x in self.data.keys() for x in self.fields):
            raise ValueError('Missing fields: '+', '.join(list(set(self.fields)-set(self.data.keys())))+'.')
        try:
            self.data['metadata'] = json.loads(self.data['metadata'])
        except:
            print self.data['metadata']
            raise ValueError('Metadata not JSON.')
            
#######################################################
########## 2. Foreign Keys ############################
#######################################################

    def get_tool_fk(self):
        try:
            self.data['tool_fk'] = pd.read_sql_query('SELECT id FROM tool WHERE LCASE(tool_name) = "'+self.data['tool_name'].lower()+'"', self.engine)['id'][0]
        except:
            raise ValueError('Tool '+self.data['tool_name']+' not found.')
        
    def get_dataset_fk(self):
        if type(self.data['dataset_accession']) == list:
            if len(self.data['dataset_accession']) == 1:
                self.data['dataset_accession'] = self.data['dataset_accession'][0]
            else:
                raise ValueError('Multiple datasets not currently supported.')
        try:
            self.data['dataset_fk'] = pd.read_sql_query('SELECT id FROM dataset WHERE LCASE(dataset_accession) = "'+self.data['dataset_accession'].lower()+'"', self.engine)['id'][0]
        except:
            raise ValueError('Dataset '+self.data['dataset_accession']+' not found.')
            
    def get_term_fk(self, term_name):
        try:
            term_fk = pd.read_sql_query('SELECT id FROM term WHERE LCASE(term_name) = "'+term_name.lower()+'"', self.engine)['id'][0]
        except:
            self.connection.execute('INSERT INTO term (`term_name`, `term_description`) VALUES ("{term_name}", "")'.format(**locals()))
            term_fk = self.connection.execute('SELECT LAST_INSERT_ID();').fetchall()[0][0]
        return term_fk
               
#######################################################
########## 3. Upload ##################################
#######################################################

    def upload_analysis(self):
        print 'Uploading analysis...'
        self.get_tool_fk()
        self.get_dataset_fk()
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        try:
            self.connection.execute('''INSERT INTO canned_analysis (`canned_analysis_title`, `canned_analysis_description`, `canned_analysis_url`, `canned_analysis_preview_url`, `dataset_fk`, `tool_fk`) VALUES ("{canned_analysis_title}", "{canned_analysis_description}", "{canned_analysis_url}", "{canned_analysis_preview_url}", "{dataset_fk}", "{tool_fk}")'''.format(**self.data).replace('%', '%%'))
            self.canned_analysis_fk = self.connection.execute('SELECT LAST_INSERT_ID();').fetchall()[0][0]
            self.transaction.commit()
        except:
            self.transaction.rollback()
            self.error = sys.exc_info()[0]
            raise
        
    def upload_metadata(self):
        print 'Uploading analysis metadata...'
        metadataDataframe = pd.DataFrame.from_dict(self.data['metadata'], orient='index').reset_index().rename(columns={'index': 'term_name', 0: 'value'})
        metadataDataframe['term_fk'] = [self.get_term_fk(x) for x in metadataDataframe['term_name']]
        metadataDataframe['canned_analysis_fk'] = self.canned_analysis_fk
        metadataDataframe.drop('term_name', axis=1, inplace=True)
        metadataDataframe.to_sql('canned_analysis_metadata', self.connection, index=False, if_exists='append')
    
    def upload(self):
        # try:
        self.upload_analysis()
        self.upload_metadata()
        time.sleep(0.3)
        return self.canned_analysis_fk
        # except:
            # pass

############################################################
############################################################
############### 2. Dataset #################################
############################################################
############################################################

class Dataset:
    
#######################################################
########## 1. Initialize ##############################
#######################################################

    def __init__(self, datasetDict, engine):
        self.data = datasetDict
        self.engine = engine
        self.fields = ['repository_fk', 'dataset_accession', 'dataset_landing_url', 'dataset_title', 'dataset_description']
        if not all(x in self.data.keys() for x in self.fields):
            raise ValueError('Missing fields: '+', '.join(list(set(self.fields)-set(self.data.keys())))+'.')
                   
#######################################################
########## 2. Upload ##################################
#######################################################

    def upload(self):
        columns = self.data.keys()
        values = self.data.values()
        'INSERT INTO dataset () VALUES ()'
 
############################################################
############################################################
############### 3. Dataset #################################
############################################################
############################################################

class Tool:
    
#######################################################
########## 1. Initialize ##############################
#######################################################

    def __init__(self, toolDict, engine):
        self.data = cannedAnalysisDict
        self.engine = engine
        self.fields = ['tool_name', 'tool_icon_url', 'tool_homepage_url', 'tool_description', 'tool_screenshot_url3']
        if not all(x in self.data.keys() for x in self.fields):
            raise ValueError('Missing fields: '+', '.join(list(set(self.fields)-set(self.data.keys())))+'.')
                   
#######################################################
########## 2. Upload ##################################
#######################################################
 
    def upload(self):
        pass
 
        
