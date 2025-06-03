import google.generativeai as genai
from typing import List, Dict
from config import Config

class LLMAnalyzer:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_person_data(self, name: str, company: str, search_results: List[Dict]) -> Dict:
        """Analyze person data and extract key insights"""
        
        # Combine all search content
        content = self._combine_search_results(search_results)
        
        prompt = f"""
        Analyze the following information about {name} from {company}:
        
        {content}
        
        Extract and provide:
        1. Professional Background (role, experience, education)
        2. Key Achievements and Notable Work
        3. Investment Focus Areas (if they're an investor)
        4. Opinions and Viewpoints (from blogs, tweets, interviews)
        5. Industry Expertise and Interests
        6. Recent Activities and News
        
        Format your response as a structured analysis focusing on insights that would be valuable for a business meeting.
        Be concise but comprehensive. If this person is an investor, focus on their investment thesis and portfolio companies.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'analysis': response.text,
                'type': self._determine_person_type(response.text)
            }
        except Exception as e:
            return {
                'analysis': f"Error analyzing person data: {e}",
                'type': 'unknown'
            }
    
    def analyze_company_data(self, company: str, search_results: List[Dict], person_name: str = None) -> Dict:
        """Analyze company data and extract key insights"""
        
        content = self._combine_search_results(search_results)
        
        prompt = f"""
        Analyze the following information about {company}:
        
        {content}
        
        Extract and provide:
        1. Company Overview (what they do, business model)
        2. Industry and Market Position
        3. Key Products/Services
        4. Funding and Investment History (if available)
        5. Recent News and Developments
        6. Company Culture and Values
        7. If it's a VC firm: Investment Focus Areas and Portfolio Companies
        
        {f"Note: {person_name} is associated with this company." if person_name else ""}
        
        Format as a structured business analysis. Focus on information relevant for understanding the company's strategy and market position.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'analysis': response.text,
                'type': self._determine_company_type(response.text)
            }
        except Exception as e:
            return {
                'analysis': f"Error analyzing company data: {e}",
                'type': 'unknown'
            }
    
    def extract_opinions_and_insights(self, name: str, social_results: List[Dict]) -> Dict:
        """Extract opinions and insights from social media and blog content"""
        
        content = self._combine_search_results(social_results)
        
        if not content.strip():
            return {'insights': 'No social media or blog content found.'}
        
        prompt = f"""
        Analyze the following social media posts, blog articles, and public statements by {name}:
        
        {content}
        
        Extract:
        1. Key Opinions and Viewpoints
        2. Industry Perspectives and Predictions
        3. Investment Philosophy (if applicable)
        4. Recent Thoughts and Commentary
        5. Areas of Expertise and Interest
        
        Focus on understanding their thought process, priorities, and professional perspectives.
        This analysis will help in preparing for a business meeting with this person.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {'insights': response.text}
        except Exception as e:
            return {'insights': f"Error analyzing social content: {e}"}
    
    def _combine_search_results(self, results: List[Dict]) -> str:
        """Combine search results into a single text block"""
        combined = ""
        for result in results:
            title = result.get('title', '')
            content = result.get('content', '')
            url = result.get('url', '')
            
            combined += f"Title: {title}\n"
            combined += f"Content: {content}\n"
            combined += f"Source: {url}\n"
            combined += "-" * 50 + "\n"
            
        return combined
    
    def _determine_person_type(self, analysis: str) -> str:
        """Determine if person is investor, founder, executive, etc."""
        analysis_lower = analysis.lower()
        
        if any(term in analysis_lower for term in ['investor', 'venture capital', 'vc', 'investment']):
            return 'investor'
        elif any(term in analysis_lower for term in ['founder', 'ceo', 'co-founder']):
            return 'founder'
        elif any(term in analysis_lower for term in ['executive', 'cto', 'cfo', 'vp']):
            return 'executive'
        else:
            return 'professional'
    
    def _determine_company_type(self, analysis: str) -> str:
        """Determine company type (startup, vc, enterprise, etc.)"""
        analysis_lower = analysis.lower()
        
        if any(term in analysis_lower for term in ['venture capital', 'vc firm', 'investment fund']):
            return 'vc_firm'
        elif any(term in analysis_lower for term in ['startup', 'early stage']):
            return 'startup'
        else:
            return 'company'