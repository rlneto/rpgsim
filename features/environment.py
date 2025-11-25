# Behave environment setup file
import os

# Set up environment variables or configuration
def before_all(context):
    # Initialize shared context variables
    context.game_initialized = True
    context.test_data_path = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    
    # Create test data directory if it doesn't exist
    if not os.path.exists(context.test_data_path):
        os.makedirs(context.test_data_path)
    
    # Set up test data
    context.random_seed = 12345  # For reproducible tests
    context.test_mode = True

def after_all(context):
    # Clean up after all tests
    pass

def before_feature(context, feature):
    # Set up before each feature
    context.feature_name = feature.name

def after_feature(context, feature):
    # Clean up after each feature
    pass

def before_scenario(context, scenario):
    # Set up before each scenario
    context.scenario_name = scenario.name

def after_scenario(context, scenario):
    # Clean up after each scenario
    pass