#!/usr/bin/env python
"""
Setup script for Unified E-Commerce System
Handles initial configuration and dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and return success status"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        return False

def install_requirements():
    """Install Python dependencies"""
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def verify_python_version():
    """Check Python version"""
    print(f"\n{'='*60}")
    print("🐍 Checking Python Version")
    print(f"{'='*60}")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version OK (3.8+)")
        return True
    else:
        print("❌ Python 3.8 or higher required")
        return False

def create_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = Path(__file__).parent.parent
    print(f"\n{'='*60}")
    print("📁 Setting up directories")
    print(f"{'='*60}")
    
    print(f"Data directory: {data_dir}")
    print(f"App directory: {Path(__file__).parent}")
    
    # Check for CSV files
    csv_files = list(data_dir.glob('*.csv'))
    if csv_files:
        print(f"✅ Found {len(csv_files)} CSV file(s)")
    else:
        print("⚠️  No CSV files found in data directory")
        print("   You can:")
        print("   1. Place your CSV files in the parent directory")
        print("   2. Run: python test_utils.py --generate")

def generate_sample_data():
    """Ask if user wants to generate sample data"""
    print(f"\n{'='*60}")
    print("📊 Sample Data Generation")
    print(f"{'='*60}")
    
    response = input("\nNo CSV files found. Generate sample data? (y/n): ").strip().lower()
    
    if response == 'y':
        run_command(
            f"{sys.executable} test_utils.py --generate",
            "Generating sample data files"
        )
        return True
    else:
        print("⚠️  Skipping sample data generation")
        print("   Place your CSV files in the parent directory before running the app")
        return False

def test_imports():
    """Test critical imports"""
    print(f"\n{'='*60}")
    print("✅ Testing imports")
    print(f"{'='*60}")
    
    critical_modules = [
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('sklearn', 'Scikit-learn'),
        ('xgboost', 'XGBoost'),
        ('prophet', 'Prophet'),
    ]
    
    all_ok = True
    for module_name, display_name in critical_modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name}")
            all_ok = False
    
    return all_ok

def main():
    """Run setup"""
    print("""
    
    ╔══════════════════════════════════════════════════════════╗
    ║   Unified E-Commerce System - Setup Wizard              ║
    ║   Version 1.0.0                                          ║
    ╚══════════════════════════════════════════════════════════╝
    
    """)
    
    # Check Python version
    if not verify_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install dependencies")
        print("Run manually: pip install -r requirements.txt")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n⚠️  Some packages failed to import")
        print("This may be normal on first run - dependencies are being installed")
    
    # Check data files
    create_data_directory()
    
    # Check for CSV files and ask to generate if needed
    data_dir = Path(__file__).parent.parent
    csv_files = list(data_dir.glob('*.csv'))
    
    if not csv_files:
        generate_sample_data()
    
    # Setup complete
    print(f"\n{'='*60}")
    print("🎉 Setup Complete!")
    print(f"{'='*60}")
    
    print("""
    
    Your Unified E-Commerce System is ready to use!
    
    To start the application, run:
    
        streamlit run app.py
    
    The app will open in your browser at http://localhost:8501
    
    For more information, see:
    - README.md       (Complete documentation)
    - QUICKSTART.md   (Quick start guide)
    - config.py       (Configuration options)
    
    """)
    
    # Ask to run app
    response = input("Would you like to start the app now? (y/n): ").strip().lower()
    if response == 'y':
        print("\n🚀 Starting application...\n")
        os.system(f"{sys.executable} -m streamlit run app.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
