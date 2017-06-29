#################################################################
#################################################################
########## 1. Libraries #########################################
#################################################################
#################################################################
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

#################################################################
#################################################################
########## 3. Analysis Notebook Class ###########################
#################################################################
#################################################################

#######################################################
########## 1. Initialize ##############################
#######################################################

class AnalysisNotebook:

	def __init__(self, config_dict):

		# Add notebook
		self.notebook = nbf.v4.new_notebook()

		# Add description
		self.notebook['cells'].append(nbf.v4.new_markdown_cell('# Analysis Notebook\n## 1. Load Modules'))

		# Setup code
		self.notebook['cells'].append(nbf.v4.new_code_cell('\n'.join(['import sys', 'import plotly', 'plotly.offline.init_notebook_mode()', 'sys.path.append("scripts")', "import datasets2tools as d2t"])))

		# Fetch dataset
		self.notebook['cells'].append(nbf.v4.new_markdown_cell('## 2. Get Dataset'))
		self.notebook['cells'].append(nbf.v4.new_code_cell('\n'.join([
			'# Get data',
			'dataset = d2t.fetch_dataset(dataset_id="{dataset_id}", dataset_source="{dataset_source}")'.format(**config_dict['dataset']),
			'dataset.rawcount_dataframe.head()'
		])))
		self.notebook['cells'].append(nbf.v4.new_code_cell('dataset.sample_metadata_dataframe.head()'))

		# Add analyses
		for tool in config_dict['tools']:
			
			# Get parameter string
			tool['parameter_str'] = ', '.join(['='.join([key, '"'+value+'"']) for key, value in tool['params'].iteritems()])

			# Add cell
			self.notebook['cells'].append(nbf.v4.new_code_cell('\n'.join([
				'# {comment}\ndataset.{tool_name}({parameter_str})'.format(**tool)
			])))




	#######################################################
	########## 2. Export to HTML ##########################
	#######################################################

	def export_to_html(self):

		# Add preprocessor
		ep = ExecutePreprocessor(timeout=600)

		# Process
		ep.preprocess(self.notebook, {'metadata': {'path': '.'}})

		# create a configuration object that changes the preprocessors
		from traitlets.config import Config
		c = Config()
		c.HTMLExporter.preprocessors = ['nbconvert.preprocessors.ExtractOutputPreprocessor']

		# create the new exporter using the custom config
		html_exporter_with_figs = HTMLExporter(config=c)
		html_exporter_with_figs.preprocessors
		resources_with_fig = html_exporter_with_figs.from_notebook_node(self.notebook)[0]

		# Return
		return resources_with_fig
