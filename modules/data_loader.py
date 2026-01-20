import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta


class DataLoader:
    """Load and manage data from CSV files"""
    
    PRODUCT_MAPPING = {
        'Apple iPhone': 'apple_iphone.csv',
        'Nike Revolution': 'nike_revolution.csv',
        'Cricket Bat': 'cricket bat.csv',
        'Prestige Induction': 'prestige_induction.csv',
        'Levis Mens Cotton T-Shirt': 'levis_mens_cotton_tshirt.csv'
    }
    
    PLATFORM_COLORS = {
        'amazon': '#FF9900',
        'flipkart': '#0A66C2',
        'ebay': '#E53238',
        'myntra': '#F15A24',
        'ajio': '#0066CC'
    }
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.product_data_cache = {}
        self.cross_platform_data = None
        self.training_data = None
        
    def load_product_reviews(self, product_name):
        """Load reviews for a specific product"""
        if product_name in self.product_data_cache:
            return self.product_data_cache[product_name]
        
        filename = self.PRODUCT_MAPPING.get(product_name)
        if not filename:
            return None
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            df = pd.read_csv(filepath)
            # Add synthetic date and sales columns if they don't exist
            df = self._enrich_with_time_series_data(df)
            self.product_data_cache[product_name] = df
            return df
        except Exception as e:
            print(f"Error loading {product_name}: {str(e)}")
            return None
    
    def load_cross_platform_data(self):
        """Load cross-platform product data"""
        if self.cross_platform_data is not None:
            return self.cross_platform_data
        
        filepath = os.path.join(self.data_dir, 'cross_platform_products.csv')
        
        try:
            df = pd.read_csv(filepath)
            self.cross_platform_data = df
            return df
        except Exception as e:
            print(f"Error loading cross-platform data: {str(e)}")
            return None
    
    def load_training_data(self):
        """Load training data for ML models"""
        if self.training_data is not None:
            return self.training_data
        
        # Try different possible filenames
        possible_names = ['model training.csv', 'model_training.csv', 'model training data.csv']
        
        for filename in possible_names:
            filepath = os.path.join(self.data_dir, filename)
            try:
                if os.path.exists(filepath):
                    df = pd.read_csv(filepath)
                    self.training_data = df
                    return df
            except Exception as e:
                continue
        
        print("Error loading training data")
        return None
    
    def get_available_products(self):
        """Get list of available products"""
        return list(self.PRODUCT_MAPPING.keys())
    
    def get_platform_color(self, platform_name):
        """Get color for a platform"""
        platform_lower = platform_name.lower().strip()
        
        for key, color in self.PLATFORM_COLORS.items():
            if key in platform_lower or platform_lower.startswith(key):
                return color
        
        # Default colors
        default_colors = ['#0A66C2', '#FF9900', '#E53238', '#F15A24', '#0066CC']
        return default_colors[hash(platform_name) % len(default_colors)]
    
    def extract_platforms(self, df):
        """Extract unique platforms from DataFrame"""
        platforms = []
        
        for col in df.columns:
            if col.lower() in ['platform', 'marketplace', 'seller', 'store']:
                return df[col].unique().tolist()
        
        # If no platform column, try to infer from data
        return platforms or ['Platform_1', 'Platform_2', 'Platform_3']
    
    def extract_price_column(self, df):
        """Find price column in DataFrame"""
        for col in df.columns:
            if col.lower() in ['price', 'current_price', 'selling_price', 'amount', 'cost']:
                return col
        return None
    
    def extract_sales_column(self, df):
        """Find sales/quantity column in DataFrame"""
        for col in df.columns:
            if col.lower() in ['sales', 'quantity', 'units_sold', 'units', 'qty', 'count']:
                return col
        return None
    
    def extract_platform_column(self, df):
        """Find platform column in DataFrame"""
        for col in df.columns:
            if col.lower() in ['platform', 'marketplace', 'seller', 'store']:
                return col
        return None
    
    def extract_date_column(self, df):
        """Find date column in DataFrame"""
        for col in df.columns:
            if col.lower() in ['date', 'timestamp', 'datetime', 'created_at', 'date_created']:
                return col
        return None
    
    def _enrich_with_time_series_data(self, df):
        """Add synthetic date, price and sales columns if not present"""
        # Add date column if missing
        if not self.extract_date_column(df):
            # Generate dates spread over the last 365 days
            n_rows = len(df)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            # Convert numpy int to Python int
            dates = [start_date + timedelta(days=int(x)) for x in sorted(np.random.randint(0, 365, n_rows))]
            df['date'] = pd.to_datetime(dates).strftime('%Y-%m-%d')
        
        # Add price column if missing
        if not self.extract_price_column(df):
            # Generate realistic prices based on product name
            if 'product_name' in df.columns:
                # Price ranges for different products
                product_prices = {
                    'iphone': (50000, 150000),
                    'nike': (3000, 10000),
                    'cricket': (500, 3000),
                    'prestige': (3000, 15000),
                    'levis': (1000, 5000),
                }
                
                def get_price_range(product_name):
                    product_name_lower = str(product_name).lower()
                    for keyword, (min_p, max_p) in product_prices.items():
                        if keyword in product_name_lower:
                            return (min_p, max_p)
                    return (1000, 10000)  # Default range
                
                prices = []
                for idx, row in df.iterrows():
                    min_p, max_p = get_price_range(row.get('product_name', ''))
                    prices.append(np.random.uniform(min_p, max_p))
                df['price'] = prices
            else:
                df['price'] = np.random.uniform(1000, 50000, len(df))
        
        # Add sales column if missing
        if not self.extract_sales_column(df):
            # Generate realistic sales based on rating (higher rating = more likely to sell)
            if 'rating' in df.columns:
                df['sales'] = df['rating'].apply(lambda x: int(np.random.normal(50 + (x * 10), 15)))
            else:
                df['sales'] = np.random.randint(20, 100, len(df))
            df['sales'] = df['sales'].clip(lower=0)  # No negative sales
        
        return df
    
    def get_cross_platform_timeseries(self, product_name):
        """
        Extract monthly time-series data from cross-platform file
        
        Args:
            product_name: name of the product
            
        Returns:
            DataFrame with columns: date, platform, price, sales
        """
        cross_platform_df = self.load_cross_platform_data()
        
        if cross_platform_df is None:
            return None
        
        # Filter for the product
        product_matches = cross_platform_df[
            cross_platform_df['product_name'].str.lower() == product_name.lower()
        ]
        
        if product_matches.empty:
            return None
        
        timeseries_data = []
        
        for _, row in product_matches.iterrows():
            platform = row.get('platform', 'Unknown')
            
            # Extract monthly data
            for month in range(1, 9):  # 8 months of data
                price_col = f'price_month_{month}'
                sales_col = f'sales_month_{month}'
                
                if price_col in cross_platform_df.columns and sales_col in cross_platform_df.columns:
                    # Create date (assume start from current date - months back)
                    date = pd.Timestamp.now() - pd.DateOffset(months=8-month)
                    
                    timeseries_data.append({
                        'date': date,
                        'platform': platform,
                        'price': float(row[price_col]) if pd.notna(row[price_col]) else None,
                        'sales': int(row[sales_col]) if pd.notna(row[sales_col]) else None
                    })
        
        if not timeseries_data:
            return None
        
        result_df = pd.DataFrame(timeseries_data)
        result_df = result_df.sort_values('date')
        
        return result_df

