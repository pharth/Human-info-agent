import google.generativeai as genai
from typing import List, Dict
from config import Config

class LLMAnalyzer:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        # Updated to use current Gemini model names
        try:
            # Try the latest models first
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception:
            try:
                # Fallback to other available models
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            except Exception:
                try:
                    self.model = genai.GenerativeModel('gemini-pro-latest')
                except Exception:
                    # Last resort - try to list available models and use the first one
                    models = genai.list_models()
                    available_models = [model.name for model in models if 'generateContent' in model.supported_generation_methods]
                    if available_models:
                        model_name = available_models[0].split('/')[-1]  # Extract just the model name
                        self.model = genai.GenerativeModel(model_name)
                        print(f"Using model: {model_name}")
                    else:
                        raise Exception("No compatible Gemini models found")
    
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
            # Add safety settings and generation config
            generation_config = {
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
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
            generation_config = {
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
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
            generation_config = {
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
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
    
    def list_available_models(self):
        """Helper method to list available Gemini models"""
        try:
            models = genai.list_models()
            print("Available Gemini models:")
            for model in models:
                print(f"- {model.name} (supports: {model.supported_generation_methods})")
        except Exception as e:
            print(f"Error listing models: {e}")