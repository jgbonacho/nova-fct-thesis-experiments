import os

ROOT_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', '..')

SYNTHETIC_NETWORKS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'synthetic')

SYNTHETIC_RESULTS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'results', 'synthetic')

REAL_WORLD_TRAIN_NETWORKS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'train-with-gt')
REAL_WORLD_TEST_NETWORKS_WITH_GT_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'test-with-gt')
REAL_WORLD_TEST_NETWORKS_WITHOUT_GT_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'test-without-gt')

REAL_WORLD_RESULTS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'results', 'real-world')
REAL_WORLD_RESULTS_TRAIN_NETWORKS_NAME = "train_networks"
REAL_WORLD_RESULTS_TRAIN_NETWORKS_WITH_GT_NAME = "test_with_train_networks"
REAL_WORLD_RESULTS_TEST_NETWORKS_WITH_GT_NAME = "test_networks_with_gt"
REAL_WORLD_RESULTS_TEST_NETWORKS_WITHOUT_GT_NAME = "test_networks_without_gt"
