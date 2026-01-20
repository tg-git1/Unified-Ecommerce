# Configuration settings for Unified E-Commerce System

# Products available in the system
PRODUCTS = {
    'Apple iPhone': {
        'file': 'apple_iphone.csv',
        'category': 'Electronics',
        'icon': '📱'
    },
    'Nike Revolution': {
        'file': 'nike_revolution.csv',
        'category': 'Footwear',
        'icon': '👟'
    },
    'Cricket Bat': {
        'file': 'cricket bat.csv',
        'category': 'Sports',
        'icon': '🏏'
    },
    'Prestige Induction': {
        'file': 'prestige_induction.csv',
        'category': 'Kitchen Appliances',
        'icon': '🍳'
    },
    'Levis Mens Cotton T-Shirt': {
        'file': 'levis_mens_cotton_tshirt.csv',
        'category': 'Clothing',
        'icon': '👕'
    }
}

# Platforms and their colors
PLATFORMS = {
    'Amazon': '#FF9900',
    'Flipkart': '#0A66C2',
    'eBay': '#E53238',
    'Myntra': '#F15A24',
    'AJIO': '#0066CC'
}

# XGBoost model parameters
XGBOOST_PARAMS = {
    'n_estimators': 100,
    'max_depth': 6,
    'learning_rate': 0.1,
    'random_state': 42,
    'eval_metric': 'logloss'
}

# Prophet forecasting parameters
PROPHET_PARAMS = {
    'yearly_seasonality': True,
    'weekly_seasonality': True,
    'daily_seasonality': False,
    'interval_width': 0.95
}

# Product score weights
SCORE_WEIGHTS = {
    'fake_reviews': 0.25,
    'price_stability': 0.20,
    'sales_trend': 0.20,
    'eco_friendliness': 0.20,
    'platform_reliability': 0.15
}

# Carbon emission factors (g CO2 per kg-km)
EMISSION_FACTORS = {
    'air': 255,
    'rail': 41,
    'road': 84,
    'ship': 10
}

# Eco-friendliness thresholds (kg CO2)
ECO_THRESHOLDS = {
    'green': 0.5,
    'yellow': 1.0,
    'orange': 1.5,
    'red': 2.5
}

# Default forecast periods (days)
FORECAST_PERIODS = 90

# Fake review probability threshold
FAKE_REVIEW_THRESHOLD = 0.5
