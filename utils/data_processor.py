from typing import Dict, List
import re
from datetime import datetime

class DataProcessor:
    def __init__(self):
        pass
    
    def process_research_data(self, raw_data: Dict) -> Dict:
        """Process and clean raw research data"""
        
        processed_data = {
            'person': self._process_person_data(raw_data['person']),
            'company': self._process_company_data(raw_data['company']),
            'insights': self._process_insights_data(raw_data['insights']),
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'total_sources': self._count_total_sources(raw_data)
            }
        }
        
        return processed_data
    
    def _process_person_data(self, person_data: Dict) -> Dict:
        """Process person-specific data"""
        
        analysis = person_data.get('analysis', {})
        
        return {
            'name': person_data.get('name', ''),
            'company': person_data.get('company', ''),
            'type': analysis.get('type', 'unknown'),
            'analysis': self._clean_text(analysis.get('analysis', '')),
            'key_points': self._extract_key_points(analysis.get('analysis', '')),
            'sources_count': len(person_data.get('raw_results', []))
        }
    
    def _process_company_data(self, company_data: Dict) -> Dict:
        """Process company-specific data"""
        
        analysis = company_data.get('analysis', {})
        
        return {
            'name': company_data.get('name', ''),
            'type': analysis.get('type', 'unknown'),
            'analysis': self._clean_text(analysis.get('analysis', '')),
            'key_points': self._extract_key_points(analysis.get('analysis', '')),
            'sources_count': len(company_data.get('raw_results', []))
        }
    
    def _process_insights_data(self, insights_data: Dict) -> Dict:
        """Process insights and opinions data"""
        
        social_analysis = insights_data.get('social_analysis', {})
        
        return {
            'insights': self._clean_text(social_analysis.get('insights', '')),
            'key_opinions': self._extract_opinions(social_analysis.get('insights', '')),
            'sources_count': len(insights_data.get('raw_results', []))
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and format text content"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might cause formatting issues
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)\"\'\/]', '', text)
        
        # Trim
        text = text.strip()
        
        return text
    
    def _extract_key_points(self, analysis: str) -> List[str]:
        """Extract key points from analysis text"""
        if not analysis:
            return []
        
        # Look for numbered lists or bullet points
        key_points = []
        
        # Pattern for numbered items (1. 2. 3. etc.)
        numbered_pattern = r'\d+\.\s*([^\.]+(?:\.[^0-9][^\.]*)*)'
        numbered_matches = re.findall(numbered_pattern, analysis)
        key_points.extend(numbered_matches)
        
        # Pattern for bullet points (- * • etc.)
        bullet_pattern = r'[-\*•]\s*([^\n\r]+)'
        bullet_matches = re.findall(bullet_pattern, analysis)
        key_points.extend(bullet_matches)
        
        # Clean and filter key points
        cleaned_points = []
        for point in key_points:
            cleaned_point = point.strip()
            if len(cleaned_point) > 10 and len(cleaned_point) < 200:  # Reasonable length
                cleaned_points.append(cleaned_point)
        
        return cleaned_points[:5]  # Limit to top 5 points
    
    def _extract_opinions(self, insights: str) -> List[str]:
        """Extract key opinions and viewpoints"""
        if not insights:
            return []
        
        opinions = []
        
        # Look for opinion indicators
        opinion_patterns = [
            r'believes?\s+that\s+([^\.]+)',
            r'thinks?\s+([^\.]+)',
            r'opinion\s+(?:is\s+)?(?:that\s+)?([^\.]+)',
            r'view\s+(?:is\s+)?(?:that\s+)?([^\.]+)',
            r'perspective\s+(?:is\s+)?(?:that\s+)?([^\.]+)'
        ]
        
        for pattern in opinion_patterns:
            matches = re.findall(pattern, insights, re.IGNORECASE)
            opinions.extend(matches)
        
        # Clean opinions
        cleaned_opinions = []
        for opinion in opinions:
            cleaned_opinion = opinion.strip()
            if len(cleaned_opinion) > 15 and len(cleaned_opinion) < 150:
                cleaned_opinions.append(cleaned_opinion)
        
        return list(set(cleaned_opinions))[:3]  # Unique opinions, top 3
    
    def _count_total_sources(self, raw_data: Dict) -> int:
        """Count total number of sources used"""
        total = 0
        
        person_results = raw_data.get('person', {}).get('raw_results', [])
        company_results = raw_data.get('company', {}).get('raw_results', [])
        insights_results = raw_data.get('insights', {}).get('raw_results', [])
        
        total = len(person_results) + len(company_results) + len(insights_results)
        
        return total
    
    def extract_contact_info(self, search_results: List[Dict]) -> Dict:
        """Extract potential contact information"""
        contact_info = {
            'twitter': [],
            'linkedin': [],
            'email': [],
            'website': []
        }
        
        for result in search_results:
            content = result.get('content', '') + ' ' + result.get('url', '')
            
            # Twitter handles
            twitter_matches = re.findall(r'@([a-zA-Z0-9_]+)', content)
            contact_info['twitter'].extend(twitter_matches)
            
            # LinkedIn profiles
            linkedin_matches = re.findall(r'linkedin\.com/in/([a-zA-Z0-9\-]+)', content)
            contact_info['linkedin'].extend(linkedin_matches)
            
            # Email addresses
            email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
            contact_info['email'].extend(email_matches)
            
            # Personal websites
            if any(domain in content for domain in ['.com', '.org', '.net']):
                url = result.get('url', '')
                if url and not any(social in url for social in ['twitter', 'linkedin', 'facebook']):
                    contact_info['website'].append(url)
        
        # Remove duplicates and limit results
        for key in contact_info:
            contact_info[key] = list(set(contact_info[key]))[:3]
        
        return contact_info