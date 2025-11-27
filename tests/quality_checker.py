"""
Quality checker for all RPGSim systems
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any


class QualityChecker:
    """Runs all quality checks on the project"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.results = {}
    
    def run_all_checks(self, verbose: bool = False) -> bool:
        """Run all quality checks and return overall success"""
        checks = [
            self._run_bdd_tests,
            self._run_unit_tests,
            self._run_property_tests,
            self._run_pylint,
            self._check_module_sizes,
            self._check_imports
        ]
        
        all_passed = True
        
        for check_func in checks:
            try:
                passed = check_func(verbose)
                self.results[check_func.__name__] = passed
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"❌ {check_func.__name__} failed: {e}")
                self.results[check_func.__name__] = False
                all_passed = False
        
        return all_passed
    
    def run_system_check(self, system_name: str, verbose: bool = False) -> bool:
        """Run checks for a specific system"""
        system_checks = [
            lambda v: self._run_bdd_tests_for_system(system_name, v),
            lambda v: self._run_unit_tests_for_system(system_name, v),
            lambda v: self._run_pylint_for_system(system_name, v)
        ]
        
        all_passed = True
        
        for check_func in system_checks:
            try:
                passed = check_func(verbose)
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"❌ System check failed: {e}")
                all_passed = False
        
        return all_passed
    
    def _run_bdd_tests(self, verbose: bool = False) -> bool:
        """Run all BDD tests"""
        if verbose:
            print("🧪 Running BDD tests...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "behave", "features/"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if verbose or result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ BDD test error: {e}")
            return False
    
    def _run_bdd_tests_for_system(self, system_name: str, verbose: bool = False) -> bool:
        """Run BDD tests for specific system"""
        if verbose:
            print(f"🧪 Running BDD tests for {system_name}...")
        
        feature_files = {
            "character": "character_creation.feature",
            "world": "world_exploration.feature",
            "combat": "combat_system.feature",
            "shop": "shop_system.feature"
        }
        
        feature_file = feature_files.get(system_name)
        if not feature_file:
            print(f"⚠️  No BDD tests found for {system_name}")
            return True
        
        try:
            result = subprocess.run(
                ["python", "-m", "behave", f"features/{feature_file}"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if verbose or result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ BDD test error: {e}")
            return False
    
    def _run_unit_tests(self, verbose: bool = False) -> bool:
        """Run all unit tests with coverage"""
        if verbose:
            print("🔬 Running unit tests...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/unit/", 
                 "--cov=core.systems", "--cov-report=term-missing", "--cov-fail-under=90"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if verbose or result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Unit test error: {e}")
            return False
    
    def _run_unit_tests_for_system(self, system_name: str, verbose: bool = False) -> bool:
        """Run unit tests for specific system"""
        if verbose:
            print(f"🔬 Running unit tests for {system_name}...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", f"tests/unit/test_{system_name}.py",
                 f"--cov=core.systems.{system_name}", "--cov-report=term-missing"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if verbose or result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Unit test error: {e}")
            return False
    
    def _run_property_tests(self, verbose: bool = False) -> bool:
        """Run property-based tests"""
        if verbose:
            print("🔍 Running property tests...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/property/"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if verbose or result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Property test error: {e}")
            return False
    
    def _run_pylint(self, verbose: bool = False) -> bool:
        """Run Pylint on all systems"""
        if verbose:
            print("📏 Running Pylint...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "pylint", "core/systems/", "--score=yes", "--fail-under=10.0"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if verbose or result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Pylint error: {e}")
            return False
    
    def _run_pylint_for_system(self, system_name: str, verbose: bool = False) -> bool:
        """Run Pylint on specific system"""
        if verbose:
            print(f"📏 Running Pylint on {system_name}...")
        
        system_path = f"core/systems/{system_name}.py"
        if not Path(self.project_root / system_path).exists():
            system_path = f"core/systems/{system_name}/"  # Package
        
        try:
            result = subprocess.run(
                ["python", "-m", "pylint", system_path, "--score=yes", "--fail-under=10.0"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if verbose or result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Pylint error: {e}")
            return False
    
    def _check_module_sizes(self, verbose: bool = False) -> bool:
        """Check that no module exceeds 1000 lines"""
        if verbose:
            print("📐 Checking module sizes...")
        
        all_valid = True
        
        for system_file in Path(self.project_root / "core/systems").glob("*.py"):
            if system_file.name == "__init__.py":
                continue
                
            line_count = self._count_lines(system_file)
            if line_count > 1000:
                print(f"❌ {system_file.name}: {line_count} lines (exceeds 1000)")
                all_valid = False
            elif verbose:
                print(f"✅ {system_file.name}: {line_count} lines")
        
        return all_valid
    
    def _count_lines(self, file_path: Path) -> int:
        """Count non-empty lines in file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0
    
    def _check_imports(self, verbose: bool = False) -> bool:
        """Check that all imports are valid"""
        if verbose:
            print("🔗 Checking imports...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "core", "--check"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if verbose or result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Import check error: {e}")
            return False


def run_quality_checks(system_only: str = None, verbose: bool = False) -> bool:
    """Run quality checks - main entry point"""
    checker = QualityChecker()
    
    if system_only:
        return checker.run_system_check(system_only, verbose)
    else:
        return checker.run_all_checks(verbose)


if __name__ == "__main__":
    import sys
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    system_only = None
    
    for arg in sys.argv:
        if arg.startswith("--system="):
            system_only = arg.split("=")[1]
    
    success = run_quality_checks(system_only, verbose)
    sys.exit(0 if success else 1)