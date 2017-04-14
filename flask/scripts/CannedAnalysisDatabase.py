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
        # matching_search_results = pd.read_sql_query('SELECT DISTINCT canned_analysis_fk FROM canned_analysis_metadata WHERE canned_analysis_fk IN (SELECT canned_analysis_fk FROM canned_analysis_metadata WHERE value = "' + '") AND canned_analysis_fk IN (SELECT canned_analysis_fk FROM canned_analysis_metadata WHERE value = "'.join(keywords)+'")', self.engine)
        similar_search_results = pd.read_sql_query('SELECT DISTINCT canned_analysis_fk FROM canned_analysis_metadata WHERE canned_analysis_fk IN (SELECT canned_analysis_fk FROM canned_analysis_metadata WHERE value LIKE "%%' + '%%") AND canned_analysis_fk IN (SELECT canned_analysis_fk FROM canned_analysis_metadata WHERE value LIKE "%%'.join(keywords)+'%%")', self.engine)
        ids = similar_search_results['canned_analysis_fk'].tolist()
        return ids

    def make_canned_analysis_table(self, ids, limit=25):
        ids = ids[:limit]
        canned_analyses = pd.read_sql_query('SELECT ca.id as id, tool_name, tool_icon_url, tool_homepage_url, tool_description, repository_name, repository_homepage_url, repository_icon_url, repository_description, dataset_description, dataset_title, dataset_landing_url, dataset_accession, canned_analysis_url, tool_screenshot_url FROM canned_analysis ca LEFT JOIN dataset d ON d.id=ca.dataset_fk LEFT JOIN tool t ON t.id=ca.tool_fk LEFT JOIN repository r ON r.id=d.repository_fk WHERE ca.id IN ('+', '.join([str(x) for x in ids])+')', self.engine, index_col='id')
        metadata = pd.read_sql_query('SELECT canned_analysis_fk, term_name, term_description, value FROM canned_analysis_metadata cam LEFT JOIN term t on t.id = cam.term_fk WHERE term_name != "description" AND cam.canned_analysis_fk IN ('+', '.join([str(x) for x in ids])+') ORDER BY term_name', self.engine)
        descriptions = dict(pd.read_sql_query('SELECT canned_analysis_fk, value FROM canned_analysis_metadata cam LEFT JOIN term t on t.id = cam.term_fk WHERE term_name = "description"', self.engine, index_col='canned_analysis_fk'))['value']
        print descriptions
        result_list = []
        for index, rowData in canned_analyses.iterrows():
            tool_html = '<div class="tool-cell"><a class="tool-cell-logo" href="'+rowData['tool_homepage_url']+'"><img class="tool-cell-logo-icon" src="'+rowData['tool_icon_url']+'"><span class="tool-cell-logo-title">'+rowData['tool_name']+'</span></a><span class="tool-cell-text">'+rowData['tool_description']+'</span></div>'
            dataset_html = '<div class="dataset-cell"><a class="dataset-cell-logo" href="'+rowData['dataset_landing_url']+'""><img class="dataset-cell-logo-icon" src="'+rowData['repository_icon_url']+'"><span class="dataset-cell-logo-title">'+rowData['dataset_accession']+'</span></a><span class="dataset-cell-text">'+rowData['dataset_title']+' <sup><i class="fa fa-info-circle fa-1x"  aria-hidden="true" data-toggle="tooltip" data-placement="right" data-html="true" title="'+rowData['dataset_description']+'"></i></sup></span></div>'
            analysis_hyml = '<div class="analysis-cell"><a href="'+rowData['canned_analysis_url']+'"><img class="analysis-cell-icon" src="'+rowData['tool_screenshot_url']+'"></a><div class="analysis-cell-text">'+descriptions[index]+'.</div></div>'
            metadata_html = '<div class="metadata-cell">'+'<br>'.join(['<span class="metadata-cell-tag">'+metadataRowData['term_name'].replace('_', ' ').title()+'</span><sup>&nbsp<i class="fa fa-info-circle fa-1x"  aria-hidden="true" data-toggle="tooltip" data-placement="top" data-html="true" data-animation="false" title="'+metadataRowData['term_description']+'"></i></sup>: <span class="metadata-cell-value">'+metadataRowData['value']+'</span>' for metadataIndex, metadataRowData in metadata[metadata['canned_analysis_fk'] == index].iterrows()]) + '</div>'
            result_list.append([tool_html, dataset_html, analysis_hyml, metadata_html])
        result_dataframe = pd.DataFrame(result_list, columns=['Tool', 'Dataset', 'Analysis', 'Metadata'])
        return result_dataframe.to_html(escape=False, index=False, classes='canned-analysis-table').encode('ascii', 'ignore')

    def search_datasets_by_keyword(self, keywords):
        similar_search_results = pd.read_sql_query('SELECT id FROM dataset WHERE id IN (SELECT id FROM dataset WHERE CONCAT(dataset_accession, " ", dataset_title, " ", dataset_description) LIKE "%%' + '%%") AND id IN (SELECT id FROM dataset WHERE CONCAT(dataset_accession, " ", dataset_title, " ", dataset_description) LIKE "%%'.join(keywords)+'%%")', self.engine)
        ids = similar_search_results['id'].tolist()
        return ids

    def make_dataset_table(self, ids, limit=25):
        ids = ids[:limit]
        analysis_counts = pd.read_sql_query('SELECT dataset_accession, tool_name, tool_icon_url, tool_description, tool_homepage_url, count(dataset_accession) AS count FROM canned_analysis ca LEFT JOIN dataset d on d.id=ca.dataset_fk LEFT JOIN tool t on t.id = ca.tool_fk WHERE d.id in ('+', '.join([str(x) for x in ids])+') GROUP BY dataset_accession, tool_name ORDER BY dataset_accession ASC, count DESC', self.engine)
        datasets = pd.read_sql_query('SELECT * FROM dataset d LEFT JOIN repository r on r.id = d.repository_fk WHERE d.id in ('+', '.join([str(x) for x in ids])+')', self.engine)
        datasets = datasets.set_index('dataset_accession', drop=False).loc[analysis_counts.groupby('dataset_accession').sum().sort_values('count', ascending=False).index].reset_index(drop=True)
        return_letter = lambda x: 'e' if x > 1 else 'i'
        result_list = []
        for index, rowData in datasets.iterrows():
            dataset_html = '<div class="dataset-title-cell"><a href="'+rowData['dataset_landing_url']+'" class="dataset-title-cell-accession">'+rowData['dataset_accession']+'</a><div class="dataset-title-cell-text">'+rowData['dataset_title']+'</div></div>'
            description_html = '<div class="dataset-description-cell">'+rowData['dataset_description']+'</div>'
            repository_html = '<div class="dataset-repository-cell"><a href="'+rowData['repository_homepage_url']+'"><img class="dataset-repository-cell-icon" src="'+rowData['repository_icon_url']+'"></a><div class="dataset-repository-cell-text">'+rowData['repository_name']+' <sup><i class="fa fa-info-circle fa-1x"  aria-hidden="true" data-toggle="tooltip" data-placement="bottom" data-html="true" data-animation="false" title="'+rowData['repository_description']+'"></i></sup></div></div>'
            analysis_html = '<div class="dataset-tool-analysis-count-cell">'+''.join('<div class="dataset-tool-analysis-count"><a class="dataset-tool-analysis-count-tool-link" href="'+countRowData['tool_homepage_url']+'"><img class="dataset-tool-analysis-count-icon" src="'+countRowData['tool_icon_url']+'"></a><div class="dataset-tool-analysis-count-text"><a href="'+countRowData['tool_homepage_url']+'" class="dataset-tool-analysis-count-title">'+countRowData['tool_name']+'</a><sup> <i class="fa fa-info-circle fa-1x" aria-hidden="true" data-toggle="tooltip" data-placement="top" data-html="true" data-animation="false" title="'+countRowData['tool_description']+'"></i></sup>: <a href="#" class="dataset-tool-analysis-count-analysis">' + str(countRowData['count']) + ' analys'+return_letter(countRowData['count'])+'s</a></div></div>' for countIndex, countRowData in analysis_counts[analysis_counts['dataset_accession']==rowData['dataset_accession']].iterrows()) + '</div>'
            result_list.append([dataset_html, description_html, repository_html, analysis_html])
        result_dataframe = pd.DataFrame(result_list, columns=['Dataset', 'Description', 'Repository', 'Analyses']).set_index('Dataset', drop=False)#.loc[analysis_counts['dataset_accession'].unique()]
        return result_dataframe.to_html(escape=False, index=False, classes='dataset-table').encode('ascii', 'ignore')

    def search_tools_by_keyword(self, keywords):
        similar_search_results = pd.read_sql_query('SELECT id FROM tool WHERE id IN (SELECT id FROM tool WHERE CONCAT(tool_name, " ", tool_description) LIKE "%%' + '%%") AND id IN (SELECT id FROM tool WHERE CONCAT(tool_name, " ", tool_description) LIKE "%%'.join(keywords)+'%%")', self.engine)
        ids = similar_search_results['id'].tolist()
        return ids

    def make_tool_table(self, ids, limit=25):
        ids = ids[:limit]
        tools = pd.read_sql_query('SELECT tool_name, tool_icon_url, tool_homepage_url, tool_description, count(*)-1 AS count FROM tool t LEFT JOIN canned_analysis ca on t.id = ca.tool_fk WHERE t.id IN ('+', '.join([str(x) for x in ids])+') GROUP BY tool_name ORDER BY count desc', self.engine)
        result_list = []
        for indew, rowData in tools.iterrows():
            tool_icon_html = '<a href="'+rowData['tool_homepage_url']+'" class="tool-icon-cell"><img class="tool-icon-cell-logo" src="'+rowData['tool_icon_url']+'"><div class="tool-icon-cell-text">'+rowData['tool_name']+'</div></a>'
            tool_description_html = '<div class="tool-description-cell">'+rowData['tool_description']+'</div>'
            analysis_html = '<a href="#" class="tool-analysis-count-cell">' + str(rowData['count']) + '</div>'
            result_list.append([tool_icon_html, tool_description_html, analysis_html])
        result_dataframe = pd.DataFrame(result_list, columns=['Tool', 'Description', 'Analyses'])
        return result_dataframe.to_html(escape=False, index=False, classes='tool-table').encode('ascii', 'ignore')

