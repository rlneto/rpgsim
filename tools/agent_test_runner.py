"""
Agent-optimized test runner
Simple, explicit testing optimized for LLM agents
"""

import sys
import os
import time
import importlib
import inspect
import traceback
from typing import List, Dict, Any, Callable
from pathlib import Path


class AgentTestRunner:
    """
    Simple test runner for LLM agents.
    Explicit execution - no hidden framework logic.
    """
    
    def __init__(self, test_directory: str = "tests"):
        self.test_directory = Path(test_directory)
        self.results = []
        self.passed = 0
        self.failed = 0
        self.start_time = None
        self.end_time = None
    
    def find_test_functions(self, module) -> List[Callable]:
        """
        Find test functions in module.
        Explicit function discovery - no magic.
        """
        test_functions = []
        
        for name in dir(module):
            obj = getattr(module, name)
            
            # Check if it's a test function
            if (name.startswith('test_') and 
                inspect.isfunction(obj) and 
                not name.startswith('test_')):
                test_functions.append(obj)
        
        return test_functions
    
    def run_single_test(self, test_func: Callable) -> Dict[str, Any]:
        """
        Run single test function.
        Explicit test execution - no hidden setup.
        """
        test_name = test_func.__name__
        
        try:
            # Execute test function
            start_time = time.time()
            test_func()
            end_time = time.time()
            
            # Record successful test
            self.passed += 1
            
            return {
                'name': test_name,
                'status': 'PASSED',
                'execution_time': end_time - start_time,
                'error': None,
                'traceback': None
            }
            
        except Exception as e:
            # Record failed test
            self.failed += 1
            
            return {
                'name': test_name,
                'status': 'FAILED',
                'execution_time': 0,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def run_test_file(self, test_file: str) -> Dict[str, Any]:
        """
        Run test file and return results.
        Explicit file execution - no hidden module loading.
        """
        file_path = self.test_directory / test_file
        
        if not file_path.exists():
            return {
                'file': test_file,
                'status': 'FILE_NOT_FOUND',
                'error': f"File not found: {file_path}",
                'tests': []
            }
        
        try:
            # Import test module
            module_name = f"{self.test_directory.name}.{test_file[:-3]}"
            test_module = importlib.import_module(module_name)
            
            # Find test functions
            test_functions = self.find_test_functions(test_module)
            
            # Run tests
            test_results = []
            for test_func in test_functions:
                result = self.run_single_test(test_func)
                test_results.append(result)
            
            return {
                'file': test_file,
                'status': 'COMPLETED',
                'tests': test_results,
                'total_tests': len(test_functions),
                'passed_tests': len([t for t in test_results if t['status'] == 'PASSED']),
                'failed_tests': len([t for t in test_results if t['status'] == 'FAILED'])
            }
            
        except Exception as e:
            return {
                'file': test_file,
                'status': 'IMPORT_ERROR',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'tests': []
            }
    
    def run_all_tests(self, pattern: str = "test_*.py") -> Dict[str, Any]:
        """
        Run all test files matching pattern.
        Explicit batch execution - no hidden test discovery.
        """
        self.start_time = time.time()
        
        # Find test files
        test_files = list(self.test_directory.glob(pattern))
        
        # Run each test file
        results = []
        for test_file in test_files:
            file_result = self.run_test_file(test_file.name)
            results.append(file_result)
        
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        
        return {
            'total_time': total_time,
            'total_files': len(test_files),
            'total_tests': sum(r.get('total_tests', 0) for r in results),
            'total_passed': self.passed,
            'total_failed': self.failed,
            'success_rate': (self.passed / (self.passed + self.failed)) if (self.passed + self.failed) > 0 else 0,
            'results': results
        }
    
    def print_results(self, results: Dict[str, Any]) -> None:
        """
        Print test results in agent-friendly format.
        Explicit output - no hidden formatting logic.
        """
        print(f"\n{'='*60}")
        print(f"TEST RESULTS SUMMARY")
        print(f"{'='*60}")
        print(f"Total Time: {results['total_time']:.2f} seconds")
        print(f"Total Files: {results['total_files']}")
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['total_passed']}")
        print(f"Failed: {results['total_failed']}")
        print(f"Success Rate: {results['success_rate']:.1%}")
        print(f"{'='*60}")
        
        # Print individual file results
        for result in results['results']:
            print(f"\n{'-'*40}")
            print(f"FILE: {result['file']}")
            
            if result['status'] == 'FILE_NOT_FOUND':
                print(f"  ❌ File not found: {result['error']}")
                continue
            
            if result['status'] == 'IMPORT_ERROR':
                print(f"  ❌ Import error: {result['error']}")
                print(f"  Traceback: {result['traceback']}")
                continue
            
            if result['status'] == 'COMPLETED':
                print(f"  Tests: {result['total_tests']}")
                print(f"  Passed: {result['passed_tests']}")
                print(f"  Failed: {result['failed_tests']}")
                
                # Print individual test results
                for test in result['tests']:
                    if test['status'] == 'PASSED':
                        print(f"    ✓ {test['name']} ({test['execution_time']:.3f}s)")
                    else:
                        print(f"    ✗ {test['name']}")
                        print(f"      Error: {test['error']}")
                        if test['traceback']:
                            print(f"      Traceback: {test['traceback']}")
        
        print(f"\n{'='*60}")
        print(f"OVERALL RESULT: {'✅ SUCCESS' if results['success_rate'] >= 0.9 else '❌ FAILURE'}")
        print(f"{'='*60}")
    
    def print_agent_summary(self, results: Dict[str, Any]) -> None:
        """
        Print agent-friendly summary.
        Focused on agent productivity metrics.
        """
        print(f"\n{'='*60}")
        print(f"AGENT PRODUCTIVITY SUMMARY")
        print(f"{'='*60}")
        
        # Calculate agent metrics
        tests_per_second = results['total_tests'] / results['total_time'] if results['total_time'] > 0 else 0
        files_per_second = results['total_files'] / results['total_time'] if results['total_time'] > 0 else 0
        
        print(f"Execution Speed:")
        print(f"  Tests per second: {tests_per_second:.1f}")
        print(f"  Files per second: {files_per_second:.1f}")
        print(f"  Average time per test: {results['total_time'] / results['total_tests']:.3f}s")
        
        print(f"\nQuality Metrics:")
        print(f"  Success rate: {results['success_rate']:.1%}")
        print(f"  Failed tests: {results['total_failed']}")
        print(f"  Error rate: {results['total_failed'] / results['total_tests']:.1%}")
        
        # Agent recommendations
        print(f"\nAgent Recommendations:")
        if results['success_rate'] >= 0.95:
            print(f"  ✅ Excellent test quality")
        elif results['success_rate'] >= 0.90:
            print(f"  ⚠️  Good test quality, consider fixing failing tests")
        else:
            print(f"  ❌ Poor test quality, need to fix many failing tests")
        
        if tests_per_second >= 10:
            print(f"  ✅ Excellent test execution speed")
        elif tests_per_second >= 5:
            print(f"  ⚠️  Good test execution speed")
        else:
            print(f"  ❌ Slow test execution, consider optimization")
        
        print(f"{'='*60}")


class ContractValidator:
    """
    Simple function contract validator for agents.
    Explicit validation - no hidden analysis.
    """
    
    def __init__(self):
        self.validations = []
        self.passed = 0
        self.failed = 0
    
    def validate_function_contract(self, func: Callable) -> Dict[str, Any]:
        """
        Validate function contract meets agent standards.
        Explicit contract validation - no hidden rules.
        """
        signature = inspect.signature(func)
        docstring = inspect.getdoc(func)
        
        validation_result = {
            'function': func.__name__,
            'signature_valid': True,
            'docstring_valid': True,
            'type_hints_valid': True,
            'issues': [],
            'status': 'PASSED'
        }
        
        # Check docstring presence
        if not docstring:
            validation_result['docstring_valid'] = False
            validation_result['issues'].append("Missing docstring")
        
        # Check parameter documentation
        if docstring:
            params = signature.parameters
            for param_name in params:
                if f"{param_name}:" not in docstring and "Args:" in docstring:
                    validation_result['issues'].append(f"Parameter {param_name} not documented")
        
        # Check return documentation
        if docstring and "Returns:" not in docstring:
            validation_result['issues'].append("Return value not documented")
        
        # Check type hints
        for param_name, param in signature.parameters.items():
            if param.annotation == inspect.Parameter.empty:
                validation_result['type_hints_valid'] = False
                validation_result['issues'].append(f"Parameter {param_name} missing type hint")
        
        if signature.return_annotation == inspect.Signature.empty:
            validation_result['type_hints_valid'] = False
            validation_result['issues'].append("Return type missing type hint")
        
        # Set status based on issues
        if validation_result['issues']:
            validation_result['status'] = 'FAILED'
            self.failed += 1
        else:
            self.passed += 1
        
        return validation_result
    
    def validate_module_contracts(self, module) -> Dict[str, Any]:
        """
        Validate all function contracts in module.
        Explicit module validation - no hidden discovery.
        """
        functions = [
            getattr(module, name) 
            for name in dir(module) 
            if inspect.isfunction(getattr(module, name))
        ]
        
        # Validate public functions only
        public_functions = [f for f in functions if not f.__name__.startswith('_')]
        
        validation_results = []
        for func in public_functions:
            result = self.validate_function_contract(func)
            validation_results.append(result)
        
        return {
            'module': module.__name__,
            'functions': validation_results,
            'total_functions': len(public_functions),
            'passed_validations': self.passed,
            'failed_validations': self.failed
        }


def main():
    """
    Main entry point for agent test runner.
    Explicit main function - no hidden command parsing.
    """
    # Parse command line arguments (explicit)
    if len(sys.argv) > 1:
        test_pattern = sys.argv[1]
    else:
        test_pattern = "test_*.py"
    
    print(f"Running tests with pattern: {test_pattern}")
    
    # Create test runner
    runner = AgentTestRunner()
    
    # Run tests
    results = runner.run_all_tests(test_pattern)
    
    # Print results
    runner.print_results(results)
    runner.print_agent_summary(results)
    
    # Exit with appropriate code
    if results['success_rate'] >= 0.9:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()