import requests, json
import pandas as pd
import time

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
        self.connection.execute('''INSERT INTO canned_analysis (`canned_analysis_title`, `canned_analysis_description`, `canned_analysis_url`, `canned_analysis_preview_url`, `dataset_fk`, `tool_fk`) VALUES ("{canned_analysis_title}", "{canned_analysis_description}", "{canned_analysis_url}", "{canned_analysis_preview_url}", "{dataset_fk}", "{tool_fk}")'''.format(**self.data).replace('%', '%%'))
        self.canned_analysis_fk = self.connection.execute('SELECT LAST_INSERT_ID();').fetchall()[0][0]
        
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
        self.transaction.commit()
        time.sleep(0.3)
        # except:
            # pass
        
