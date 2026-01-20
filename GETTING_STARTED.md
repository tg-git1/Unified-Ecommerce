# 🚀 Getting Started - Unified E-Commerce System

Welcome! This guide will help you get the application running in minutes.

---

## ⚡ Quick Start (2 Minutes)

### For Windows Users

1. **Open Command Prompt/PowerShell**
   ```
   cd unified_ecommerce_app
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```
   streamlit run app.py
   ```

Your app will open at http://localhost:8501

### For Mac/Linux Users

1. **Open Terminal**
   ```bash
   cd unified_ecommerce_app
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```bash
   streamlit run app.py
   ```

---

## 📋 Pre-requisites

### Required
- Python 3.8 or higher
- pip (Python package manager)
- 4 GB RAM minimum
- 500 MB free disk space

### Optional
- Git (for version control)
- Docker (for containerized deployment)

### Check Your Python Version
```bash
python --version
```

Should show Python 3.8+

---

## 📥 Installation Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Streamlit (web framework)
- Pandas (data processing)
- XGBoost (ML model)
- Prophet (forecasting)
- Plotly (charts)
- And more...

### Step 2: Prepare Data (Choose One)

#### Option A: Use Sample Data (Recommended for Testing)
```bash
python test_utils.py --generate
```

This creates sample CSV files automatically.

#### Option B: Use Your Own Data
Place these CSV files in the parent directory:
- `apple_iphone.csv`
- `nike_revolution.csv`
- `cricket bat.csv`
- `prestige_induction.csv`
- `levis_mens_cotton_tshirt.csv`
- `cross_platform_products.csv`
- `model training.csv`

See README.md for CSV format details.

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will:
1. Start a local server
2. Open your default browser
3. Show the home page

**That's it! You're ready to use the app.** 🎉

---

## 🎮 First Time Usage

### Step 1: Enter Your Location
- See a text input for your 6-digit PIN code
- Example: 560001 (Bangalore)
- Click "Confirm Location" button

### Step 2: Select a Product
- See 5 product options
- Click on any product to analyze

### Step 3: View Analysis
The app shows 5 analysis tabs:

1. **📈 Sales Forecast**
   - 90-day sales prediction
   - Platform trends
   - Growth indicators

2. **💰 Price Analysis**
   - Price predictions for 3 months
   - Platform comparison
   - Stability metrics

3. **⚠️ Fake Reviews**
   - Percentage of suspicious reviews
   - Platform-wise breakdown
   - Example suspicious reviews

4. **🌱 Eco-Friendliness**
   - Carbon emissions rating
   - Color-coded (Green/Yellow/Orange/Red)
   - Most eco-friendly platform

5. **⭐ Overall Score**
   - 0-100 rating
   - Score breakdown
   - Recommendation

---

## 🆘 Troubleshooting

### Issue: "Command not found: python"
**Solution:**
- Windows: Use `py` instead of `python`
- Mac/Linux: Try `python3` instead of `python`

### Issue: "No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
```

Or reinstall all:
```bash
pip install -r requirements.txt
```

### Issue: "CSV files not found"
**Solution:**
Option 1: Generate sample data
```bash
python test_utils.py --generate
```

Option 2: Place your CSV files in the parent directory

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

Use port 8502 instead.

### Issue: "Prophet installation failed"
**Solution (Windows):**
```bash
pip install --upgrade scikit-learn
pip install prophet
```

---

## 📂 Expected File Structure

After installation, you should have:

```
unified_ecommerce_app/
├── app.py
├── config.py
├── requirements.txt
├── setup.py
├── test_utils.py
├── modules/
│   ├── data_loader.py
│   ├── fake_review_detector.py
│   ├── forecasting.py
│   ├── carbon_emissions.py
│   └── product_score.py
├── README.md
├── QUICKSTART.md
└── ... (other documentation files)

CSV Files (should be in parent directory):
apple_iphone.csv
nike_revolution.csv
cricket bat.csv
prestige_induction.csv
levis_mens_cotton_tshirt.csv
cross_platform_products.csv
model training.csv
```

---

## 🔧 Using the Setup Wizard (Alternative)

Instead of manual steps, you can use the interactive setup:

```bash
python setup.py
```

This will:
1. Check Python version
2. Install dependencies
3. Check imports
4. Setup data directory
5. Ask to generate sample data
6. Ask to start the app

---

## 🐳 Running with Docker (Advanced)

If you have Docker installed:

```bash
docker-compose up
```

The app will be available at http://localhost:8501

---

## 💡 Tips for Best Experience

1. **Use Chrome or Firefox** for best compatibility
2. **Place CSV in correct location** for data to load
3. **Run setup.py once** if you're unsure about dependencies
4. **Generate sample data first** if you don't have real data
5. **Use realistic PIN codes** for accurate distance calculations

---

## 📚 Learn More

- **README.md** - Complete documentation
- **QUICKSTART.md** - More detailed quick start
- **DEPLOYMENT.md** - Deploy to cloud
- **config.py** - Configuration options
- **PROJECT_SUMMARY.md** - Project overview

---

## 🎯 Common Tasks

### Generate Sample Data
```bash
python test_utils.py --generate
```

### Validate Data Files
```bash
python test_utils.py --validate
```

### Check All Dependencies
```bash
python test_utils.py --check-deps
```

### Run Everything (Setup + Test + Start)
```bash
python setup.py
```

---

## 🌐 Deploying to Cloud

After testing locally, deploy to:
- **Streamlit Cloud** (easiest, free)
- **Heroku** (simple)
- **Docker** (portable)
- **AWS EC2** (powerful)

See DEPLOYMENT.md for detailed guides.

---

## 📞 Need Help?

1. Check the **Troubleshooting** section above
2. Read **README.md** for detailed docs
3. Review CSV format in **QUICKSTART.md**
4. Check **test_utils.py** output for errors

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (no error messages)
- [ ] CSV files in correct location (parent directory)
- [ ] App starts without errors
- [ ] Can enter PIN code
- [ ] Can select a product
- [ ] All 5 analysis tabs visible
- [ ] Charts load and display

---

## 🎉 Ready to Go!

You're all set! Here's what to do next:

1. **Run the app**: `streamlit run app.py`
2. **Enter a PIN code**: (e.g., 560001)
3. **Select a product**: Click any product button
4. **Explore the analysis**: Check each tab
5. **Read the docs**: Learn more features

**Enjoy exploring the Unified E-Commerce System!** 🚀

---

## 📅 Version Info

- **Version**: 1.0.0
- **Released**: January 2026
- **Status**: Production Ready ✅
- **Python**: 3.8+

---

**Happy Shopping! 🛍️**
