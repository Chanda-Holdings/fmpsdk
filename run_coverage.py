#!/usr/bin/env python3
"""
Script to run coverage analysis for specific modules while avoiding import conflicts.
"""
import sys
import os
import subprocess
import tempfile

def run_coverage_analysis():
    """Run coverage analysis for the target modules."""
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Get the virtual environment python path
    venv_python = os.path.join(project_dir, ".venv", "bin", "python")
    
    # Create a temporary script that imports and runs the tests
    test_script_content = '''
import sys
import os
sys.path.insert(0, "/Users/yushrajkapoor/Desktop/Python Libraries/fmpsdk")

# Import the modules we want to analyze
import fmpsdk.institutional_fund
import fmpsdk.senate  
import fmpsdk.mutual_funds

# Import pytest and run the tests
import pytest

# Run the specific test files
result = pytest.main([
    "tests/test_institutional_fund.py",
    "tests/test_senate.py", 
    "tests/test_mutual_funds.py",
    "-v"
])
sys.exit(result)
'''
    
    # Write the test script to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script_content)
        temp_script = f.name
    
    try:
        # Run coverage with the temporary script
        cmd = [
            venv_python, "-m", "coverage", "run", 
            "--source=fmpsdk.institutional_fund,fmpsdk.senate,fmpsdk.mutual_funds",
            temp_script
        ]
        
        print("Running coverage analysis...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Tests completed successfully. Generating coverage report...")
            
            # Generate the coverage report
            report_cmd = [venv_python, "-m", "coverage", "report", "-m"]
            report_result = subprocess.run(report_cmd, capture_output=True, text=True)
            
            print("Coverage Report:")
            print("=" * 50)
            print(report_result.stdout)
            
            if report_result.stderr:
                print("Coverage Warnings/Errors:")
                print(report_result.stderr)
                
        else:
            print("Test execution failed:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            
    finally:
        # Clean up the temporary script
        os.unlink(temp_script)

if __name__ == "__main__":
    run_coverage_analysis()
