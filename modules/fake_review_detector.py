import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import pickle
import os


class FakeReviewDetector:
    """XGBoost model for fake review detection"""
    
    def __init__(self, model_path=None):
        self.model = None
        self.vectorizer = None
        self.scaler = None
        self.model_path = model_path
        
    def train(self, training_data_path):
        """
        Train the XGBoost model on fake reviews
        
        Expected columns in training data:
        - review_text or text
        - label (0 = real, 1 = fake)
        """
        df = pd.read_csv(training_data_path)
        
        # Identify text and label columns
        text_col = None
        label_col = None
        
        for col in df.columns:
            if col.lower() in ['review_text', 'text', 'review', 'content']:
                text_col = col
            if col.lower() in ['label', 'is_fake', 'fake']:
                label_col = col
        
        if text_col is None or label_col is None:
            raise ValueError(f"Could not identify text and label columns. Columns: {df.columns.tolist()}")
        
        # Clean data
        df = df.dropna(subset=[text_col, label_col])
        
        # Extract text features
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
        X_text = self.vectorizer.fit_transform(df[text_col].astype(str))
        
        # Create additional features
        X_text_dense = X_text.toarray()
        
        # Calculate text features
        review_length = df[text_col].astype(str).str.len().values.reshape(-1, 1)
        word_count = df[text_col].astype(str).str.split().str.len().values.reshape(-1, 1)
        
        # Combine features
        additional_features = np.hstack([review_length, word_count])
        self.scaler = StandardScaler()
        additional_features = self.scaler.fit_transform(additional_features)
        
        X = np.hstack([X_text_dense, additional_features])
        y = df[label_col].values
        
        # Train XGBoost
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        self.model.fit(X, y)
        
        return self.model
    
    def predict(self, reviews):
        """
        Predict if reviews are fake
        
        Args:
            reviews: list of review texts or DataFrame with text column
            
        Returns:
            array of probabilities (probability of being fake)
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        if isinstance(reviews, pd.DataFrame):
            text_col = [col for col in reviews.columns if col.lower() in 
                       ['review_text', 'text', 'review', 'content']][0]
            reviews = reviews[text_col].astype(str).tolist()
        elif isinstance(reviews, str):
            reviews = [reviews]
        
        # Transform text
        X_text = self.vectorizer.transform(reviews)
        X_text_dense = X_text.toarray()
        
        # Calculate features
        review_length = np.array([len(r) for r in reviews]).reshape(-1, 1)
        word_count = np.array([len(r.split()) for r in reviews]).reshape(-1, 1)
        
        additional_features = np.hstack([review_length, word_count])
        additional_features = self.scaler.transform(additional_features)
        
        X = np.hstack([X_text_dense, additional_features])
        
        # Get probability of being fake (class 1)
        probabilities = self.model.predict_proba(X)[:, 1]
        
        return probabilities
    
    def get_fake_percentage(self, reviews, threshold=0.5):
        """
        Get percentage of fake reviews
        
        Args:
            reviews: list of review texts or DataFrame with text column
            threshold: probability threshold for considering a review fake
            
        Returns:
            tuple: (fake_percentage, fake_count, total_count)
        """
        probs = self.predict(reviews)
        fake_count = np.sum(probs >= threshold)
        total_count = len(probs)
        fake_percentage = (fake_count / total_count) * 100 if total_count > 0 else 0
        
        return fake_percentage, fake_count, total_count, probs
    
    def save(self, path):
        """Save model and vectorizer"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        model_data = {
            'model': self.model,
            'vectorizer': self.vectorizer,
            'scaler': self.scaler
        }
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load(self, path):
        """Load model and vectorizer"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        self.model = model_data['model']
        self.vectorizer = model_data['vectorizer']
        self.scaler = model_data['scaler']
