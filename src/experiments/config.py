import os

ROOT_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', '..')

# Synthetic experiments.
SYNTHETIC_NETWORKS_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'synthetic', 'training')

SYNTHETIC_RESULTS_PATH = os.path.join(ROOT_DIR_PATH, 'results', 'synthetic')

# Real-world experiments.
RW_TRAINING_NETWORKS_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'training')
RW_VALIDATION_NETWORKS_WITH_GT_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'validation', 'with-gt')
RW_VALIDATION_NETWORKS_WITHOUT_GT_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'validation', 'without-gt')
RW_TEST_NETWORKS_WITH_GT_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'test', 'with-gt')
RW_TEST_NETWORKS_WITHOUT_GT_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'test', 'without-gt')

RW_RESULTS_PATH = os.path.join(ROOT_DIR_PATH, 'results', 'real-world')
RW_RESULTS_REFERENCE_THS_NAME = "reference_ths"
RW_RESULTS_TRAINING_NETWORKS_NAME = "training_networks"
RW_RESULTS_VALIDATION_NETWORKS_WITH_GT_NAME = "validation_networks_with_gt"
RW_RESULTS_VALIDATION_NETWORKS_WITHOUT_GT_NAME = "validation_networks_without_gt"
RW_RESULTS_TEST_NETWORKS_WITH_GT_NAME = "test_networks_with_gt"
RW_RESULTS_TEST_NETWORKS_WITHOUT_GT_NAME = "test_networks_without_gt"
