import re, json
import pandas as pd
pd.set_option('max.colwidth', -1)

class CannedAnalysisDatabase:

#######################################################
########## 1. Initialize ##############################
#######################################################
    
    def __init__(self, engine):
        self.engine = engine

#######################################################
########## 2. Search ##################################
#######################################################

##############################
##### 2.1 Keyword Search
##############################

    def keyword_search(self, object_type, keywords_list, size):
        try:
            if object_type == 'analysis':
                query = 'SELECT id FROM canned_analysis WHERE id IN ('
                query_terms = []
                for keyword in keywords_list:
                    query_terms.append('SELECT DISTINCT canned_analysis_fk AS id FROM canned_analysis_metadata WHERE value LIKE "%%{keyword}%%" UNION SELECT id FROM canned_analysis WHERE CONCAT(canned_analysis_title, " ", canned_analysis_description) LIKE "%%{keyword}%%"'.format(**locals()))
                query += ') AND id IN ('.join(query_terms) + ')'
            elif object_type == 'dataset':
                query = 'SELECT id FROM dataset WHERE id IN (SELECT id FROM dataset WHERE CONCAT(dataset_accession, " ", dataset_title, " ", dataset_description) LIKE "%%' + '%%") AND id IN (SELECT id FROM dataset WHERE CONCAT(dataset_accession, " ", dataset_title, " ", dataset_description) LIKE "%%'.join(keywords_list)+'%%")'
            elif object_type == 'tool':
                query = 'SELECT id FROM tool WHERE id IN (SELECT id FROM tool WHERE CONCAT(tool_name, " ", tool_description) LIKE "%%' + '%%") AND id IN (SELECT id FROM tool WHERE CONCAT(tool_name, " ", tool_description) LIKE "%%'.join(keywords_list)+'%%")'
            else:
                raise ValueError('Wrong object_type specified.  Must be analysis, dataset or tool.')
            if keywords_list == ['None']:
                raise ValueError('No keywords specified.  Please insert a comma-separated string of keywords for the search.')
            query += 'LIMIT {size}'.format(**locals())
            search_results = pd.read_sql_query(query, self.engine)
            ids = search_results['id'].tolist()
        except:
            ids = None
        return ids

##############################
##### 2.2 Advanced Search
##############################

    def advanced_search(self, query, object_type):

        try:

            # no query
            if query == 'None':
                raise ValueError('Query not specified.  Please use the query builder to construct a query.')

            # object type db query handling
            if object_type == 'analysis':
                db_query = 'SELECT DISTINCT ca.id AS id FROM canned_analysis ca LEFT JOIN canned_analysis_metadata cam ON ca.id=cam.canned_analysis_fk LEFT JOIN dataset d on d.id=ca.dataset_fk LEFT JOIN tool t ON t.id=ca.tool_fk WHERE '
            elif object_type == 'dataset':
                db_query = 'SELECT d.id AS id FROM dataset d LEFT JOIN repository r ON r.id=d.repository_fk WHERE '
            elif object_type == 'tool':
                db_query = 'SELECT id FROM tool WHERE '
            else:
                raise ValueError('Wrong object_type specified.  Must be analysis, dataset or tool.')

            # operators and separators
            operators = " NOT CONTAINS | CONTAINS | IS NOT | IS "
            separators = "AND|OR "

            # metadata terms
            metadata_term_names = pd.read_sql_query('SELECT * FROM term', self.engine)['term_name'].tolist() 

            # query terms
            for query_term in query.replace('(', '').split(') '):
                # split
                variable, value = re.split(operators, query_term.replace('AND ', '').replace('OR ', '').replace('"', '').replace(')', ''))
                operator = re.search(operators, query_term).group(0).replace('CONTAINS', 'LIKE').replace('IS NOT', '!=').replace('IS', '=')
                separator = re.search(separators, query_term).group(0) if re.search(separators, query_term) else ''
                value = '%%{value}%%'.format(**locals()) if 'LIKE' in operator else value
                # build
                if variable in metadata_term_names and object_type == 'analysis':
                    db_query += ' {separator} ca.id IN (SELECT DISTINCT canned_analysis_fk AS id FROM canned_analysis_metadata cam LEFT JOIN term t ON t.id=cam.term_fk WHERE `term_name` = "{variable}" AND `value`{operator}"{value}")'.format(**locals())
                elif variable == 'all_fields':
                    if object_type == 'analysis':
                        db_query += ' {separator} ca.id IN (SELECT DISTINCT canned_analysis_fk AS id FROM canned_analysis_metadata WHERE `value`{operator}"{value}" UNION SELECT id FROM canned_analysis WHERE CONCAT(canned_analysis_title, " ", canned_analysis_description){operator}"{value}")'.format(**locals())
                    if object_type == 'dataset':
                        db_query += ' {separator} (SELECT id FROM dataset WHERE CONCAT(dataset_accession, " ", dataset_title, " ", dataset_description){operator}"{value}")'.format(**locals())
                    if object_type == 'tool':
                        db_query += ' {separator} (SELECT id FROM tool WHERE CONCAT(tool_name, " ", tool_description){operator}"{value}")'.format(**locals())
                else:
                    db_query += ' {separator} `{variable}`{operator}"{value}"'.format(**locals())

            # size
            db_query += ' LIMIT 25'

            # db query
            print db_query
            search_results = pd.read_sql_query(db_query, self.engine)
            ids = search_results['id'].tolist() if len(search_results.index) > 0 else []
        except:
            ids = None
        return ids

##############################
##### 2.3 Analysis API
##############################

    def analysis_api(self, query_dict, size=25):
        try:
            sql_query = 'SELECT DISTINCT canned_analysis_fk AS id FROM canned_analysis ca LEFT JOIN canned_analysis_metadata cam ON ca.id=cam.canned_analysis_fk LEFT JOIN term ON term.id=cam.term_fk LEFT JOIN dataset d ON d.id=ca.dataset_fk LEFT JOIN tool ON tool.id=ca.tool_fk LEFT JOIN repository r on r.id=d.repository_fk'
            term_names = pd.read_sql_query('SELECT * FROM term', self.engine)['term_name'].tolist()
            query_terms = []
            if 'size' in query_dict.keys():
                size = query_dict.pop('size')
            for key, value in query_dict.iteritems():
                if 'id' in key:
                    query_terms.append('{key} = {value}'.format(**locals()))
                elif key in term_names:
                    query_terms.append('(`term_name` = "{key}" AND `value` = "{value}")'.format(**locals()))
                else:
                    query_terms.append('`{key}` = "{value}"'.format(**locals()))
            if len(query_terms) > 0:
                sql_query += ' WHERE ' + ' AND '.join(query_terms)
            sql_query += ' LIMIT {size}'.format(**locals())
            print sql_query
            print sql_query
            print sql_query
            print sql_query
            print sql_query
            print sql_query
            ids = pd.read_sql_query(sql_query, self.engine)['id'].tolist()
        except:
            ids = None
        return ids

##############################
##### 2.4 Dataset API
##############################

    def dataset_api(self, query_dict, size=25):
        try:
            sql_query = 'SELECT DISTINCT d.id FROM dataset d LEFT JOIN repository r on r.id=d.repository_fk'
            query_terms = []
            if 'size' in query_dict.keys():
                size = query_dict.pop('size')
            for key, value in query_dict.iteritems():
                if 'id' in key:
                    query_terms.append('{key} = {value}'.format(**locals()))
                else:
                    query_terms.append('`{key}` = "{value}"'.format(**locals()))
            if len(query_terms) > 0:
                sql_query += ' WHERE ' + ' AND '.join(query_terms)
            sql_query += ' LIMIT {size}'.format(**locals())
            ids = pd.read_sql_query(sql_query, self.engine)['id'].tolist()
        except:
            ids = None
        return ids

##############################
##### 2.5 Tool API
##############################

    def tool_api(self, query_dict, size=25):
        try:
            sql_query = 'SELECT DISTINCT id FROM tool t'
            query_terms = []
            if 'size' in query_dict.keys():
                size = query_dict.pop('size')
            for key, value in query_dict.iteritems():
                if 'id' in key:
                    query_terms.append('{key} = {value}'.format(**locals()))
                else:
                    query_terms.append('`{key}` = "{value}"'.format(**locals()))
            if len(query_terms) > 0:
                sql_query += ' WHERE ' + ' AND '.join(query_terms)
            sql_query += ' LIMIT {size}'.format(**locals())
            ids = pd.read_sql_query(sql_query, self.engine)['id'].tolist()
        except:
            ids = None
        return ids

#######################################################
########## 3. JSON Summary ############################
#######################################################

##############################
##### 3.1 Analysis
##############################

    def analysis_summary(self, id):
        analysis_data = pd.read_sql_query('SELECT canned_analysis_accession, canned_analysis_title, canned_analysis_description, canned_analysis_url, canned_analysis_preview_url, dataset_accession, dataset_title, dataset_description, dataset_landing_url, tool_name, tool_description, tool_homepage_url FROM canned_analysis ca LEFT JOIN dataset d on d.id=ca.dataset_fk LEFT JOIN tool t ON t.id=ca.tool_fk LEFT JOIN repository r on r.id=d.repository_fk WHERE ca.id = {id}'.format(**locals()), self.engine)
        analysis_metadata = pd.read_sql_query('SELECT term_name, value FROM canned_analysis_metadata cam LEFT JOIN term t on t.id=cam.term_fk WHERE canned_analysis_fk = {id}'.format(**locals()), self.engine, index_col='term_name')
        analysis_summary_dict = analysis_data.to_dict(orient='index')[0]
        analysis_summary_dict['metadata'] = {index: rowData['value'] for index, rowData in analysis_metadata.iterrows()}
        return analysis_summary_dict

##############################
##### 3.2 Dataset
##############################

    def dataset_summary(self, id):
        dataset_data = pd.read_sql_query('SELECT * FROM dataset d LEFT JOIN repository r on r.id=d.repository_fk WHERE d.id = {id}'.format(**locals()), self.engine)
        dataset_analysis_data = pd.read_sql_query('SELECT tool_name, count(*) AS count FROM canned_analysis ca LEFT JOIN dataset d ON d.id=ca.dataset_fk LEFT JOIN tool t ON t.id=ca.tool_fk WHERE d.id = {id} GROUP BY tool_name ORDER BY count DESC'.format(**locals()), self.engine, index_col='tool_name')
        dataset_summary_dict = dataset_data.to_dict(orient='index')[0]
        dataset_summary_dict['canned_analysis_count'] = dataset_analysis_data.to_dict()['count']
        return dataset_summary_dict

##############################
##### 3.3 Tool
##############################

    def tool_summary(self, id):
        tool_data = pd.read_sql_query('SELECT * FROM tool WHERE id = {id}'.format(**locals()), self.engine)
        tool_summary_dict = tool_data.to_dict(orient='index')[0]
        tool_summary_dict['canned_analyses'] = pd.read_sql_query('SELECT count(*) AS count FROM canned_analysis ca LEFT JOIN tool t ON t.id=ca.tool_fk WHERE t.id = {id}'.format(**locals()), self.engine)['count'][0]
        tool_summary_dict['datasets_analyzed'] = pd.read_sql_query('SELECT count(DISTINCT dataset_fk) AS count FROM canned_analysis ca LEFT JOIN tool t ON t.id=ca.tool_fk WHERE t.id = {id}'.format(**locals()), self.engine)['count'][0]
        return tool_summary_dict

#######################################################
########## 4. Table Display ###########################
#######################################################

##############################
##### 3.1 Analysis
##############################

    def analysis_table(self, analysis_summary_list):
        result_list = ['<hr width="100%">']
        for analysis_summary_dict in analysis_summary_list:
            result_list.append('''
                <div class="row">
                    <div class="col-9">
                        <p class="canned-analysis-title">
                            <a href="{canned_analysis_url}">
                                {canned_analysis_title}
                            </a>
                        </p>
                        <p class="canned-analysis-description">
                            {canned_analysis_description}
                        </p>
                        <p class="canned-analysis-annotation">
                            <span>Dataset: <a href="{dataset_landing_url}">{dataset_accession}</a></span>
                            <span>Analyzed by: <a href="{tool_homepage_url}">{tool_name}</a></span>
                            <span>Metadata: <a href="{dataset_landing_url}">i</a></span>
                        </p>
                        <p class="canned-analysis-accession">
                            <span>Accession: <a href="{canned_analysis_url}">{canned_analysis_accession}</a></span>
                        </p>
                    </div>
                    <div class="col-3">
                        <a href="{canned_analysis_url}">
                            <img src="{canned_analysis_preview_url}">
                        </a>
                    </div>
                    <hr width="100%">
                </div>
            
            '''.format(**analysis_summary_dict))
        return ''.join(result_list)


##############################
##### 3.2 Dataset
##############################

    def dataset_table(self, dataset_summary_list):
        result_list = ['<hr width="100%">']
        for dataset_summary_dict in dataset_summary_list:
            result_list.append('''
                <div class="row">
                    <div class="col-10">
                        <p class="dataset-title">
                            <a href="{dataset_landing_url}">
                                {dataset_title}
                            </a>
                        </p>
                        <p class="dataset-description">
                            {dataset_description}
                        </p>
                        <p class="dataset-analyses">
                            <span>Analyzed by: </span>
                        </p>
                        <p class="dataset-repository">
                            <span>Accession: <a href="{dataset_landing_url}">{dataset_accession}</a></span>
                            <span>Repository: <a href="{repository_homepage_url}">{repository_name}</a></span>
                        </p>
                    </div>
                    <div class="col-2">
                        <a href="{repository_homepage_url}">
                            <img src="{repository_icon_url}">
                        </a>
                    </div>
                    <hr width="100%">
                </div>
            
            '''.format(**dataset_summary_dict)
               .replace('Analyzed by: ', 'Analyzed by: '+', '.join('{key} (<a href="http://localhost:5000/datasets2tools/advanced_search?query=((object%20IS%20analyses)%20AND%20dataset_accession%20IS%20%22ACC%22)%20AND%20tool_name%20IS%20%22{key}%22">{value} analyses</a>)'.format(**locals()) for key, value in dataset_summary_dict['canned_analysis_count'].iteritems()))
               .replace('%22ACC%22', '%22{dataset_accession}%22'.format(**dataset_summary_dict)))
            
        return ''.join(result_list)

##############################
##### 3.3 Tool
##############################

    def tool_table(self, tool_summary_list):
        result_list = ['<hr width="100%">']
        for tool_summary_dict in tool_summary_list:
            result_list.append('''
                <div class="row">
                    <div class="col-10">
                        <p class="tool-name">
                            <a href="{tool_homepage_url}">
                                {tool_name}
                            </a>
                        </p>
                        <p class="tool-description">
                            {tool_description}
                        </p>
                        <p class="tool-analyses">
                            <span>Analyzed {datasets_analyzed} datasets, generating {canned_analyses} analyses </span>
                        </p>
                    </div>
                    <div class="col-2">
                        <a href="{tool_homepage_url}">
                            <img src="{tool_icon_url}">
                        </a>
                    </div>
                    <hr width="100%">
                </div>
            
            '''.format(**tool_summary_dict))

        return ''.join(result_list)

#######################################################
########## 4. Card Display ############################
#######################################################

##############################
##### 3.1 Analysis
##############################

##############################
##### 3.2 Dataset
##############################

##############################
##### 3.3 Tool
##############################


#######################################################
########## 5. Display Wrapper #########################
#######################################################

##############################
##### 1. Annotate
##############################

    def get_annotations(self, ids, object_type, output='list'):
        if ids == []:
            return 'Sorry, no search results found'
        elif ids == 'None' or ids == None:
            return 'Sorry, there has been an error.'
        else:
            if object_type == 'analysis':
                summary_list = [self.analysis_summary(analysis_id) for analysis_id in ids]
            elif object_type == 'dataset':
                summary_list = [self.dataset_summary(dataset_id) for dataset_id in ids]
            elif object_type == 'tool':
                summary_list = [self.tool_summary(tool_id) for tool_id in ids]
            else:
                raise ValueError('Wrong object type specified.  Must be analysis, dataset or tool.')
            if output == 'list':
                return summary_list
            elif output == 'json':
                summary_json = json.dumps({'results': summary_list})
                return summary_json

##############################
##### 2. Make Table
##############################

    def table_from_summary_list(self, summary_list, object_type):
        if object_type == 'analysis':
            table_html = self.analysis_table(summary_list)
        elif object_type == 'dataset':
            table_html = self.dataset_table(summary_list)
        elif object_type == 'tool':
            table_html = self.tool_table(summary_list)
        else:
            raise ValueError('Wrong object type specified.  Must be analysis, dataset or tool.')
        return table_html

##############################
##### 3. Wrapper
##############################

    def table_from_ids(self, ids, object_type):
        if ids == []:
            return 'Sorry, no search results found'
        elif ids == None:
            return 'Sorry, there has been an error.'
        else:
            summary_list = self.get_annotations(ids, object_type)
            table_html = self.table_from_summary_list(summary_list, object_type)
            return table_html

#######################################################
########## 5. Miscellaneous ###########################
#######################################################

##############################
##### 1. Analysis Preview
##############################

    def get_analysis_preview(self, analysis_json):
        analysis_dict = json.loads(analysis_json)
        analysis_dict['dataset'] = [self.dataset_summary(x) if type(x) != dict else x for x in analysis_dict['dataset']]
        analysis_dict['tool'] = self.tool_summary(analysis_dict['tool']) if type(analysis_dict['tool']) != dict else analysis_dict['tool']
        preview = '''
                <div class="row">
                    <div class="col-9">
                        <p class="canned-analysis-title">
                            <a href="{canned_analysis_url}">
                                {canned_analysis_title}
                            </a>
                        </p>
                        <p class="canned-analysis-description">
                            {canned_analysis_description}
                        </p> '''.format(**analysis_dict['analysis']) + '''
                        <p class="canned-analysis-annotation">
                            <span>Datasets: ''' + ', '.join(['<a href="{dataset_landing_url}">{dataset_accession}</a>'.format(**x) for x in analysis_dict['dataset']]) + '''</span>
                            <span>Analyzed by: <a href="{tool_homepage_url}">{tool_name}</a></span> '''.format(**analysis_dict['tool'])  + '''
                            <span>Metadata: <a href="#">i</a></span>
                        </p>
                    </div>
                    <div class="col-3">
                        <a href="{canned_analysis_url}">
                            <img class="analysis-preview-image" src="{canned_analysis_preview_url}">
                        </a>
                    </div>
                    <hr width="100%">
                </div>
            
            '''.format(**analysis_dict['analysis'])
        return preview

##############################
##### 2. Advanced Search Dropdown terms
##############################

    def get_available_search_terms(self):
        canned_analysis_metadata_terms = pd.read_sql_query('SELECT term_name FROM term', self.engine)['term_name'].tolist()
        dataset_terms = ['dataset_accession', 'dataset_title', 'dataset_description', 'repository', 'repository_description']
        tool_terms = ['tool_name', 'tool_description']
        available_search_terms = {
            'analysis': [x.replace('_', ' ').title() for x in ['All Fields']+canned_analysis_metadata_terms+dataset_terms+tool_terms],
            'dataset': [x.replace('_', ' ').title() for x in ['All Fields']+dataset_terms],
            'tool': [x.replace('_', ' ').title() for x in ['All Fields']+tool_terms]
        }
        return available_search_terms

##############################
##### 3.2 Dataset
##############################

##############################
##### 3.3 Tool
##############################



#######################################################
########## 2. Keyword Search ##########################
#######################################################

    def make_canned_analysis_table(self, ids, limit=25):
        ids = ids[:limit]
        canned_analyses = pd.read_sql_query('SELECT ca.id as id, tool_name, tool_icon_url, tool_homepage_url, tool_description, repository_name, repository_homepage_url, repository_icon_url, repository_description, dataset_description, dataset_title, dataset_landing_url, dataset_accession, canned_analysis_url, tool_screenshot_url FROM canned_analysis ca LEFT JOIN dataset d ON d.id=ca.dataset_fk LEFT JOIN tool t ON t.id=ca.tool_fk LEFT JOIN repository r ON r.id=d.repository_fk WHERE ca.id IN ('+', '.join([str(x) for x in ids])+')', self.engine, index_col='id')
        metadata = pd.read_sql_query('SELECT canned_analysis_fk, term_name, term_description, value FROM canned_analysis_metadata cam LEFT JOIN term t on t.id = cam.term_fk WHERE term_name != "description" AND cam.canned_analysis_fk IN ('+', '.join([str(x) for x in ids])+') ORDER BY term_name', self.engine)
        descriptions = dict(pd.read_sql_query('SELECT canned_analysis_fk, value FROM canned_analysis_metadata cam LEFT JOIN term t on t.id = cam.term_fk WHERE term_name = "description"', self.engine, index_col='canned_analysis_fk'))['value']
        result_list = []
        for index, rowData in canned_analyses.iterrows():
            tool_html = '<div class="tool-cell"><a class="tool-cell-logo" href="'+rowData['tool_homepage_url']+'"><img class="tool-cell-logo-icon" src="'+rowData['tool_icon_url']+'"><span class="tool-cell-logo-title">'+rowData['tool_name']+'</span></a><span class="tool-cell-text">'+rowData['tool_description']+'</span></div>'
            dataset_html = '<div class="dataset-cell"><a class="dataset-cell-logo" href="'+rowData['dataset_landing_url']+'""><img class="dataset-cell-logo-icon" src="'+rowData['repository_icon_url']+'"><span class="dataset-cell-logo-title">'+rowData['dataset_accession']+'</span></a><span class="dataset-cell-text">'+rowData['dataset_title']+' <sup><i class="fa fa-info-circle fa-1x"  aria-hidden="true" data-toggle="tooltip" data-placement="right" data-html="true" title="'+rowData['dataset_description']+'"></i></sup></span></div>'
            analysis_html = '<div class="analysis-cell"><a href="'+rowData['canned_analysis_url']+'"><img class="analysis-cell-icon" src="'+rowData['tool_screenshot_url']+'"></a><div class="analysis-cell-text">'+descriptions[index]+'.</div></div>'
            metadata_html = '<div class="metadata-cell">'+'<br>'.join(['<span class="metadata-cell-tag">'+metadataRowData['term_name'].replace('_', ' ').title()+'</span><sup>&nbsp<i class="fa fa-info-circle fa-1x"  aria-hidden="true" data-toggle="tooltip" data-placement="top" data-html="true" data-animation="false" title="'+metadataRowData['term_description']+'"></i></sup>: <span class="metadata-cell-value">'+metadataRowData['value']+'</span>' for metadataIndex, metadataRowData in metadata[metadata['canned_analysis_fk'] == index].iterrows()]) + '</div>'
            result_list.append([tool_html, dataset_html, analysis_html, metadata_html])
        result_dataframe = pd.DataFrame(result_list, columns=['Tool', 'Dataset', 'Analysis', 'Metadata'])
        return result_dataframe.to_html(escape=False, index=False, classes='canned-analysis-table').encode('ascii', 'ignore')

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
            analysis_html = '<div class="dataset-tool-analysis-count-cell">'+''.join('<div class="dataset-tool-analysis-count"><a class="dataset-tool-analysis-count-tool-link" href="'+countRowData['tool_homepage_url']+'"><img class="dataset-tool-analysis-count-icon" src="'+countRowData['tool_icon_url']+'"></a><div class="dataset-tool-analysis-count-text"><a href="'+countRowData['tool_homepage_url']+'" class="dataset-tool-analysis-count-title">'+countRowData['tool_name']+'</a><sup> <i class="fa fa-info-circle fa-1x" aria-hidden="true" data-toggle="tooltip" data-placement="top" data-html="true" data-animation="false" title="'+countRowData['tool_description']+'"></i></sup>: <a href="http://localhost:5000/datasets2tools/advanced_search?query=((object%20IS%20analyses)%20AND%20dataset_accession%20IS%20%22'+rowData['dataset_accession']+'%22)%20AND%20tool_name%20IS%20%22'+countRowData['tool_name']+'%22" class="dataset-tool-analysis-count-analysis">' + str(countRowData['count']) + ' analys'+return_letter(countRowData['count'])+'s</a></div></div>' for countIndex, countRowData in analysis_counts[analysis_counts['dataset_accession']==rowData['dataset_accession']].iterrows()) + '</div>'
            result_list.append([dataset_html, description_html, repository_html, analysis_html])
        result_dataframe = pd.DataFrame(result_list, columns=['Dataset', 'Description', 'Repository', 'Analyses']).set_index('Dataset', drop=False)#.loc[analysis_counts['dataset_accession'].unique()]
        return result_dataframe.to_html(escape=False, index=False, classes='dataset-table').encode('ascii', 'ignore')

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

    def get_keyword_json(self, ignore_keywords=['pert_ids', 'description', 'ctrl_ids', 'creeds_id', 'smiles', 'mm_gene_symbol', 'chdir_norm', 'top_genes']):
        values = pd.read_sql_query('SELECT DISTINCT term_name, value, count(*) AS count FROM canned_analysis_metadata cam LEFT JOIN term t on t.id=cam.term_fk WHERE term_name NOT IN ("'+'", "'.join(ignore_keywords)+'") GROUP BY term_name, value HAVING count > 10 ORDER BY count ASC', self.engine, index_col='term_name')
        tree_dict = {'name': 'Canned Analyses', 'children': [{'name': term_name.replace('_', ' ').title(), 'children': [{'name': rowData['value'], 'size': rowData['count']} for index, rowData in values.loc[term_name].iterrows()]} for term_name in values.index.unique()]}
        return tree_dict

    def get_keyword_count(self, ignore_keywords=['pert_ids', 'description', 'ctrl_ids', 'creeds_id', 'smiles', 'mm_gene_symbol', 'chdir_norm', 'top_genes']):
        keyword_count = pd.read_sql_query('SELECT DISTINCT term_name, value, count(*) AS count FROM canned_analysis_metadata cam LEFT JOIN term t on t.id=cam.term_fk WHERE term_name NOT IN ("'+'", "'.join(ignore_keywords)+'") GROUP BY term_name, value', self.engine, index_col='term_name')

    def get_term_names(self, object_type):
        canned_analysis_metadata_terms = pd.read_sql_query('SELECT term_name FROM term', self.engine)['term_name'].tolist()
        dataset_terms = ['dataset_accession', 'dataset_title', 'dataset_description', 'repository', 'repository_description']
        tool_terms = ['tool_name', 'tool_description']
        if object_type == 'Analyses':
            available_search_terms = ['All Fields']+canned_analysis_metadata_terms+dataset_terms+tool_terms
            return '\n'.join([x.replace('_', ' ').title() for x in available_search_terms])
        elif object_type == 'Datasets':
            available_search_terms = ['All Fields']+dataset_terms
            return '\n'.join([x.replace('_', ' ').title() for x in available_search_terms])
        elif object_type == 'Tools':
            available_search_terms = ['All Fields']+tool_terms
            return '\n'.join([x.replace('_', ' ').title() for x in available_search_terms])

    def get_stored_data(self):
        stored_data = {x: pd.read_sql_query('SELECT * FROM %(x)s' % locals(), self.engine, index_col='id') for x in ['dataset', 'tool', 'term', 'repository']}
        return stored_data

    def object_search(self, object_type, column, value):
        if object_type == 'dataset':
            return json.dumps(pd.read_sql_query('SELECT d.id AS id, dataset_accession, dataset_title, dataset_description, dataset_landing_url, repository_name, repository_description, repository_homepage_url, repository_icon_url FROM dataset d LEFT JOIN repository r on r.id = d.repository_fk WHERE {column} = {value}'.format(**locals()), self.engine).to_dict(orient='index')[0])
        elif object_type == 'tool':
            return json.dumps(pd.read_sql_query('SELECT * FROM tool WHERE {column} = {value}'.format(**locals()), self.engine).to_dict(orient='index')[0])        
        elif object_type == 'repository':
            return json.dumps(pd.read_sql_query('SELECT * FROM repository WHERE {column} = {value}'.format(**locals()), self.engine).to_dict(orient='index')[0])
        else:
            return 'Wrong object type specified - must be dataset, tool, repository.'

    def prepare_canned_analysis_table(self, canned_analysis_json):
        canned_analysis_dict = json.loads(canned_analysis_json)
        if 'keywords' in canned_analysis_dict['analysis_metadata'].keys():
            canned_analysis_dict['analysis_metadata']['keywords'] = ', '.join(canned_analysis_dict['analysis_metadata']['keywords'])
        result_list = []
        tool_html = '<div class="tool-cell"><a class="tool-cell-logo" href="'+canned_analysis_dict['tool']['tool_homepage_url']+'"><img class="tool-cell-logo-icon" src="'+canned_analysis_dict['tool']['tool_icon_url']+'"><span class="tool-cell-logo-title">'+canned_analysis_dict['tool']['tool_name']+'</span></a><span class="tool-cell-text">'+canned_analysis_dict['tool']['tool_description']+'</span></div>'
        dataset_html = '<div class="dataset-cell"><a class="dataset-cell-logo" href="'+canned_analysis_dict['dataset']['dataset_landing_url']+'""><img class="dataset-cell-logo-icon" src="'+"https://datamed.org/img/repositories/0003.png"+'"><span class="dataset-cell-logo-title">'+canned_analysis_dict['dataset']['dataset_accession']+'</span></a><span class="dataset-cell-text">'+canned_analysis_dict['dataset']['dataset_title']+' <sup><i class="fa fa-info-circle fa-1x"  aria-hidden="true" data-toggle="tooltip" data-placement="right" data-html="true" title="'+canned_analysis_dict['dataset']['dataset_description']+'"></i></sup></span></div>'
        analysis_html = '<div class="analysis-cell"><a href="'+canned_analysis_dict['analysis']['canned_analysis_url']+'"><img class="analysis-cell-icon" src="'+canned_analysis_dict['analysis']['canned_analysis_snapshot_url']+'"></a><div class="analysis-cell-text">'+canned_analysis_dict['analysis']['canned_analysis_description']+'.</div></div>'
        metadata_html = '<div class="metadata-cell">'+'<br>'.join(['<span class="metadata-cell-tag">'+term_name.replace('_', ' ').title()+'</span><sup>&nbsp<i class="fa fa-info-circle fa-1x"  aria-hidden="true" data-toggle="tooltip" data-placement="top" data-html="true" data-animation="false" title="'+"metadataRowData['term_description']"+'"></i></sup>: <span class="metadata-cell-value">'+value+'</span>' for term_name, value in canned_analysis_dict['analysis_metadata'].iteritems()]) + '</div>'
        result_list.append([tool_html, dataset_html, analysis_html, metadata_html])
        result_dataframe = pd.DataFrame(result_list, columns=['Tool', 'Dataset', 'Analysis', 'Metadata'])
        return result_dataframe.to_html(escape=False, index=False, classes='canned-analysis-table').encode('ascii', 'ignore')

