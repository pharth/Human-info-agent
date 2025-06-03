from typing import Dict, List
from tools.web_search import WebSearchTool
from tools.llm_analyzer import LLMAnalyzer
from utils.report_generator import ReportGenerator
from utils.data_processor import DataProcessor

class ResearchAgent:
    def __init__(self):
        self.web_search = WebSearchTool()
        self.llm_analyzer = LLMAnalyzer()
        self.report_generator = ReportGenerator()
        self.data_processor = DataProcessor()
    
    def research_person_and_company(self, person_name: str, company_name: str) -> Dict:
        """Main research function that orchestrates the entire process"""
        
        print(f"🔍 Starting research for {person_name} at {company_name}")
        
        # Step 1: Search for person information
        print("📊 Searching for person information...")
        person_results = self.web_search.search_person(person_name, company_name)
        
        # Step 2: Search for company information
        print("🏢 Searching for company information...")
        company_results = self.web_search.search_company(company_name)
        
        # Step 3: Search for social media and blog content
        print("💬 Searching for social content and opinions...")
        social_results = self.web_search.search_social_content(person_name)
        
        # Step 4: Analyze person data
        print("🧠 Analyzing person data...")
        person_analysis = self.llm_analyzer.analyze_person_data(
            person_name, company_name, person_results
        )
        
        # Step 5: Analyze company data
        print("🏭 Analyzing company data...")
        company_analysis = self.llm_analyzer.analyze_company_data(
            company_name, company_results, person_name
        )
        
        # Step 6: Extract opinions and insights
        print("💡 Extracting opinions and insights...")
        insights_analysis = self.llm_analyzer.extract_opinions_and_insights(
            person_name, social_results
        )
        
        # Step 7: Process and clean data
        research_data = {
            'person': {
                'name': person_name,
                'company': company_name,
                'analysis': person_analysis,
                'raw_results': person_results
            },
            'company': {
                'name': company_name,
                'analysis': company_analysis,
                'raw_results': company_results
            },
            'insights': {
                'social_analysis': insights_analysis,
                'raw_results': social_results
            }
        }
        
        processed_data = self.data_processor.process_research_data(research_data)
        
        # Step 8: Generate comprehensive report
        print("📝 Generating comprehensive report...")
        report = self.report_generator.generate_comprehensive_report(processed_data)
        
        print("✅ Research completed successfully!")
        
        return {
            'report': report,
            'raw_data': processed_data,
            'person_type': person_analysis.get('type', 'unknown'),
            'company_type': company_analysis.get('type', 'unknown')
        }
    
    def quick_research(self, person_name: str, company_name: str) -> str:
        """Quick research for basic information only"""
        
        print(f"⚡ Quick research for {person_name} at {company_name}")
        
        # Basic searches
        person_results = self.web_search.search_person(person_name, company_name)
        company_results = self.web_search.search_company(company_name)
        
        # Quick analysis
        person_analysis = self.llm_analyzer.analyze_person_data(
            person_name, company_name, person_results[:3]  # Limit results for speed
        )
        
        company_analysis = self.llm_analyzer.analyze_company_data(
            company_name, company_results[:3], person_name
        )
        
        # Generate quick report
        report = self.report_generator.generate_quick_report(
            person_name, company_name, person_analysis, company_analysis
        )
        
        return report
    
    def research_investor_focus(self, person_name: str, vc_firm: str) -> Dict:
        """Specialized research for VCs and investors"""
        
        print(f"💼 Researching investor {person_name} at {vc_firm}")
        
        # Investor-specific searches
        investor_queries = [
            f'"{person_name}" "{vc_firm}" portfolio investments',
            f'"{person_name}" investment thesis',
            f'"{vc_firm}" portfolio companies',
            f'"{vc_firm}" investment focus areas'
        ]
        
        investor_results = []
        for query in investor_queries:
            results = self.web_search.search(query, max_results=5)
            investor_results.extend(results)
        
        # Get social content for investment opinions
        social_results = self.web_search.search_social_content(person_name)
        
        # Analyze with investor focus
        analysis = self.llm_analyzer.analyze_person_data(
            person_name, vc_firm, investor_results
        )
        
        insights = self.llm_analyzer.extract_opinions_and_insights(
            person_name, social_results
        )
        
        # Generate investor-focused report
        report = self.report_generator.generate_investor_report(
            person_name, vc_firm, analysis, insights
        )
        
        return {
            'report': report,
            'investment_focus': analysis.get('analysis', ''),
            'opinions': insights.get('insights', '')
        }