import pandas as pd
import numpy as np
import math


class CarbonEmissionsCalculator:
    """Calculate carbon emissions based on warehouse and user pin codes"""
    
    # Approximate coordinates for Indian pin codes (latitude, longitude)
    PIN_CODE_COORDINATES = {
        # Major metro areas - these are examples
        '110001': (28.6139, 77.2090),  # Delhi
        '400001': (19.0760, 72.8777),  # Mumbai
        '560001': (12.9716, 77.5946),  # Bangalore
        '700001': (22.5726, 88.3639),  # Kolkata
        '600001': (13.0827, 80.2707),  # Chennai
    }
    
    # Carbon emissions per km per kg of product
    # Different for different modes of transport
    EMISSION_FACTORS = {
        'air': 0.255,      # kg CO2 per ton-km → 0.255 g CO2 per kg-km
        'rail': 0.041,     # kg CO2 per ton-km → 0.041 g CO2 per kg-km
        'road': 0.084,     # kg CO2 per ton-km → 0.084 g CO2 per kg-km
        'ship': 0.010      # kg CO2 per ton-km → 0.010 g CO2 per kg-km
    }
    
    def __init__(self):
        self.warehouse_data = {}
    
    def load_warehouse_data(self, csv_path):
        """Load warehouse locations from CSV"""
        try:
            df = pd.read_csv(csv_path)
            
            # Try to identify relevant columns
            pin_col = None
            platform_col = None
            
            for col in df.columns:
                if col.lower() in ['pin', 'pincode', 'pin_code', 'warehouse_pin', 'warehouse_zip_code', 'warehouse_zipcode']:
                    pin_col = col
                if col.lower() in ['platform', 'marketplace', 'seller']:
                    platform_col = col
            
            if pin_col:
                if platform_col and platform_col in df.columns:
                    for _, row in df.iterrows():
                        platform = str(row[platform_col]).strip()
                        self.warehouse_data[platform] = str(row[pin_col]).strip()
                else:
                    # Default platforms if not specified
                    if len(df) >= 1:
                        self.warehouse_data['Amazon'] = str(df[pin_col].iloc[0]).strip()
                    if len(df) >= 2:
                        self.warehouse_data['Flipkart'] = str(df[pin_col].iloc[1]).strip()
                    if len(df) >= 3:
                        self.warehouse_data['eBay'] = str(df[pin_col].iloc[2]).strip()
        except Exception as e:
            print(f"Error loading warehouse data: {str(e)}")
    
    def get_coordinates(self, pin_code):
        """Get approximate coordinates for a pin code"""
        pin_str = str(pin_code).strip()
        
        if pin_str in self.PIN_CODE_COORDINATES:
            return self.PIN_CODE_COORDINATES[pin_str]
        
        # Generate approximate coordinates based on pin code
        # This is a simplified approach - in production, use geolocation API
        lat = 10 + (hash(pin_str) % 30)
        lon = 65 + (hash(pin_str) % 40)
        
        return lat, lon
    
    def calculate_distance(self, pin1, pin2):
        """Calculate distance between two pin codes using Haversine formula"""
        lat1, lon1 = self.get_coordinates(pin1)
        lat2, lon2 = self.get_coordinates(pin2)
        
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def calculate_emissions(self, warehouse_pin, user_pin, product_weight=1.0, transport_mode='road'):
        """
        Calculate carbon emissions for a shipment
        
        Args:
            warehouse_pin: warehouse pin code
            user_pin: user's pin code
            product_weight: weight of product in kg (default 1.0)
            transport_mode: 'air', 'rail', 'road', or 'ship'
            
        Returns:
            float: CO2 emissions in kg
        """
        distance = self.calculate_distance(warehouse_pin, user_pin)
        emission_factor = self.EMISSION_FACTORS.get(transport_mode, self.EMISSION_FACTORS['road'])
        
        # Calculate emissions
        emissions = (distance * emission_factor * product_weight) / 1000  # Convert grams to kg
        
        return emissions
    
    def get_platform_emissions(self, user_pin, platforms=None, product_weight=1.0):
        """
        Calculate emissions for multiple platforms
        
        Args:
            user_pin: user's pin code
            platforms: list of platform names (if None, use all available)
            product_weight: weight of product in kg
            
        Returns:
            dict: {platform: emissions in kg}
        """
        if platforms is None:
            platforms = list(self.warehouse_data.keys())
        
        # If no warehouse data is loaded, use default platforms
        if not platforms:
            platforms = ['Amazon', 'Flipkart', 'eBay', 'Myntra', 'Ajio']
        
        emissions = {}
        
        for platform in platforms:
            if platform in self.warehouse_data:
                warehouse_pin = self.warehouse_data[platform]
                # Determine transport mode based on distance (simplified)
                distance = self.calculate_distance(warehouse_pin, user_pin)
                
                if distance > 2000:
                    mode = 'rail'
                elif distance > 500:
                    mode = 'road'
                else:
                    mode = 'road'
                
                emissions[platform] = self.calculate_emissions(warehouse_pin, user_pin, product_weight, mode)
            else:
                # Default calculation for unknown platforms
                emissions[platform] = self.calculate_emissions('110001', user_pin, product_weight, 'road')
        
        return emissions
    
    def get_eco_friendliness_rating(self, emissions):
        """
        Get eco-friendliness rating based on emissions
        
        Args:
            emissions: CO2 emissions in kg
            
        Returns:
            tuple: (rating, color, description)
        """
        if emissions < 0.5:
            return 'Excellent', 'green', f'{emissions:.3f} kg CO2 - Very Eco-Friendly'
        elif emissions < 1.0:
            return 'Good', 'green', f'{emissions:.3f} kg CO2 - Eco-Friendly'
        elif emissions < 1.5:
            return 'Moderate', 'yellow', f'{emissions:.3f} kg CO2 - Moderate Impact'
        elif emissions < 2.5:
            return 'High', 'orange', f'{emissions:.3f} kg CO2 - High Impact'
        else:
            return 'Very High', 'red', f'{emissions:.3f} kg CO2 - Very High Impact'
    
    def get_all_platform_ratings(self, user_pin, platforms=None, product_weight=1.0):
        """
        Get eco-friendliness ratings for all platforms
        
        Args:
            user_pin: user's pin code
            platforms: list of platform names
            product_weight: weight of product in kg
            
        Returns:
            dict: {platform: {'emissions': float, 'distance': float, 'rating': str, 'color': str, 'description': str}}
        """
        if platforms is None:
            platforms = list(self.warehouse_data.keys())
        
        # If no warehouse data is loaded, use default platforms
        if not platforms:
            platforms = ['Amazon', 'Flipkart', 'eBay', 'Myntra', 'Ajio']
        
        ratings = {}
        for platform in platforms:
            if platform in self.warehouse_data:
                warehouse_pin = self.warehouse_data[platform]
            else:
                # Use default warehouse for unknown platforms
                warehouse_pin = '110001'
            
            # Calculate distance
            distance = self.calculate_distance(warehouse_pin, user_pin)
            
            # Calculate emissions
            if distance > 2000:
                mode = 'rail'
            elif distance > 500:
                mode = 'road'
            else:
                mode = 'road'
            
            emissions = self.calculate_emissions(warehouse_pin, user_pin, product_weight, mode)
            
            # Get rating
            rating, color, description = self.get_eco_friendliness_rating(emissions)
            ratings[platform] = {
                'emissions': emissions,
                'distance': distance,
                'rating': rating,
                'color': color,
                'description': description
            }
        
        return ratings
