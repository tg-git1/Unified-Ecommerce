# Unified E-Commerce System

A comprehensive e-commerce analysis platform built with Streamlit that provides intelligent insights for making better purchasing decisions across multiple platforms.

## 🎯 Features

### 1. **Fake Review Detection**
- XGBoost machine learning model trained on labeled reviews
- Identifies suspicious and fake reviews with confidence scores
- Platform-wise analysis showing percentage of fake reviews
- Examples of detected suspicious reviews

### 2. **Price Analysis**
- Prophet time-series forecasting for price predictions
- 3-month price forecasts for each platform
- Multi-platform price comparison
- Price stability metrics and trend analysis

### 3. **Sales Forecasting**
- Prophet-based demand and sales predictions
- 90-day sales forecasts
- Trend visualization
- Popularity indicators

### 4. **Eco-Friendliness Rating**
- Carbon emissions calculation based on shipping distance
- PIN code-based distance calculation
- Color-coded environmental impact (Green/Yellow/Orange/Red)
- Sustainable purchasing guidance

### 5. **Comprehensive Product Score**
- Multi-factor scoring system (0-100 scale)
- Weighted analysis considering:
  - Fake review percentage (25%)
  - Price stability (20%)
  - Sales trends (20%)
  - Eco-friendliness (20%)
  - Platform reliability (15%)
- Smart recommendations based on overall score

## 📋 Requirements

### System Requirements
- Python 3.8+
- 4GB RAM minimum
- 500MB free disk space

### Dependencies
All Python packages are listed in `requirements.txt`:
- streamlit==1.28.1
- pandas==2.0.3
- numpy==1.24.3
- scikit-learn==1.3.0
- xgboost==2.0.0
- prophet==1.1.4
- matplotlib==3.7.2
- plotly==5.16.1
- seaborn==0.12.2
- pytz==2023.3

## 🚀 Installation

### Step 1: Clone/Setup the Project
```bash
cd unified_ecommerce_app
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Prepare Data Files
Ensure the following CSV files are in the parent directory:
- `apple_iphone.csv`
- `nike_revolution.csv`
- `cricket bat.csv`
- `prestige_induction.csv`
- `levis_mens_cotton_tshirt.csv`
- `cross_platform_products.csv` (for warehouse and pricing data)
- `model training.csv` (for XGBoost model training)

## 📁 Project Structure

```
unified_ecommerce_app/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration and constants
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── modules/
│   ├── __init__.py
│   ├── data_loader.py             # CSV data loading and management
│   ├── fake_review_detector.py    # XGBoost fake review detection
│   ├── forecasting.py             # Prophet price and sales forecasting
│   ├── carbon_emissions.py        # Carbon emissions calculator
│   └── product_score.py           # Product score calculation
├── data/
│   └── (CSV files stored here)
└── assets/
    └── (Images and styling resources)
```

## ▶️ Running the Application

### Local Development
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Command-line Options
```bash
# Run with custom port
streamlit run app.py --server.port 8080

# Run in headless mode
streamlit run app.py --logger.level=error

# Run with custom config
streamlit run app.py --config.toml path/to/config.toml
```

## 📊 Data Format Requirements

### Product Review CSV
```
Columns needed (at least one of each category):
- Text column: review_text, text, review, or content
- Platform column: platform, marketplace, seller, or store
- Date column: date, timestamp, datetime, or date_created
- (Optional) Price column: price, current_price, or selling_price
- (Optional) Sales column: sales, quantity, units_sold, or units
```

### Training Data CSV (for XGBoost)
```
Columns needed:
- Text column: review_text, text, review, or content
- Label column: label, is_fake, or fake (0=real, 1=fake)
```

### Cross-Platform Products CSV
```
Columns needed:
- Pin code column: pin, pincode, pin_code, or warehouse_pin
- (Optional) Platform column: platform, marketplace, or seller
- Price data for forecasting
- Sales/quantity data for forecasting
```

## 🎮 How to Use

1. **Enter Your Location**
   - Click on the home page
   - Enter your 6-digit PIN code
   - Click "Confirm Location"

2. **Select a Product**
   - Choose from 5 available products
   - The system will analyze the product data

3. **View Analytics**
   - Navigate through tabs:
     - Sales Forecast: 90-day demand prediction
     - Price Analysis: 3-month price trends
     - Fake Reviews: Review authenticity analysis
     - Eco-Friendliness: Environmental impact rating
     - Overall Score: Comprehensive product rating

4. **Make Decisions**
   - Compare platforms
   - Check eco-friendly options
   - Review quality metrics
   - Make informed purchases

## 🔧 Configuration

Edit `config.py` to customize:
- Product list and categories
- Platform colors and details
- ML model parameters
- Forecasting parameters
- Scoring weights
- Carbon emission factors

## 📈 Model Details

### Fake Review Detection (XGBoost)
- **Features**: TF-IDF text vectors, review length, word count
- **Training Data**: model training.csv with fake labels
- **Output**: Probability of review being fake (0-1)
- **Threshold**: 0.5 (configurable)

### Price Forecasting (Prophet)
- **Model**: Facebook's Prophet time-series forecasting
- **Frequency**: Daily/aggregated data
- **Forecast Horizon**: 90 days
- **Seasonality**: Yearly and weekly

### Sales Forecasting (Prophet)
- **Model**: Facebook's Prophet with changepoint detection
- **Features**: Seasonal patterns, trend changes
- **Forecast Horizon**: 90 days
- **Bounds**: 95% confidence intervals

## 🌍 Eco-Friendliness Calculation

Carbon emissions are calculated using:
- Distance between warehouse and user location (Haversine formula)
- Transport mode selection based on distance:
  - Road: <500 km, 84 g CO2/kg-km
  - Rail: 500-2000 km, 41 g CO2/kg-km
  - Air: >2000 km, 255 g CO2/kg-km
- Product weight (default: 1 kg)

## 🚀 Deployment

### Streamlit Cloud
1. Push repository to GitHub
2. Go to share.streamlit.io
3. Connect your GitHub repository
4. Deploy instantly

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
git push heroku main
```

### AWS (EC2)
```bash
# Create EC2 instance
# SSH into instance
# Install Python and dependencies
# Clone repository
# Run: streamlit run app.py --server.port 80
```

## 📝 CSV File Examples

### Product Review Format
```csv
review_text,rating,platform,date,price
"Great product!",5,Amazon,2024-01-15,9999
"Not as described",2,Flipkart,2024-01-14,9500
```

### Model Training Format
```csv
review_text,label
"Buy now!!!",1
"Excellent quality",0
"Fake product",1
```

## 🔐 Security Considerations

1. **Data Privacy**: PIN codes are only used locally for distance calculations
2. **No Data Storage**: User information is not persisted
3. **Safe Dependencies**: All packages are from official PyPI
4. **Input Validation**: User inputs are validated before processing

## 🐛 Troubleshooting

### Issue: "No such file or directory" for CSV files
**Solution**: Place CSV files in the correct directory or update the data_dir path in the code

### Issue: "No module named 'prophet'"
**Solution**: Install requirements: `pip install -r requirements.txt`

### Issue: Model training fails
**Solution**: Ensure model training.csv has proper format with text and label columns

### Issue: Slow forecasting
**Solution**: Prophet can be slow on first run. Results are cached afterward.

## 📚 API Documentation

### FakeReviewDetector
```python
detector = FakeReviewDetector()
detector.train('path/to/training/data.csv')
probabilities = detector.predict(reviews_list)
fake_pct, fake_count, total_count = detector.get_fake_percentage(reviews_list)
```

### PriceForecastor
```python
forecaster = PriceForecastor('product_name')
prepared_data = forecaster.prepare_data(df, platform_col, date_col, price_col)
forecasts = forecaster.forecast(prepared_data, periods=90)
forecast_df = forecaster.get_forecast_dataframe('platform_name')
```

### CarbonEmissionsCalculator
```python
calc = CarbonEmissionsCalculator()
calc.load_warehouse_data('warehouse_data.csv')
emissions = calc.calculate_emissions(warehouse_pin, user_pin, weight=1.0)
ratings = calc.get_all_platform_ratings(user_pin)
```

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review CSV file formats
3. Verify all dependencies are installed
4. Check Streamlit documentation: https://docs.streamlit.io

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Features Roadmap

- [ ] User account and preferences
- [ ] Review comparison with other users
- [ ] Integration with real warehouse locations API
- [ ] Mobile app version
- [ ] Real-time price tracking
- [ ] Email notifications for price drops
- [ ] Advanced ML models for review detection
- [ ] Integration with real e-commerce APIs

## 👥 Contributors

Developed as a comprehensive e-commerce analysis system in January 2026.

---

**Version**: 1.0.0  
**Last Updated**: January 2026
