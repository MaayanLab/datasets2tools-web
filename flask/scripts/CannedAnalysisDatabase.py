import pandas as pd
pd.set_option('max.colwidth', -1)

class CannedAnalysisDatabase:
    
    def __init__(self, engine):
        self.engine = engine
# 
    # def fetch_tables(self):
        # self.tool = pd.read_sql_query('SELECT * FROM tool', self.engine, index_col='id')
        # self.dataset = pd.read_sql_query('SELECT * FROM dataset', self.engine, index_col='id')
        # self.repository = pd.read_sql_query('SELECT * FROM repository', self.engine, index_col='id')
        # self.term = pd.read_sql_query('SELECT * FROM term', self.engine, index_col='id')
        # self.canned_analysis = pd.read_sql_query('SELECT * FROM canned_analysis', self.engine, index_col='id')
        # self.canned_analysis_metadata = pd.read_sql_query('SELECT * FROM canned_analysis_metadata', self.engine, index_col='id')
        
    def search_analyses_by_keyword(self, keywords):
        sorted_search_results = pd.read_sql_query('SELECT canned_analysis_fk, count(canned_analysis_fk) as count FROM canned_analysis_metadata WHERE value IN ("' + '", "'.join(keywords) + '") GROUP BY canned_analysis_fk ORDER BY count DESC', self.engine)
        ids = sorted_search_results['canned_analysis_fk'].tolist()
        return ids

    def make_canned_analysis_table(self, ids, limit=25):
        ids = ids[:limit]
        canned_analyses = pd.read_sql_query('SELECT ca.id as id, tool_name, tool_icon_url, tool_homepage_url, tool_description, repository_name, repository_homepage_url, repository_icon_url, repository_description, dataset_description, dataset_title, dataset_landing_url, dataset_accession, canned_analysis_url FROM canned_analysis ca LEFT JOIN dataset d ON d.id=ca.dataset_fk LEFT JOIN tool t ON t.id=ca.tool_fk LEFT JOIN repository r ON r.id=d.repository_fk WHERE ca.id IN ('+', '.join([str(x) for x in ids])+')', self.engine, index_col='id')
        metadata = pd.read_sql_query('SELECT canned_analysis_fk, term_name, value FROM canned_analysis_metadata cam LEFT JOIN term t on t.id = cam.term_fk WHERE cam.canned_analysis_fk IN ('+', '.join([str(x) for x in ids])+')', self.engine)
        result_list = []
        for index, rowData in canned_analyses.iterrows():
            tool_html = '<a href="'+rowData['tool_homepage_url']+'"><img class="tool-icon" src="'+rowData['tool_icon_url']+'"></a>'
            dataset_html = '<a class="dataset-cell" data-animation="false" data-toggle="tooltip" data-placement="bottom" data-html="true" title="'+rowData['dataset_title']+'"><img class="repository-icon" src="'+rowData['repository_icon_url']+'">'+rowData['dataset_accession']+'</a>'
            url_html = '''<a href="'''+rowData['canned_analysis_url']+'''" data-animation="false" data-toggle="tooltip" data-placement="bottom" data-html="true" title="<iframe src=\''''+rowData['canned_analysis_url']+'''\'>"><img src="'''+rowData['tool_icon_url']+'''"></a>'''
            description_html = 'Analysis Description.'
            metadata_html = '<ul><li>'+'</li><li>'.join(['<b>'+metadataRowData['term_name'].replace('_', ' ').title()+'</b>: '+metadataRowData['value'] for metadataIndex, metadataRowData in metadata[metadata['canned_analysis_fk'] == index].iterrows()]) + '</li></ul>'
            print ['<b>'+metadataRowData['term_name'].replace('_', ' ').title()+'</b>: '+metadataRowData['value'] for metadataIndex, metadataRowData in metadata[metadata['canned_analysis_fk'] == index].iterrows()]
            result_list.append([tool_html, dataset_html, url_html, description_html, metadata_html])
        result_dataframe = pd.DataFrame(result_list, columns=['Tool', 'Dataset', 'Analysis', 'Description', 'Metadata'])
        return result_dataframe.to_html(escape=False, index=False, classes='canned-analysis-table').encode('ascii', 'ignore')
