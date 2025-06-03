import requests
from typing import List, Dict
from config import Config

class WebSearchTool:
    def __init__(self):
        self.api_key = Config.JINA_API_KEY
        self.base_url = Config.JINA_SEARCH_URL
        
    def search(self, query: str, max_results: int = None) -> List[Dict]:
        """Search the web using Jina API"""
        if not max_results:
            max_results = Config.MAX_SEARCH_RESULTS
            
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Use Jina's search format
        search_url = f"{self.base_url}{query}"
        
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            
            # Parse Jina response
            content = response.text
            results = self._parse_jina_response(content, query)
            
            return results[:max_results]
            
        except requests.RequestException as e:
            print(f"Search error: {e}")
            return []
    
    def _parse_jina_response(self, content: str, query: str) -> List[Dict]:
        """Parse Jina API response into structured format"""
        # Simple parsing - you might need to adjust based on actual Jina response format
        lines = content.split('\n')
        results = []
        
        current_result = {}
        for line in lines:
            if line.strip():
                if '**' in line:  # Title
                    if current_result:
                        results.append(current_result)
                        current_result = {}
                    current_result['title'] = line.strip('*').strip()
                elif line.startswith('http'):  # URL
                    current_result['url'] = line.strip()
                else:  # Content
                    if 'content' not in current_result:
                        current_result['content'] = ""
                    current_result['content'] += line + " "
        
        if current_result:
            results.append(current_result)
            
        return results
    
    def search_person(self, name: str, company: str = None) -> List[Dict]:
        """Search for information about a person"""
        queries = [
            f'"{name}" bio profile',
            f'"{name}" background experience',
        ]
        
        if company:
            queries.append(f'"{name}" "{company}"')
            
        all_results = []
        for query in queries:
            results = self.search(query, max_results=5)
            all_results.extend(results)
            
        return self._deduplicate_results(all_results)
    
    def search_company(self, company: str) -> List[Dict]:
        """Search for information about a company"""
        queries = [
            f'"{company}" company about',
            f'"{company}" business model',
            f'"{company}" funding investment'
        ]
        
        all_results = []
        for query in queries:
            results = self.search(query, max_results=5)
            all_results.extend(results)
            
        return self._deduplicate_results(all_results)
    
    def search_social_content(self, name: str) -> List[Dict]:
        """Search for social media content and blogs"""
        queries = [
            f'"{name}" twitter tweet',
            f'"{name}" blog post article',
            f'"{name}" linkedin post',
            f'"{name}" medium article'
        ]
        
        all_results = []
        for query in queries:
            results = self.search(query, max_results=3)
            all_results.extend(results)
            
        return self._deduplicate_results(all_results)
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate results based on URL"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
                
        return unique_results