import logging
import re
from typing import Dict

logger = logging.getLogger(__name__)

class AITicketService:
    def __init__(self):
        self.urgency_keywords = {
            'critical': ['urgent', 'critical', 'emergency', 'broken', 'down', 'not working', 'outage', 'asap'],
            'high': ['important', 'issue', 'problem', 'error', 'failed', 'cannot', "can't", 'help'],
            'medium': ['question', 'advice', 'information', 'how to'],
            'low': ['suggestion', 'feedback', 'feature request', 'improvement']
        }
        
        self.category_keywords = {
            'technical': ['login', 'password', 'error', 'bug', 'crash', 'not working', 'slow', 'loading', 'connection'],
            'billing': ['payment', 'invoice', 'charge', 'refund', 'billing', 'price', 'cost', 'fee'],
            'account': ['account', 'profile', 'settings', 'delete', 'suspend', 'register', 'sign up'],
            'feature': ['feature', 'request', 'suggestion', 'improvement', 'add', 'new functionality'],
            'general': ['help', 'question', 'information', 'how to', 'guide']
        }
        
        self.negative_words = ['not working', 'broken', 'error', 'bad', 'terrible', 'frustrated', 'angry', 'mad', 'hate']
        self.positive_words = ['thanks', 'thank you', 'good', 'great', 'excellent', 'helpful', 'awesome', 'love', 'perfect']
        
    def analyze_ticket(self, subject: str, description: str) -> Dict:
        """Analyze ticket content using rule-based approach"""
        try:
            full_text = f"{subject}. {description}".lower()
            
            # Simple sentiment analysis
            sentiment, sentiment_score = self._analyze_sentiment(full_text)
            
            # Urgency detection
            urgency = self._detect_urgency(full_text)
            
            # Category prediction
            category = self._predict_category(full_text)
            
            # Overall confidence
            confidence = self._calculate_confidence(full_text)
            
            return {
                'urgency': urgency,
                'sentiment': sentiment,
                'sentiment_score': sentiment_score,
                'category': category,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._fallback_analysis(subject, description)
    
    def _analyze_sentiment(self, text: str) -> tuple:
        """Simple sentiment analysis using keyword counting"""
        negative_count = sum(1 for word in self.negative_words if word in text)
        positive_count = sum(1 for word in self.positive_words if word in text)
        
        if negative_count > positive_count:
            return "NEGATIVE", min(0.3 + (negative_count * 0.1), 0.9)
        elif positive_count > negative_count:
            return "POSITIVE", min(0.3 + (positive_count * 0.1), 0.9)
        else:
            return "NEUTRAL", 0.5
    
    def _detect_urgency(self, text: str) -> int:
        """Detect urgency level from 1-5"""
        urgency_score = 1
        
        # Keyword-based urgency detection
        critical_matches = sum(1 for keyword in self.urgency_keywords['critical'] if keyword in text)
        high_matches = sum(1 for keyword in self.urgency_keywords['high'] if keyword in text)
        medium_matches = sum(1 for keyword in self.urgency_keywords['medium'] if keyword in text)
        
        if critical_matches > 0:
            urgency_score = 5
        elif high_matches > 1:
            urgency_score = 4
        elif high_matches > 0 or medium_matches > 1:
            urgency_score = 3
        elif medium_matches > 0:
            urgency_score = 2
            
        # Boost for explicit urgency markers
        if any(marker in text for marker in ['urgent', 'asap', 'immediately', 'right away']):
            urgency_score = max(urgency_score, 4)
            
        # Boost for system down language
        if any(phrase in text for phrase in ['not working', 'broken', 'down', 'outage']):
            urgency_score = max(urgency_score, 4)
            
        return min(urgency_score, 5)
    
    def _predict_category(self, text: str) -> str:
        """Predict ticket category based on keyword matching"""
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
            
        # Return category with highest score, default to general
        best_category = max(category_scores.items(), key=lambda x: x[1])
        return best_category[0] if best_category[1] > 0 else 'general'
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate overall confidence score based on text complexity"""
        word_count = len(text.split())
        
        # More words = higher confidence (to a point)
        length_confidence = min(word_count / 30, 1.0)
        
        # More unique keywords found = higher confidence
        unique_keywords = sum(1 for keyword_list in self.urgency_keywords.values() for keyword in keyword_list if keyword in text)
        keyword_confidence = min(unique_keywords / 5, 1.0)
        
        overall_confidence = (length_confidence + keyword_confidence) / 2
        
        return min(overall_confidence, 0.95)
    
    def _fallback_analysis(self, subject: str, description: str) -> Dict:
        """Simple fallback when analysis fails"""
        text = f"{subject} {description}".lower()
        
        return {
            'urgency': self._detect_urgency(text),
            'sentiment': 'NEUTRAL',
            'sentiment_score': 0.5,
            'category': self._predict_category(text),
            'confidence': 0.6
        }

# Global instance
ai_service = AITicketService()