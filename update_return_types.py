#!/usr/bin/env python3
"""
Script to automatically update return types in fmpsdk files based on model registry
"""

import os
import re
import sys
from pathlib import Path

# Add the fmpsdk directory to the path so we can import the model registry
sys.path.insert(0, 'fmpsdk')

from fmpsdk.model_registry import ENDPOINT_MODEL_MAP

# Files to update (excluding model_registry.py, models.py, settings.py, etc.)
FILES_TO_UPDATE = [
    'general.py',
    'calendar.py', 
    'company_valuation.py',
    'technical_indicators.py',
    'news.py',
    'senate.py',
    'insider_trading.py',
    'alternative_data.py',
    'cryptocurrencies.py',
    'forex.py',
    'etf.py',
    'mutual_funds.py',
    'market_indexes.py',
    'stock_market.py',
    'stock_time_series.py',
    'bulk.py',
    'institutional_fund.py',
    'commodities.py',
    'economic_indicators.py',
    'shares_float.py',
    'euronext.py',
    'tsx.py'
]

def get_model_imports_needed(file_path, endpoint_map):
    """Get the model imports needed for a file based on its endpoint functions"""
    models_needed = set()
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all function definitions with @parse_response decorator
    function_pattern = r'@parse_response\s+def\s+(\w+)\s*\('
    functions = re.findall(function_pattern, content)
    
    for func_name in functions:
        if func_name in endpoint_map:
            model_class = endpoint_map[func_name]
            models_needed.add(model_class.__name__)
    
    return sorted(models_needed)

def update_imports_in_file(file_path, models_needed):
    """Update the imports in a file to include the needed model classes"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if models are already imported
    if 'from .models import' in content:
        # Update existing import
        import_pattern = r'from \.models import \((.*?)\)'
        match = re.search(import_pattern, content, re.DOTALL)
        if match:
            # Extract current imports and add new ones
            current_imports = match.group(1)
            all_imports = set()
            for line in current_imports.split('\n'):
                line = line.strip().rstrip(',')
                if line:
                    all_imports.add(line)
            all_imports.update(models_needed)
            
            # Create new import block
            new_imports = ',\n    '.join(sorted(all_imports))
            new_import_block = f'from .models import (\n    {new_imports},\n)'
            content = re.sub(import_pattern, new_import_block, content, flags=re.DOTALL)
        else:
            # Single line import, convert to multi-line
            import_pattern = r'from \.models import ([^\n]+)'
            match = re.search(import_pattern, content)
            if match:
                current_imports = [imp.strip() for imp in match.group(1).split(',')]
                all_imports = set(current_imports + models_needed)
                new_imports = ',\n    '.join(sorted(all_imports))
                new_import_block = f'from .models import (\n    {new_imports},\n)'
                content = re.sub(import_pattern, new_import_block, content)
    else:
        # Add new import after existing imports
        utils_import_pattern = r'(from \.utils import parse_response\n)'
        if re.search(utils_import_pattern, content):
            new_imports = ',\n    '.join(models_needed)
            new_import_block = f'from .models import (\n    {new_imports},\n)\n'
            content = re.sub(utils_import_pattern, f'\\1{new_import_block}', content)
    
    with open(file_path, 'w') as f:
        f.write(content)

def update_function_return_types(file_path, endpoint_map):
    """Update function return types based on the endpoint map"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    for func_name, model_class in endpoint_map.items():
        # Pattern to match function definition with return type
        pattern = rf'(@parse_response\s+def\s+{re.escape(func_name)}\s*\([^)]*\)\s*->\s*)typing\.Optional\[typing\.List\[typing\.Dict\]\]:'
        replacement = f'\\g<1>{model_class.__name__}:'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Also handle other typing patterns
        pattern2 = rf'(@parse_response\s+def\s+{re.escape(func_name)}\s*\([^)]*\)\s*->\s*)typing\.List\[typing\.Dict\]:'
        content = re.sub(pattern2, replacement, content, flags=re.DOTALL)
        
        pattern3 = rf'(@parse_response\s+def\s+{re.escape(func_name)}\s*\([^)]*\)\s*->\s*)typing\.Union\[typing\.List\[typing\.Dict\],\s*None\]:'
        content = re.sub(pattern3, replacement, content, flags=re.DOTALL)
    
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    """Main function to update all files"""
    base_dir = Path('fmpsdk')
    
    for filename in FILES_TO_UPDATE:
        file_path = base_dir / filename
        if not file_path.exists():
            print(f"Warning: {file_path} does not exist, skipping...")
            continue
            
        print(f"Processing {filename}...")
        
        # Get needed models for this file
        models_needed = get_model_imports_needed(file_path, ENDPOINT_MODEL_MAP)
        
        if models_needed:
            # Update imports
            update_imports_in_file(file_path, models_needed)
            
            # Update function return types
            update_function_return_types(file_path, ENDPOINT_MODEL_MAP)
            
            print(f"  Updated {len(models_needed)} model imports: {', '.join(models_needed)}")
        else:
            print(f"  No models needed for {filename}")

if __name__ == '__main__':
    main()
