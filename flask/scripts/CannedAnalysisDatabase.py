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
        sorted_search_results = pd.read_sql_query('SELECT DISTINCT canned_analysis_fk FROM canned_analysis_metadata WHERE canned_analysis_fk IN (SELECT canned_analysis_fk FROM canned_analysis_metadata WHERE value = "' + '") AND canned_analysis_fk IN (SELECT canned_analysis_fk FROM canned_analysis_metadata WHERE value = "'.join(keywords)+'")', self.engine)
        # sorted_search_results = pd.read_sql_query('SELECT canned_analysis_fk, count(canned_analysis_fk) as count FROM canned_analysis_metadata WHERE value IN ("' + '", "'.join(keywords) + '") GROUP BY canned_analysis_fk ORDER BY count DESC', self.engine)
        ids = sorted_search_results['canned_analysis_fk'].tolist()
        return ids

    def make_canned_analysis_table(self, ids, limit=25):
        ids = ids[:limit]
        canned_analyses = pd.read_sql_query('SELECT ca.id as id, tool_name, tool_icon_url, tool_homepage_url, tool_description, repository_name, repository_homepage_url, repository_icon_url, repository_description, dataset_description, dataset_title, dataset_landing_url, dataset_accession, canned_analysis_url, tool_screenshot_url FROM canned_analysis ca LEFT JOIN dataset d ON d.id=ca.dataset_fk LEFT JOIN tool t ON t.id=ca.tool_fk LEFT JOIN repository r ON r.id=d.repository_fk WHERE ca.id IN ('+', '.join([str(x) for x in ids])+')', self.engine, index_col='id')
        metadata = pd.read_sql_query('SELECT canned_analysis_fk, term_name, value FROM canned_analysis_metadata cam LEFT JOIN term t on t.id = cam.term_fk WHERE cam.canned_analysis_fk IN ('+', '.join([str(x) for x in ids])+')', self.engine)
        result_list = []
        for index, rowData in canned_analyses.iterrows():
            tool_html = '<div class="tool-cell"><div class="tool-cell-logo"><a href="'+rowData['tool_homepage_url']+'"><img class="tool-cell-logo-icon" src="'+rowData['tool_icon_url']+'"></a><span class="tool-cell-logo-title">'+rowData['tool_name']+'</span></div><span class="tool-cell-text">'+rowData['tool_description']+'</span></div>'
            dataset_html = '<div class="dataset-cell"><div class="dataset-cell-logo"><a href="'+rowData['dataset_landing_url']+'""><img class="dataset-cell-logo-icon" src="'+rowData['repository_icon_url']+'"></a><span class="dataset-cell-logo-title">'+rowData['dataset_accession']+'</div><span class="dataset-cell-text">'+rowData['dataset_title']+'</span></div>'
            analysis_hyml = '<div class="analysis-cell"><img class="analysis-cell-icon" src="'+rowData['tool_screenshot_url']+'"><span class="analysis-cell-text">'+'Description'+'</span></div>'
            metadata_html = '<ul class="metadata-list"><li>'+'</li><li>'.join(['<b>'+metadataRowData['term_name'].replace('_', ' ').title()+'</b>: '+metadataRowData['value'] for metadataIndex, metadataRowData in metadata[metadata['canned_analysis_fk'] == index].iterrows()]) + '</li></ul>'
            result_list.append([tool_html, dataset_html, analysis_hyml, metadata_html])
        result_dataframe = pd.DataFrame(result_list, columns=['Tool', 'Dataset', 'Analysis', 'Metadata'])
        return result_dataframe.to_html(escape=False, index=False, classes='canned-analysis-table').encode('ascii', 'ignore')
