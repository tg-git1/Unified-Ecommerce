import pandas as pd
import numpy as np
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')


class PriceForecastor:
    """Prophet-based price forecasting for multiple platforms"""
    
    def __init__(self, product_name):
        self.product_name = product_name
        self.models = {}
        self.forecasts = {}
        
    def prepare_data(self, df, platform_col, date_col, price_col):
        """
        Prepare data for Prophet
        
        Args:
            df: DataFrame with price data
            platform_col: column name for platform
            date_col: column name for dates
            price_col: column name for prices
            
        Returns:
            dict: {platform: DataFrame in Prophet format}
        """
        prepared_data = {}
        
        if date_col not in df.columns or price_col not in df.columns:
            return prepared_data
        
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col, price_col])
        
        if platform_col in df.columns:
            platforms = df[platform_col].unique()
        else:
            platforms = ['Platform_1']
        
        for platform in platforms:
            if platform_col in df.columns:
                platform_data = df[df[platform_col] == platform].copy()
            else:
                platform_data = df.copy()
            
            platform_data = platform_data.sort_values(date_col)
            prophet_df = pd.DataFrame({
                'ds': platform_data[date_col],
                'y': platform_data[price_col]
            })
            
            # Remove duplicates and keep the latest value
            prophet_df = prophet_df.drop_duplicates(subset=['ds'], keep='last')
            prophet_df = prophet_df.sort_values('ds')
            
            if len(prophet_df) >= 2:
                prepared_data[str(platform)] = prophet_df
        
        return prepared_data
    
    def forecast(self, prepared_data, periods=90):
        """
        Generate price forecast for given periods
        
        Args:
            prepared_data: dict from prepare_data method
            periods: number of periods to forecast (default 90 days)
            
        Returns:
            dict: {platform: forecast DataFrame}
        """
        for platform, data in prepared_data.items():
            try:
                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False,
                    interval_width=0.95
                )
                model.fit(data)
                
                future = model.make_future_dataframe(periods=periods)
                forecast = model.predict(future)
                
                self.models[platform] = model
                self.forecasts[platform] = forecast
            except Exception as e:
                print(f"Error forecasting for {platform}: {str(e)}")
        
        return self.forecasts
    
    def get_forecast_dataframe(self, platform):
        """Get forecast data for a specific platform"""
        if platform in self.forecasts:
            forecast = self.forecasts[platform]
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        return None


class SalesForecastor:
    """Prophet-based sales forecasting for multiple platforms"""
    
    def __init__(self, product_name):
        self.product_name = product_name
        self.models = {}
        self.forecasts = {}
        
    def prepare_data(self, df, platform_col, date_col, sales_col):
        """
        Prepare data for Prophet
        
        Args:
            df: DataFrame with sales data
            platform_col: column name for platform
            date_col: column name for dates
            sales_col: column name for sales/quantity
            
        Returns:
            dict: {platform: DataFrame in Prophet format}
        """
        prepared_data = {}
        
        if date_col not in df.columns or sales_col not in df.columns:
            return prepared_data
        
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col, sales_col])
        
        if platform_col in df.columns:
            platforms = df[platform_col].unique()
        else:
            platforms = ['Platform_1']
        
        for platform in platforms:
            if platform_col in df.columns:
                platform_data = df[df[platform_col] == platform].copy()
            else:
                platform_data = df.copy()
            
            platform_data = platform_data.sort_values(date_col)
            
            # Aggregate by date if multiple entries per date
            prophet_df = platform_data.groupby(date_col)[sales_col].sum().reset_index()
            prophet_df.columns = ['ds', 'y']
            prophet_df = prophet_df.sort_values('ds')
            
            if len(prophet_df) >= 2:
                prepared_data[str(platform)] = prophet_df
        
        return prepared_data
    
    def forecast(self, prepared_data, periods=90):
        """
        Generate sales forecast for given periods
        
        Args:
            prepared_data: dict from prepare_data method
            periods: number of periods to forecast (default 90 days)
            
        Returns:
            dict: {platform: forecast DataFrame}
        """
        for platform, data in prepared_data.items():
            try:
                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False,
                    interval_width=0.95,
                    changepoint_prior_scale=0.05
                )
                model.fit(data)
                
                future = model.make_future_dataframe(periods=periods)
                forecast = model.predict(future)
                
                # Ensure non-negative forecasts for sales
                forecast['yhat'] = forecast['yhat'].clip(lower=0)
                forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
                
                self.models[platform] = model
                self.forecasts[platform] = forecast
            except Exception as e:
                print(f"Error forecasting sales for {platform}: {str(e)}")
        
        return self.forecasts
    
    def get_forecast_dataframe(self, platform):
        """Get forecast data for a specific platform"""
        if platform in self.forecasts:
            forecast = self.forecasts[platform]
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        return None
