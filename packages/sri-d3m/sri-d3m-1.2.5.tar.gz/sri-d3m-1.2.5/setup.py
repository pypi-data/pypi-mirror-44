import setuptools

from sri.common import config

setuptools.setup(
    name = config.PACKAGE_NAME,

    version = config.VERSION,

    description = 'Graph and PSL based TA1 primitive for D3M',
    long_description = 'Graph and PSL based TA1 primitive for D3M',
    keywords = 'd3m_primitive',

    maintainer_email = config.EMAIL,
    maintainer = config.MAINTAINER,

    # The project's main homepage.
    url = config.REPOSITORY,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Programming Language :: Python :: 3.6',
    ],

    # packages = setuptools.find_packages(exclude = ['contrib', 'docs', 'tests']),
    packages = [
        'sri',
        'sri.autoflow',
        'sri.baseline',
        'sri.common',
        'sri.graph',
        'sri.pipelines',
        'sri.psl',
        'sri.psl.cli',
        'sri.tpot',
    ],

    include_package_data = True,
    package_data = {
        'sri.psl.cli': [
            'psl-cli-CANARY-2.1.5.jar',
            'link_prediction_template.data',
            'link_prediction_template.psl'
            'general_relational_template.data',
            'general_relational_template.psl',
            'relational_timeseries_template.data',
            'relational_timeseries_template.psl',
        ]
    },

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = [
        # Base
        'd3m', 'psutil',
        # TPOT
        'pathos', 'sri_tpot',
        # Testing
        'sripipeline',

        # Already provided by d3m (let d3m manage the exact versions):
        # 'networkx', 'numpy', 'pandas', 'scikit-learn',
    ],

    python_requires = '>=3.6',

    entry_points = {
        'd3m.primitives': [
            'data_transformation.conditioner.Conditioner = sri.autoflow.conditioner:Conditioner',
            'data_preprocessing.dataset_text_reader.DatasetTextReader = sri.autoflow.dataset_text_reader:DatasetTextReader',
            'data_transformation.conditioner.StaticEnsembler = sri.autoflow.static_ensembler:StaticEnsembler',
            'classification.gaussian_classification.MeanBaseline = sri.baseline.mean:MeanBaseline',
            'data_transformation.collaborative_filtering_parser.CollaborativeFilteringParser = sri.graph.collaborative_filtering:CollaborativeFilteringParser',
            'data_transformation.community_detection_parser.CommunityDetectionParser = sri.graph.community_detection:CommunityDetectionParser',
            'data_transformation.graph_matching_parser.GraphMatchingParser = sri.graph.graph_matching:GraphMatchingParser',
            'data_transformation.graph_transformer.GraphTransformer = sri.graph.transform:GraphTransformer',
            'data_transformation.vertex_nomination_parser.VertexNominationParser = sri.graph.vertex_nomination:VertexNominationParser',
            'link_prediction.collaborative_filtering_link_prediction.CollaborativeFilteringLinkPrediction = sri.psl.collaborative_filtering_link_prediction:CollaborativeFilteringLinkPrediction',
            'classification.community_detection.CommunityDetection = sri.psl.community_detection:CommunityDetection',
            # Until we have preprocessing code to prepare the data, do not expose this entrypoint.
            # 'sri.psl.GeneralRelational = sri.psl.general_relational:GeneralRelational',
            'classification.general_relational_dataset.GeneralRelationalDataset = sri.psl.general_relational_dataset:GeneralRelationalDataset',
            'link_prediction.graph_matching_link_prediction.GraphMatchingLinkPrediction = sri.psl.graph_matching_link_prediction:GraphMatchingLinkPrediction',
            'link_prediction.link_prediction.LinkPrediction = sri.psl.link_prediction:LinkPrediction',
            'time_series_forecasting.time_series_to_list.RelationalTimeseries = sri.psl.relational_timeseries:RelationalTimeseries',
            'classification.vertex_nomination.VertexNomination = sri.psl.vertex_nomination:VertexNomination',
            'data_transformation.stacking_operator.StackingOperator = sri.tpot.stacking:StackingOperator',
            'data_transformation.zero_count.ZeroCount = sri.tpot.zerocount:ZeroCount',

            # TODO(eriq): Will be moved to common primitives when actually implemented.
            'data_transformation.graph_node_splitter.GraphNodeSplitter = sri.graph.node_splitter:GraphNodeSplitter',
            'data_transformation.graph_to_edge_list.GraphToEdgeList = sri.graph.graph_to_edgelist:GraphToEdgeList',
            'data_transformation.edge_list_to_graph.EdgeListToGraph = sri.graph.edgelist_to_graph:EdgeListToGraph',
        ]
    }
)
