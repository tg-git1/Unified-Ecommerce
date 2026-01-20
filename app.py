import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.data_loader import DataLoader
from modules.fake_review_detector import FakeReviewDetector
from modules.forecasting import PriceForecastor, SalesForecastor
from modules.carbon_emissions import CarbonEmissionsCalculator
from modules.product_score import ProductScoreCalculator

# Page configuration
st.set_page_config(
    page_title="Unified E-Commerce System",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .score-excellent {
        color: #27ae60;
        font-weight: bold;
        font-size: 2em;
    }
    
    .score-good {
        color: #2980b9;
        font-weight: bold;
        font-size: 2em;
    }
    
    .score-moderate {
        color: #f39c12;
        font-weight: bold;
        font-size: 2em;
    }
    
    .score-poor {
        color: #e74c3c;
        font-weight: bold;
        font-size: 2em;
    }
    
    .eco-green {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .eco-yellow {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .eco-orange {
        background: #ffe5cc;
        border-left: 5px solid #ff9800;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .eco-red {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .navbar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .streamlit-container {
        max-width: 1400px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_pincode' not in st.session_state:
    st.session_state.user_pincode = None
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if 'detector_trained' not in st.session_state:
    st.session_state.detector_trained = False
if 'fake_detector' not in st.session_state:
    st.session_state.fake_detector = FakeReviewDetector()
if 'data_loader' not in st.session_state:
    # Determine data directory - look for data subdirectory first, then parent
    script_dir = Path(__file__).parent
    data_dir = script_dir / 'data'  # Primary location: data/ subdirectory
    
    # If not found, try parent directory
    if not data_dir.exists():
        parent_data_dir = script_dir.parent
        if any(parent_data_dir.glob('*.csv')):
            data_dir = parent_data_dir
        else:
            # Fall back to data subdirectory even if it doesn't exist
            data_dir = script_dir / 'data'
    
    st.session_state.data_loader = DataLoader(str(data_dir))

# Header
st.markdown("""
<div class="navbar">
    <h1>🛍️ Unified E-Commerce System</h1>
    <p>Your intelligent shopping companion for better purchasing decisions</p>
</div>
""", unsafe_allow_html=True)

# Determine current page based on product selection
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Sidebar
with st.sidebar:
    st.header("🎯 Navigation")
    
    # Auto-navigate to Product Details if a product is selected
    if st.session_state.selected_product:
        page = "Product Details"
        st.session_state.current_page = "Product Details"
    else:
        page = st.radio("Select Page", ["Home", "Product Details", "About"], 
                       index=0 if st.session_state.current_page == "Home" else 
                             (1 if st.session_state.current_page == "Product Details" else 2))
        st.session_state.current_page = page
    
    st.divider()
    
    st.header("📍 Location Info")
    if st.session_state.user_pincode:
        st.success(f"Your Pin Code: {st.session_state.user_pincode}")
        if st.button("Change Pin Code"):
            st.session_state.user_pincode = None
            st.session_state.selected_product = None
            st.session_state.current_page = "Home"
            st.rerun()
    else:
        st.info("No pin code entered yet. Enter on home page.")


def show_home_page():
    """Display home page with product selection"""
    
    # Pin code input modal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 📍 Enter Your Location")
        
        pincode_input = st.text_input(
            "Enter your 6-digit PIN code:",
            placeholder="e.g., 560001",
            key="pincode_input"
        )
        
        if st.button("Confirm Location", type="primary", use_container_width=True):
            if pincode_input and len(pincode_input) >= 5:
                st.session_state.user_pincode = pincode_input
                st.success(f"Location set to PIN code: {pincode_input}")
            else:
                st.error("Please enter a valid PIN code (at least 5 digits)")
    
    if not st.session_state.user_pincode:
        st.warning("⚠️ Please enter your PIN code to get started!")
        return
    
    st.divider()
    
    # Product selection
    st.markdown("### 🛒 Select a Product to Analyze")
    
    data_loader = st.session_state.data_loader
    products = data_loader.get_available_products()
    
    # Create product cards
    cols = st.columns(min(2, len(products)))
    
    for idx, product in enumerate(products):
        col = cols[idx % len(cols)]
        
        with col:
            if st.button(
                f"📦 {product}",
                key=f"product_{product}",
                use_container_width=True,
                help="Click to analyze this product"
            ):
                st.session_state.selected_product = product
                st.rerun()
    
    # Feature highlights
    st.divider()
    st.markdown("### ✨ What We Analyze")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📊 Fake Reviews Detection
        - XGBoost ML model
        - Platform-wise analysis
        - Trust score for reviews
        """)
    
    with col2:
        st.markdown("""
        #### 💰 Price Analysis
        - Prophet forecasting
        - 3-month predictions
        - Platform comparison
        """)
    
    with col3:
        st.markdown("""
        #### 🌱 Eco-Friendliness
        - Carbon emissions calc
        - Shipment impact
        - Green rating
        """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📈 Sales Forecasting
        - Prophet model
        - Trend analysis
        - Demand prediction
        """)
    
    with col2:
        st.markdown("""
        #### ⭐ Product Score
        - Comprehensive rating
        - Multi-factor analysis
        - Recommendation engine
        """)
    
    with col3:
        st.markdown("""
        #### 🚀 Smart Insights
        - Platform comparison
        - Data-driven decisions
        - Detailed analytics
        """)


def show_product_details():
    """Display detailed product analysis"""
    
    # Add back button at the top
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("← Back to Home"):
            st.session_state.selected_product = None
            st.session_state.current_page = "Home"
            st.rerun()
    
    if not st.session_state.user_pincode:
        st.warning("⚠️ Please enter your PIN code on the home page first!")
        return
    
    if not st.session_state.selected_product:
        st.info("👈 Select a product from the home page to view details")
        return
    
    product = st.session_state.selected_product
    st.markdown(f"### 📦 {product} - Detailed Analysis")
    
    # Load data
    data_loader = st.session_state.data_loader
    product_reviews = data_loader.load_product_reviews(product)
    cross_platform_data = data_loader.load_cross_platform_data()
    
    if product_reviews is None:
        st.error(f"Could not load data for {product}")
        return
    
    # Initialize components
    detector = st.session_state.fake_detector  # Use cached detector
    price_forecaster = PriceForecastor(product)
    sales_forecaster = SalesForecastor(product)
    carbon_calc = CarbonEmissionsCalculator()
    score_calc = ProductScoreCalculator()
    
    # Load warehouse data if available
    if cross_platform_data is not None:
        cross_platform_path = Path(data_loader.data_dir) / 'cross_platform_products.csv'
        if cross_platform_path.exists():
            carbon_calc.load_warehouse_data(str(cross_platform_path))
    
    # Train fake review detector if not already done
    if not st.session_state.detector_trained:
        try:
            training_data_path = Path(data_loader.data_dir) / 'model training.csv'
            if training_data_path.exists():
                with st.spinner("🤖 Training fake review detector..."):
                    detector.train(str(training_data_path))
                st.session_state.detector_trained = True
            else:
                # Mark as trained even without data to prevent repeated attempts
                st.session_state.detector_trained = True
        except Exception as e:
            st.warning(f"Could not train detector: {str(e)}")
            st.session_state.detector_trained = True  # Mark as attempted to avoid loops
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Sales Forecast",
        "💰 Price Analysis",
        "⚠️ Fake Reviews",
        "🌱 Eco-Friendliness",
        "⭐ Overall Score"
    ])
    
    # Tab 1: Sales Forecasting
    with tab1:
        st.markdown("#### Sales Forecasting (Next 90 Days)")
        
        platform_col = data_loader.extract_platform_column(product_reviews) if hasattr(data_loader, 'extract_platform_column') else None
        
        # Try to identify columns
        date_col = data_loader.extract_date_column(product_reviews)
        sales_col = data_loader.extract_sales_column(product_reviews)
        
        if date_col and sales_col:
            prepared_data = sales_forecaster.prepare_data(
                product_reviews,
                platform_col or 'Platform',
                date_col,
                sales_col
            )
            
            if prepared_data:
                forecasts = sales_forecaster.forecast(prepared_data, periods=90)
                
                # Display forecasts
                if forecasts:
                    st.success("✅ Sales forecast generated successfully!")
                    
                    for platform, forecast in forecasts.items():
                        st.subheader(f"{platform} - Sales Forecast")
                        
                        # Display chart
                        chart_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
                        chart_data.columns = ['Date', 'Predicted Sales', 'Lower Bound', 'Upper Bound']
                        
                        st.line_chart(
                            data=chart_data.set_index('Date')[['Predicted Sales']],
                            use_container_width=True
                        )
                        
                        # Statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Average Sales", f"{forecast['yhat'].mean():.2f}")
                        with col2:
                            st.metric("Max Sales", f"{forecast['yhat'].max():.2f}")
                        with col3:
                            trend = "📈 Growing" if forecast['yhat'].iloc[-1] > forecast['yhat'].iloc[0] else "📉 Declining"
                            st.metric("Trend", trend)
                else:
                    st.info("No sales data available for forecasting")
            else:
                st.warning("Could not prepare sales data for forecasting")
        else:
            st.info("Sales forecasting data not available in the dataset")
    
    # Tab 2: Price Analysis
    with tab2:
        st.markdown("#### Price Analysis (Next 90 Days)")
        
        price_col = data_loader.extract_price_column(product_reviews)
        date_col = data_loader.extract_date_column(product_reviews)
        
        if price_col and date_col:
            prepared_data = price_forecaster.prepare_data(
                product_reviews,
                platform_col or 'Platform',
                date_col,
                price_col
            )
            
            if prepared_data:
                forecasts = price_forecaster.forecast(prepared_data, periods=90)
                
                if forecasts:
                    st.success("✅ Price forecast generated successfully!")
                    
                    all_prices = []
                    
                    for platform, forecast in forecasts.items():
                        st.subheader(f"{platform} - Price Forecast")
                        
                        chart_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
                        chart_data.columns = ['Date', 'Predicted Price', 'Lower Bound', 'Upper Bound']
                        
                        st.line_chart(
                            data=chart_data.set_index('Date')[['Predicted Price']],
                            use_container_width=True
                        )
                        
                        # Price statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Current Price", f"₹{forecast['yhat'].iloc[0]:.2f}")
                        with col2:
                            st.metric("Average Price", f"₹{forecast['yhat'].mean():.2f}")
                        with col3:
                            stability = score_calc.calculate_price_stability_score(forecast)
                            st.metric("Price Stability", f"{stability:.1f}%")
                        
                        all_prices.append(forecast['yhat'].mean())
                    
                    # Platform comparison
                    st.divider()
                    st.markdown("#### 📊 Platform Comparison")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        cheapest_idx = np.argmin(all_prices)
                        platforms_list = list(forecasts.keys())
                        st.info(f"💰 Cheapest: **{platforms_list[cheapest_idx]}** (₹{all_prices[cheapest_idx]:.2f})")
                    with col2:
                        expensive_idx = np.argmax(all_prices)
                        st.warning(f"📈 Most Expensive: **{platforms_list[expensive_idx]}** (₹{all_prices[expensive_idx]:.2f})")
                else:
                    st.info("No price data available for forecasting")
        else:
            st.info("Price data not available in the dataset")
    
    # Tab 3: Fake Reviews Detection
    with tab3:
        st.markdown("#### Fake Reviews Analysis")
        
        # Check if detector is trained and has a valid model
        if st.session_state.detector_trained and st.session_state.fake_detector.model is not None:
            try:
                # Get reviews
                text_cols = [col for col in product_reviews.columns 
                           if col.lower() in ['review_text', 'text', 'review', 'content']]
                
                if text_cols:
                    text_col = text_cols[0]
                    
                    # Detect fake reviews
                    fake_pct, fake_count, total_count, probs = detector.get_fake_percentage(
                        product_reviews[text_col],
                        threshold=0.5
                    )
                    
                    # Overall statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Reviews", total_count)
                    with col2:
                        st.metric("Fake Reviews", fake_count)
                    with col3:
                        if fake_pct < 20:
                            st.metric("Fake %", f"{fake_pct:.1f}%", delta="✅ Low")
                        elif fake_pct < 50:
                            st.metric("Fake %", f"{fake_pct:.1f}%", delta="⚠️ Medium")
                        else:
                            st.metric("Fake %", f"{fake_pct:.1f}%", delta="❌ High")
                    
                    # Platform-wise analysis
                    st.divider()
                    st.markdown("#### Platform-wise Analysis")
                    
                    if platform_col in product_reviews.columns:
                        platforms = product_reviews[platform_col].unique()
                        
                        for platform in platforms:
                            platform_reviews = product_reviews[product_reviews[platform_col] == platform][text_col]
                            
                            if len(platform_reviews) > 0:
                                p_fake_pct, p_fake_count, p_total_count, _ = detector.get_fake_percentage(
                                    platform_reviews,
                                    threshold=0.5
                                )
                                
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.write(f"**{platform}**: {p_fake_count}/{p_total_count} fake ({p_fake_pct:.1f}%)")
                                with col2:
                                    if p_fake_pct < 30:
                                        st.success("✅")
                                    elif p_fake_pct < 60:
                                        st.warning("⚠️")
                                    else:
                                        st.error("❌")
                    
                    # Example fake reviews
                    st.divider()
                    st.markdown("#### Examples of Suspicious Reviews")
                    
                    # Get reviews with high fake probability
                    suspicious_indices = np.where(probs > 0.7)[0]
                    
                    if len(suspicious_indices) > 0:
                        num_examples = min(3, len(suspicious_indices))
                        for i in range(num_examples):
                            idx = suspicious_indices[i]
                            confidence = probs[idx] * 100
                            
                            st.warning(f"🚨 Review #{i+1} (Confidence: {confidence:.1f}%)")
                            st.text(product_reviews.iloc[idx][text_col][:200] + "...")
                    else:
                        st.success("No highly suspicious reviews detected!")
                else:
                    st.info("No review text column found in data")
            except Exception as e:
                st.error(f"Error analyzing fake reviews: {str(e)}")
        else:
            st.info("Fake review detector is being trained...")
    
    # Tab 4: Eco-Friendliness
    with tab4:
        st.markdown("#### 🌱 Eco-Friendliness Rating")
        
        user_pin = st.session_state.user_pincode
        
        try:
            # Extract platforms from product data
            available_platforms = None
            if platform_col and platform_col in product_reviews.columns:
                available_platforms = list(product_reviews[platform_col].unique())
            
            # Get platform eco ratings (only for available platforms)
            eco_ratings = carbon_calc.get_all_platform_ratings(
                user_pin,
                platforms=available_platforms,
                product_weight=1.0
            )
            
            st.markdown(f"Based on shipping from warehouse to PIN code: **{user_pin}**")
            st.divider()
            
            # Display eco ratings for each platform
            eco_colors = {
                'green': 'eco-green',
                'yellow': 'eco-yellow',
                'orange': 'eco-orange',
                'red': 'eco-red'
            }
            
            for platform, rating in eco_ratings.items():
                color_class = eco_colors.get(rating['color'], 'eco-yellow')
                
                st.markdown(f"""
                <div class="{color_class}">
                    <h4>{platform}</h4>
                    <p><strong>Distance:</strong> {rating['distance']:.0f} km</p>
                    <p><strong>Rating:</strong> {rating['rating']}</p>
                    <p><strong>CO₂ Emissions:</strong> {rating['emissions']:.3f} kg</p>
                    <p>{rating['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Best platform for eco-friendliness
            st.divider()
            if eco_ratings:
                best_platform = min(eco_ratings.items(), key=lambda x: x[1]['emissions'])
                st.success(f"🏆 **Most Eco-Friendly:** {best_platform[0]} with {best_platform[1]['emissions']:.3f} kg CO₂")
            else:
                st.info("Unable to calculate eco-friendliness ratings")
            
        except Exception as e:
            st.error(f"Error calculating eco-friendliness: {str(e)}")
    
    # Tab 5: Overall Product Score
    with tab5:
        st.markdown("#### ⭐ Overall Product Score")
        
        try:
            # Gather all metrics
            user_pin = st.session_state.user_pincode
            
            # Fake review score
            fake_pct = 0
            if st.session_state.detector_trained:
                text_cols = [col for col in product_reviews.columns 
                           if col.lower() in ['review_text', 'text', 'review', 'content']]
                if text_cols:
                    text_col = text_cols[0]
                    fake_pct, _, _, _ = detector.get_fake_percentage(product_reviews[text_col])
            
            # Get forecasts for scores
            price_col = data_loader.extract_price_column(product_reviews)
            sales_col = data_loader.extract_sales_column(product_reviews)
            date_col = data_loader.extract_date_column(product_reviews)
            platform_col_actual = [col for col in product_reviews.columns 
                                  if col.lower() in ['platform', 'marketplace', 'seller', 'store']]
            platform_col = platform_col_actual[0] if platform_col_actual else 'Platform'
            
            price_forecast_data = None
            sales_forecast_data = None
            
            if price_col and date_col:
                prepared = price_forecaster.prepare_data(product_reviews, platform_col, date_col, price_col)
                if prepared:
                    price_forecaster.forecast(prepared, periods=90)
                    first_platform = list(prepared.keys())[0] if prepared else None
                    if first_platform:
                        price_forecast_data = price_forecaster.get_forecast_dataframe(first_platform)
            
            if sales_col and date_col:
                prepared = sales_forecaster.prepare_data(product_reviews, platform_col, date_col, sales_col)
                if prepared:
                    sales_forecaster.forecast(prepared, periods=90)
                    first_platform = list(prepared.keys())[0] if prepared else None
                    if first_platform:
                        sales_forecast_data = sales_forecaster.get_forecast_dataframe(first_platform)
            
            # Get eco score
            # Extract platforms from product data
            available_platforms = None
            if platform_col and platform_col in product_reviews.columns:
                available_platforms = list(product_reviews[platform_col].unique())
            
            eco_ratings = carbon_calc.get_all_platform_ratings(user_pin, platforms=available_platforms, product_weight=1.0)
            first_platform = list(eco_ratings.keys())[0] if eco_ratings else 'Amazon'
            eco_color = eco_ratings.get(first_platform, {}).get('color', 'yellow')
            
            # Calculate overall score
            overall_score, scores = score_calc.calculate_overall_score(
                fake_pct,
                price_forecast_data,
                sales_forecast_data,
                eco_color,
                first_platform
            )
            
            # Display overall score
            st.markdown(f"## {overall_score:.1f}/100")
            
            rating, recommendation = score_calc.get_score_interpretation(overall_score)
            
            if overall_score >= 80:
                st.success(f"### ✅ {rating}")
            elif overall_score >= 60:
                st.info(f"### ℹ️ {rating}")
            else:
                st.error(f"### ❌ {rating}")
            
            st.markdown(f"**Recommendation:** {recommendation}")
            
            # Detailed score breakdown
            st.divider()
            st.markdown("#### Score Breakdown")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Fake Reviews", f"{scores['fake_reviews']:.1f}", "Quality")
                st.metric("Price Stability", f"{scores['price_stability']:.1f}", "Reliability")
            
            with col2:
                st.metric("Sales Trend", f"{scores['sales_trend']:.1f}", "Popularity")
                st.metric("Eco-Friendliness", f"{scores['eco_friendliness']:.1f}", "Environment")
            
            with col3:
                st.metric("Platform Reliability", f"{scores['platform_reliability']:.1f}", "Trustworthiness")
            
            # Score visualization
            st.divider()
            score_df = pd.DataFrame({
                'Category': list(scores.keys()),
                'Score': list(scores.values())
            })
            
            st.bar_chart(score_df.set_index('Category'), use_container_width=True)
            
        except Exception as e:
            st.error(f"Error calculating product score: {str(e)}")
            print(f"Error details: {e}")


def show_about_page():
    """Display about page"""
    st.markdown("""
    ## About Unified E-Commerce System
    
    ### 🎯 Mission
    To empower consumers with data-driven insights for making better purchasing decisions across multiple e-commerce platforms.
    
    ### 🔬 Technology Stack
    - **Frontend:** Streamlit
    - **Machine Learning:** XGBoost for fake review detection
    - **Forecasting:** Prophet for price and sales predictions
    - **Data Processing:** Pandas, NumPy
    - **Visualization:** Plotly, Matplotlib, Seaborn
    
    ### 📊 Features
    
    #### 1. Fake Review Detection
    - Uses XGBoost ML model trained on review patterns
    - Identifies suspicious reviews across platforms
    - Provides trust scores for product reviews
    
    #### 2. Price Analysis
    - Prophet time-series forecasting
    - 3-month price predictions
    - Platform-wise comparison
    - Price stability metrics
    
    #### 3. Sales Forecasting
    - Prophet-based demand prediction
    - Trend analysis
    - 90-day sales forecasts
    
    #### 4. Eco-Friendliness Rating
    - Carbon emissions calculation
    - Distance-based shipment analysis
    - Color-coded environmental impact
    - Green/Yellow/Red sustainability metrics
    
    #### 5. Comprehensive Product Score
    - Multi-factor analysis
    - Weighted scoring system
    - Personalized recommendations
    - Comparative insights
    
    ### 📍 How It Works
    
    1. **Enter Your Location** - Provide your PIN code for personalized analysis
    2. **Select a Product** - Choose from 5 featured products
    3. **View Analytics** - Get detailed insights on:
       - Sales trends
       - Price predictions
       - Fake reviews
       - Environmental impact
       - Overall product score
    4. **Make Informed Decisions** - Compare platforms and make the best purchase
    
    ### 🛡️ Data Privacy
    - Your location PIN code is used only for distance calculations
    - No personal data is stored or transmitted
    - All analysis is performed locally
    
    ### 📧 Contact & Support
    For questions or suggestions, please reach out to our team.
    
    ---
    
    **Version:** 1.0.0  
    **Last Updated:** January 2026
    """)


# Main app logic
if page == "Home":
    show_home_page()
elif page == "Product Details":
    show_product_details()
else:
    show_about_page()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; margin-top: 30px;">
    <p>🛍️ Unified E-Commerce System © 2026 | Making shopping smarter, one click at a time</p>
</div>
""", unsafe_allow_html=True)
