import json
import pandas as pd

class CannedAnalysisTable:
    
    ##### 1. Initialize
    def __init__(self, canned_analysis_dataframe, engine):

        # Initialize database connection
        self.engine = engine
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        
        # Initialize data dict
        self.data_dict = {}

        # Read data
        self.canned_analysis_dataframe = canned_analysis_dataframe.copy()
    
    ##### 2. Get Data
    def get_data(self, data_type):

        # Get dataset dict
        if data_type == 'dataset':
            self.data_dict['dataset'] = pd.read_sql('SELECT id, dataset_accession FROM dataset', self.connection, index_col='dataset_accession').to_dict()['id']

        # Get tool dict
        elif data_type == 'tool':
            self.data_dict['tool'] = pd.read_sql('SELECT id, LCASE(tool_name) AS tool_name FROM tool', self.connection, index_col='tool_name').to_dict()['id']
    
        # Get term dict
        elif data_type == 'term':
            self.data_dict['term'] = pd.read_sql('SELECT id, LCASE(REPLACE(term_name, " ", "_")) AS term_name FROM term', self.connection, index_col='term_name').to_dict()['id']
    
    ##### 3. Get Foreign keys
    def get_foreign_keys(self):

        # Get data
        self.get_data('dataset')
        self.get_data('tool')
        
        # Add missing tools
        self.missing_tools = set(self.canned_analysis_dataframe['tool_name']) - set(self.data_dict['tool'].keys())
        if len(self.missing_tools) > 0:
            self.upload_tools()
            self.get_data('tool')
        
        # Add missing datasets
        self.missing_datasets = set(self.canned_analysis_dataframe['dataset_accession']) - set(self.data_dict['dataset'].keys())
        if len(self.missing_datasets) > 0:
            self.upload_datasets()
            self.get_data('dataset')
            
        # Get foreign keys
        self.canned_analysis_dataframe['dataset_fk'] = [self.data_dict['dataset'][x] for x in self.canned_analysis_dataframe['dataset_accession']]
        self.canned_analysis_dataframe['tool_fk'] = [self.data_dict['tool'][x] for x in self.canned_analysis_dataframe['tool_name']]
        
        # Remove columns
        self.canned_analysis_dataframe.drop(['dataset_accession', 'tool_name'], axis=1, inplace=True)
              
    ##### 4. Upload Datasets
    def upload_datasets(self):
        
        # Print
        print 'Uploading datasets...'
        
        # Get dataset accessions
        dataset_dataframe = pd.DataFrame.from_dict({'dataset_accession': self.missing_datasets}, orient='index').T
        
        # Upload
        dataset_dataframe.to_sql('dataset', self.connection, if_exists='append', index=False)
              
    ##### 5. Upload Tools
    def upload_tools(self):
        
        # Print
        print 'Uploading tools...'
        
        # Get dataset accessions
        tool_dataframe = pd.DataFrame.from_dict({'tool_name': self.missing_tools}, orient='index').T
                
        # Upload
        tool_dataframe.to_sql('tool', self.connection, if_exists='append', index=False)
    
    ##### 6. Upload Analyses
    def upload_analyses(self):
        
        # Print
        print 'Uploading analyses...'
        
        # Get metadata dict
        self.metadata_dict = {canned_analysis_url: json.loads(metadata) for canned_analysis_url, metadata in self.canned_analysis_dataframe[['canned_analysis_url', 'metadata']].as_matrix()}

        # Drop column
        self.canned_analysis_dataframe.drop('metadata', axis=1, inplace=True)

        # Upload
        self.canned_analysis_dataframe.to_sql('canned_analysis', self.connection, if_exists='append', index=False)
        
        # Commit
        self.transaction.commit()

    ##### 7. Upload Metadata
    def upload_metadata(self):
        
        # Get canned analysis URLs
        canned_analysis_url_string = '", "'.join(self.canned_analysis_dataframe['canned_analysis_url'])
        
        # Get canned analysis dataframe
        self.canned_analysis_dataframe = pd.read_sql('SELECT * FROM canned_analysis WHERE canned_analysis_url IN ("{canned_analysis_url_string}")'.format(**locals()), self.engine, index_col='id')

        # Fix date to string
        self.canned_analysis_dataframe['date'] = ['{:%Y-%m-%d}'.format(x) for x in self.canned_analysis_dataframe['date']]
        
        # Get FK dict
        canned_analysis_fk_dict = {rowData['canned_analysis_url']: index for index, rowData in self.canned_analysis_dataframe.iterrows()}
        
        # Get terms
        self.get_data('term')
        
        # Add missing terms
        self.missing_terms = set(set([term_name.lower().replace(' ', '_') for canned_analysis_url in self.metadata_dict.keys() for term_name in self.metadata_dict[canned_analysis_url].keys()])) - set(self.data_dict['term'])
        if len(self.missing_terms) > 0:
            self.upload_terms()
            self.get_data('term')
            
        # Initialize list
        canned_analysis_metadata_list = []
            
        # Loop through canned analysis urls
        for canned_analysis_url in canned_analysis_fk_dict.keys()[:5]:
            
            # Get metadata dict
            canned_analysis_metadata_dict = self.metadata_dict[canned_analysis_url]
            
            # Get canned analysis FK
            canned_analysis_fk = canned_analysis_fk_dict[canned_analysis_url]
            
            # Loop through dict
            for term_name, value in canned_analysis_metadata_dict.iteritems():
            
                # Add metadata to list
                canned_analysis_metadata_list.append({'canned_analysis_fk': canned_analysis_fk,
                                                      'term_fk': self.data_dict['term'][term_name.lower().replace(' ', '_')],
                                                      'value': value})
                
            # Convert to dataframe
            self.canned_analysis_metadata_dataframe = pd.DataFrame(canned_analysis_metadata_list)
            
            # Upload
            self.canned_analysis_metadata_dataframe.to_sql('canned_analysis_metadata', self.engine, if_exists='append', index=False)
            
    ##### 8. Upload Terms
    def upload_terms(self):
        
        # Print
        print 'Uploading terms...'
        
        # Get dataset accessions
        tool_dataframe = pd.DataFrame.from_dict({'term_name': self.missing_terms}, orient='index').T
                
        # Upload
        tool_dataframe.to_sql('term', self.connection, if_exists='append', index=False)
        
    ##### 9. Upload Data
    def upload(self):
        
        # Get foreign keys
        self.get_foreign_keys()
        
        # Upload analyses
        self.upload_analyses()
        
        # Upload metadata
        self.upload_metadata()