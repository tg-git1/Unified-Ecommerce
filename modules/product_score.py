import pandas as pd
import numpy as np


class ProductScoreCalculator:
    """Calculate overall product score based on multiple factors"""
    
    def __init__(self):
        self.weights = {
            'fake_reviews': 0.25,      # 25% - Trust/Quality
            'price_stability': 0.20,   # 20% - Price reliability
            'sales_trend': 0.20,       # 20% - Product popularity
            'eco_friendliness': 0.20,  # 20% - Environmental impact
            'platform_reliability': 0.15  # 15% - Platform reliability
        }
    
    def normalize_score(self, value, min_val, max_val, invert=False):
        """Normalize a value to 0-100 scale"""
        if max_val == min_val:
            return 50
        
        normalized = ((value - min_val) / (max_val - min_val)) * 100
        
        if invert:
            normalized = 100 - normalized
        
        return np.clip(normalized, 0, 100)
    
    def calculate_fake_review_score(self, fake_review_percentage):
        """
        Calculate score based on fake review percentage
        Lower fake review % = Higher score
        
        Args:
            fake_review_percentage: percentage of fake reviews (0-100)
            
        Returns:
            score (0-100)
        """
        # Invert so that lower fake % = higher score
        score = 100 - fake_review_percentage
        return np.clip(score, 0, 100)
    
    def calculate_price_stability_score(self, price_forecast, lookback_days=30):
        """
        Calculate score based on price stability
        Lower variance = Higher score
        
        Args:
            price_forecast: DataFrame with forecast data (yhat column)
            lookback_days: number of days to analyze
            
        Returns:
            score (0-100)
        """
        if price_forecast is None or len(price_forecast) < 2:
            return 50  # Default if no data
        
        recent_forecast = price_forecast.head(min(lookback_days, len(price_forecast)))
        
        if len(recent_forecast) < 2:
            return 50
        
        # Calculate coefficient of variation
        mean_price = recent_forecast['yhat'].mean()
        std_price = recent_forecast['yhat'].std()
        
        if mean_price == 0:
            return 50
        
        cv = std_price / mean_price  # Coefficient of variation
        
        # Lower CV = higher score (stable price)
        # CV 0.05 → score 95, CV 0.2 → score 60, CV 0.5 → score 0
        score = max(0, 100 - (cv * 200))
        
        return np.clip(score, 0, 100)
    
    def calculate_sales_trend_score(self, sales_forecast, lookback_days=30):
        """
        Calculate score based on sales trend
        Positive trend = Higher score
        
        Args:
            sales_forecast: DataFrame with forecast data (yhat column)
            lookback_days: number of days to analyze
            
        Returns:
            score (0-100)
        """
        if sales_forecast is None or len(sales_forecast) < 2:
            return 50  # Default if no data
        
        recent_forecast = sales_forecast.head(min(lookback_days, len(sales_forecast)))
        
        if len(recent_forecast) < 2:
            return 50
        
        # Calculate trend
        x = np.arange(len(recent_forecast))
        y = recent_forecast['yhat'].values
        
        # Linear regression slope
        if len(x) < 2:
            return 50
        
        slope = np.polyfit(x, y, 1)[0]
        
        # Normalize slope to score
        # Positive slope (increasing sales) = high score
        # Negative slope (decreasing sales) = low score
        avg_sales = y.mean()
        
        if avg_sales == 0:
            return 50
        
        # Slope as percentage of average
        slope_percent = (slope / avg_sales) * 100
        
        # Map to 0-100 scale
        # +10% growth = 80 score, -10% decline = 20 score, 0% = 50 score
        score = 50 + (slope_percent * 3)
        
        return np.clip(score, 0, 100)
    
    def calculate_eco_score(self, eco_color):
        """
        Calculate score based on eco-friendliness color
        
        Args:
            eco_color: 'green', 'yellow', 'orange', or 'red'
            
        Returns:
            score (0-100)
        """
        color_scores = {
            'green': 95,
            'yellow': 60,
            'orange': 35,
            'red': 10
        }
        
        return color_scores.get(eco_color, 50)
    
    def calculate_platform_reliability_score(self, platform_name):
        """
        Calculate score based on known platform reliability
        
        Args:
            platform_name: name of the platform
            
        Returns:
            score (0-100)
        """
        # Predefined scores for major platforms
        platform_scores = {
            'amazon': 95,
            'flipkart': 90,
            'ebay': 85,
            'myntra': 88,
            'snapdeal': 75,
            'ajio': 80,
            'meesho': 70,
            'jiomart': 82
        }
        
        platform_lower = platform_name.lower().strip()
        
        for key, score in platform_scores.items():
            if key in platform_lower or platform_lower in key:
                return score
        
        # Default score for unknown platforms
        return 70
    
    def calculate_overall_score(self, fake_review_pct, price_forecast, sales_forecast, 
                               eco_color, platform_name, platform_weight=None):
        """
        Calculate overall product score
        
        Args:
            fake_review_pct: percentage of fake reviews (0-100)
            price_forecast: DataFrame with price forecast
            sales_forecast: DataFrame with sales forecast
            eco_color: eco-friendliness color rating
            platform_name: name of the platform
            platform_weight: optional custom weight for platform reliability
            
        Returns:
            overall_score (0-100)
        """
        scores = {
            'fake_reviews': self.calculate_fake_review_score(fake_review_pct),
            'price_stability': self.calculate_price_stability_score(price_forecast),
            'sales_trend': self.calculate_sales_trend_score(sales_forecast),
            'eco_friendliness': self.calculate_eco_score(eco_color),
            'platform_reliability': self.calculate_platform_reliability_score(platform_name)
        }
        
        weights = self.weights.copy()
        if platform_weight is not None:
            weights['platform_reliability'] = platform_weight
        
        # Calculate weighted average
        overall_score = sum(scores[key] * weights[key] for key in scores.keys())
        
        return overall_score, scores
    
    def get_score_interpretation(self, score):
        """
        Get interpretation of overall score
        
        Args:
            score: overall score (0-100)
            
        Returns:
            tuple: (rating, recommendation)
        """
        if score >= 90:
            return 'Excellent', 'Highly recommended! This is a top choice.'
        elif score >= 80:
            return 'Very Good', 'Great choice with strong performance.'
        elif score >= 70:
            return 'Good', 'Solid option worth considering.'
        elif score >= 60:
            return 'Fair', 'Acceptable but has some concerns.'
        elif score >= 50:
            return 'Below Average', 'Consider alternatives.'
        else:
            return 'Poor', 'Not recommended. Look for other options.'
