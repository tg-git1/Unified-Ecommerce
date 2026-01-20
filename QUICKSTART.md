# Quick Start Guide - Unified E-Commerce System

## ⚡ 5-Minute Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Your Data Files
Ensure these CSV files are in the parent directory of `unified_ecommerce_app`:
- `apple_iphone.csv`
- `nike_revolution.csv`
- `cricket bat.csv`
- `prestige_induction.csv`
- `levis_mens_cotton_tshirt.csv`
- `cross_platform_products.csv`
- `model training.csv`

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 🎯 First Use Steps

1. **Enter Your PIN Code**
   - Home page will ask for your 6-digit PIN code
   - Example: 560001 (Bangalore)
   - Click "Confirm Location"

2. **Select a Product**
   - Choose from 5 available products
   - Click the product button

3. **View Analysis**
   - **Sales Forecast**: See predicted sales for 90 days
   - **Price Analysis**: Check price trends and comparisons
   - **Fake Reviews**: Identify suspicious reviews
   - **Eco-Friendliness**: Check carbon emissions by platform
   - **Overall Score**: Get comprehensive rating and recommendation

---

## 🔧 Expected CSV Structure

### Product Review Files (apple_iphone.csv, etc.)
```
| review_text          | platform  | date       | price | sales |
|---                   |---        |---         |---    |---    |
| "Great phone!"       | Amazon    | 2024-01-15 | 50000 | 45    |
| "Good value"        | Flipkart  | 2024-01-14 | 49000 | 38    |
```

**Required columns (at least one from each group):**
- Review text: `review_text`, `text`, `review`, `content`
- Platform: `platform`, `marketplace`, `seller`
- Date: `date`, `timestamp`, `datetime`
- Optional Price: `price`, `current_price`, `selling_price`
- Optional Sales: `sales`, `quantity`, `units_sold`

### Model Training File (model training.csv)
```
| review_text              | label |
|---                       |---    |
| "Buy now!!!!"            | 1     |
| "Excellent quality"      | 0     |
| "LIMITED TIME OFFER!!!"  | 1     |
```

**Required columns:**
- `review_text` (or `text`, `review`, `content`)
- `label` (0=real review, 1=fake review)

### Cross-Platform Data (cross_platform_products.csv)
```
| platform  | pin_code | price | date       | sales |
|---        |---       |---    |---         |---    |
| Amazon    | 110001   | 50000 | 2024-01-15 | 100   |
| Flipkart  | 560001   | 49000 | 2024-01-15 | 85    |
```

**Required columns:**
- Platform identification
- Pin code for warehouse location
- Price and date data
- Sales/quantity data

---

## 🚀 Docker Deployment (Optional)

### Build and Run with Docker
```bash
# Build image
docker build -t ecommerce-app .

# Run container
docker run -p 8501:8501 ecommerce-app
```

### Or use Docker Compose
```bash
docker-compose up
```

---

## 🌐 Cloud Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect your repo
4. Choose `app.py` as main file
5. Deploy!

### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
git push heroku main
```

### AWS
```bash
# Create EC2 instance (Ubuntu)
# SSH into instance
# Install Python and Git
# Clone repository
# Install dependencies
# Run: streamlit run app.py --server.port 80
```

---

## 🔍 Troubleshooting

### Issue: CSV files not found
**Fix**: Move CSV files to parent directory or update path in `data_loader.py`

### Issue: Module import error
**Fix**: Run `pip install -r requirements.txt`

### Issue: Prophet/XGBoost installation fails
**Fix**: On Windows, use: `pip install --upgrade scikit-learn xgboost`

### Issue: Port 8501 already in use
**Fix**: `streamlit run app.py --server.port 8502`

---

## 📊 Testing the System

### Test Data
If you don't have CSV files, the app will handle missing data gracefully:
- Forecasting will show placeholder messages
- Fake review detection will explain missing data
- Eco-friendliness will still calculate based on warehouse data

### Generate Sample Data
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Sample reviews
data = {
    'review_text': [
        'Great product!',
        'Not satisfied',
        'Buy now!!!',
        'Excellent quality',
        'Waste of money'
    ],
    'platform': ['Amazon', 'Flipkart', 'Amazon', 'eBay', 'Flipkart'],
    'date': pd.date_range(start='2024-01-01', periods=5),
    'price': [50000, 49000, 50000, 48000, 49000]
}

df = pd.DataFrame(data)
df.to_csv('apple_iphone.csv', index=False)
```

---

## 💡 Tips for Best Results

1. **Use Realistic Data**: More data = better forecasts
2. **Include Date Columns**: Required for Prophet forecasting
3. **Platform Consistency**: Use consistent platform names
4. **Fake Review Labels**: Ensure 0/1 labels in training data
5. **PIN Codes**: Use actual Indian PIN codes for accurate distance calculation

---

## 📱 Features Walkthrough

### Home Page
- Enter PIN code for location-based analysis
- Select from 5 featured products
- View feature highlights

### Product Details Page

#### Sales Forecast Tab
- 90-day sales prediction
- Platform-specific trends
- Growth/decline indicators

#### Price Analysis Tab
- 3-month price forecasts
- Historical trends
- Price stability metrics
- Platform comparison

#### Fake Reviews Tab
- Review authenticity analysis
- Percentage of fake reviews
- Platform-wise breakdown
- Examples of suspicious reviews

#### Eco-Friendliness Tab
- Carbon emissions calculation
- Distance-based analysis
- Color-coded ratings (Green/Yellow/Orange/Red)
- Most eco-friendly platform

#### Overall Score Tab
- Comprehensive product rating (0-100)
- Score breakdown by category
- Recommendation based on score
- Visualization of all metrics

---

## 🎨 Customization

### Change Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#YOUR_COLOR"
backgroundColor = "#YOUR_COLOR"
```

### Add More Products
Edit `config.py`:
```python
PRODUCTS = {
    'Your Product': {
        'file': 'your_product.csv',
        'category': 'Category',
        'icon': '🎯'
    }
}
```

### Adjust Scoring Weights
Edit `config.py`:
```python
SCORE_WEIGHTS = {
    'fake_reviews': 0.30,  # Increase if fake reviews are important
    'price_stability': 0.20,
    # ... others
}
```

---

## 📞 Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Prophet Docs**: https://facebook.github.io/prophet/
- **XGBoost Docs**: https://xgboost.readthedocs.io/
- **Pandas Docs**: https://pandas.pydata.org/docs/

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] CSV files placed in correct location
- [ ] App runs without errors (`streamlit run app.py`)
- [ ] PIN code input works
- [ ] Product selection works
- [ ] All tabs load (may take time on first run)
- [ ] Charts and metrics display correctly

---

**Ready to Go!** 🎉 Your Unified E-Commerce System is ready to use.
