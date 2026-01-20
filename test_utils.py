"""
Utility script for testing and validating the Unified E-Commerce System
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

def generate_sample_data(output_dir=None):
    """Generate sample CSV files for testing"""
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("📊 Generating sample data files...")
    
    # Sample products data
    products = {
        'apple_iphone.csv': {
            'product': 'Apple iPhone',
            'price_range': (40000, 60000)
        },
        'nike_revolution.csv': {
            'product': 'Nike Revolution',
            'price_range': (2000, 4000)
        },
        'cricket bat.csv': {
            'product': 'Cricket Bat',
            'price_range': (1000, 5000)
        },
        'prestige_induction.csv': {
            'product': 'Prestige Induction',
            'price_range': (3000, 6000)
        },
        'levis_mens_cotton_tshirt.csv': {
            'product': 'Levis Mens Cotton T-Shirt',
            'price_range': (500, 2000)
        }
    }
    
    platforms = ['Amazon', 'Flipkart', 'eBay']
    
    for filename, config in products.items():
        np.random.seed(42)
        
        n_reviews = 100
        dates = pd.date_range(start='2023-06-01', periods=n_reviews, freq='D')
        
        data = {
            'review_text': np.random.choice([
                'Excellent product, highly recommended!',
                'Great quality and fast delivery',
                'Not as described in the listing',
                'Buy now! Limited time offer!!!',
                'Amazing value for money',
                'Disappointed with the quality',
                'BEST DEAL EVER!!!',
                'Good product, average service',
                'Worth every penny',
                'Cheap quality product'
            ], n_reviews),
            'platform': np.random.choice(platforms, n_reviews),
            'date': dates,
            'price': np.random.randint(config['price_range'][0], config['price_range'][1], n_reviews),
            'rating': np.random.randint(1, 6, n_reviews),
            'sales': np.random.randint(10, 100, n_reviews)
        }
        
        df = pd.DataFrame(data)
        filepath = output_dir / filename
        df.to_csv(filepath, index=False)
        print(f"✅ Created {filename}")
    
    # Create model training data
    training_data = {
        'review_text': [
            'Excellent product, highly recommended!',
            'Buy NOW!!! LIMITED TIME!!!',
            'Great quality and fast delivery',
            'DON\'T MISS THIS OFFER!!!',
            'Not as described in the listing',
            'Amazing value for money',
            'Click here for more info!!!',
            'Good product, average service',
            'Worth every penny',
            'Cheap quality product',
            'Act fast, only 2 left!!!',
            'Outstanding quality',
            'Save $$$$ now!!!!',
            'Best ever seen before!',
            'Not recommended'
        ] * 6,  # Repeat for more data
        'label': [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0] * 6
    }
    
    df_training = pd.DataFrame(training_data)
    df_training.to_csv(output_dir / 'model training.csv', index=False)
    print("✅ Created model training.csv")
    
    # Create cross-platform products data
    cross_platform = {
        'product': ['Apple iPhone'] * 12 + ['Nike Revolution'] * 12,
        'platform': ['Amazon'] * 4 + ['Flipkart'] * 4 + ['eBay'] * 4 + ['Amazon'] * 4 + ['Flipkart'] * 4 + ['eBay'] * 4,
        'date': pd.date_range(start='2023-06-01', periods=12).tolist() * 2,
        'price': np.random.randint(40000, 60000, 12).tolist() + np.random.randint(2000, 4000, 12).tolist(),
        'sales': np.random.randint(50, 200, 12).tolist() + np.random.randint(10, 50, 12).tolist(),
        'warehouse_pin': ['110001'] * 4 + ['560001'] * 4 + ['400001'] * 4 + ['110001'] * 4 + ['560001'] * 4 + ['400001'] * 4
    }
    
    df_cross = pd.DataFrame(cross_platform)
    df_cross.to_csv(output_dir / 'cross_platform_products.csv', index=False)
    print("✅ Created cross_platform_products.csv")
    
    print("\n✅ All sample data files created successfully!")
    print(f"📁 Files saved to: {output_dir}")

def validate_data_files(data_dir=None):
    """Validate that all required CSV files exist and have correct format"""
    
    if data_dir is None:
        data_dir = Path(__file__).parent.parent
    
    data_dir = Path(data_dir)
    
    print("🔍 Validating data files...\n")
    
    required_files = [
        'apple_iphone.csv',
        'nike_revolution.csv',
        'cricket bat.csv',
        'prestige_induction.csv',
        'levis_mens_cotton_tshirt.csv',
        'cross_platform_products.csv',
        'model training.csv'
    ]
    
    missing_files = []
    valid_files = []
    
    for filename in required_files:
        filepath = data_dir / filename
        
        if not filepath.exists():
            missing_files.append(filename)
            print(f"❌ Missing: {filename}")
        else:
            try:
                df = pd.read_csv(filepath)
                valid_files.append(filename)
                print(f"✅ {filename} ({len(df)} rows, {len(df.columns)} columns)")
            except Exception as e:
                print(f"⚠️  {filename} - Error reading file: {str(e)}")
    
    print("\n" + "="*50)
    print(f"Summary: {len(valid_files)} valid, {len(missing_files)} missing")
    print("="*50)
    
    if missing_files:
        print("\n⚠️  Missing files:")
        for f in missing_files:
            print(f"  - {f}")
        print("\n💡 Run 'python test_utils.py --generate' to create sample files")
    else:
        print("\n✅ All data files present!")

def check_dependencies():
    """Check if all required packages are installed"""
    
    print("🔧 Checking dependencies...\n")
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'sklearn',
        'xgboost',
        'prophet',
        'matplotlib',
        'plotly',
        'seaborn',
        'pytz'
    ]
    
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            installed_packages.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    print("\n" + "="*50)
    print(f"Summary: {len(installed_packages)} installed, {len(missing_packages)} missing")
    print("="*50)
    
    if missing_packages:
        print("\n⚠️  Missing packages:")
        for p in missing_packages:
            print(f"  - {p}")
        print("\n💡 Install missing packages with:")
        print("  pip install -r requirements.txt")
    else:
        print("\n✅ All dependencies installed!")

def test_models():
    """Quick test of ML models"""
    
    print("\n🧪 Testing ML models...\n")
    
    try:
        print("Testing XGBoost fake review detector...")
        sys.path.insert(0, str(Path(__file__).parent))
        from modules.fake_review_detector import FakeReviewDetector
        
        detector = FakeReviewDetector()
        test_reviews = [
            "Great product!",
            "Buy now!!!",
            "Not satisfied"
        ]
        print(f"✅ XGBoost detector loaded successfully")
        
    except Exception as e:
        print(f"❌ Error loading XGBoost: {str(e)}")
    
    try:
        print("Testing Prophet forecasting...")
        from modules.forecasting import PriceForecastor, SalesForecastor
        
        price_forecaster = PriceForecastor('Test Product')
        sales_forecaster = SalesForecastor('Test Product')
        print(f"✅ Prophet forecasters loaded successfully")
        
    except Exception as e:
        print(f"❌ Error loading Prophet: {str(e)}")
    
    try:
        print("Testing carbon emissions calculator...")
        from modules.carbon_emissions import CarbonEmissionsCalculator
        
        calc = CarbonEmissionsCalculator()
        emissions = calc.calculate_emissions('110001', '560001', 1.0, 'road')
        print(f"✅ Carbon calculator working (Test: {emissions:.3f} kg CO2)")
        
    except Exception as e:
        print(f"❌ Error with carbon calculator: {str(e)}")
    
    print("\n✅ Model tests completed!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified E-Commerce System Utilities")
    parser.add_argument('--generate', action='store_true', help='Generate sample data files')
    parser.add_argument('--validate', action='store_true', help='Validate data files')
    parser.add_argument('--check-deps', action='store_true', help='Check dependencies')
    parser.add_argument('--test-models', action='store_true', help='Test ML models')
    parser.add_argument('--all', action='store_true', help='Run all checks')
    parser.add_argument('--data-dir', type=str, help='Path to data directory')
    
    args = parser.parse_args()
    
    if args.all:
        check_dependencies()
        print("\n" + "="*50 + "\n")
        validate_data_files(args.data_dir)
        print("\n" + "="*50 + "\n")
        test_models()
    else:
        if args.generate:
            generate_sample_data(args.data_dir)
        if args.validate:
            validate_data_files(args.data_dir)
        if args.check_deps:
            check_dependencies()
        if args.test_models:
            test_models()
        if not any([args.generate, args.validate, args.check_deps, args.test_models]):
            parser.print_help()
