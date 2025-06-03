import sys
import argparse
from config import Config
from agents.research_agent import ResearchAgent

def main():
    parser = argparse.ArgumentParser(description='AI Research Agent for Person and Company Analysis')
    parser.add_argument('--person', '-p', required=True, help='Person name to research')
    parser.add_argument('--company', '-c', required=True, help='Company name or website')
    parser.add_argument('--mode', '-m', choices=['full', 'quick', 'investor'], 
                       default='full', help='Research mode (default: full)')
    parser.add_argument('--save', '-s', action='store_true', help='Save report to file')
    parser.add_argument('--output', '-o', help='Output filename (optional)')
    
    args = parser.parse_args()
    
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize agent
        agent = ResearchAgent()
        
        print(f"🤖 AI Research Agent Starting...")
        print(f"📝 Person: {args.person}")
        print(f"🏢 Company: {args.company}")
        print(f"⚙️  Mode: {args.mode}")
        print("-" * 50)
        
        # Execute research based on mode
        if args.mode == 'quick':
            report = agent.quick_research(args.person, args.company)
            print(report)
            
        elif args.mode == 'investor':
            result = agent.research_investor_focus(args.person, args.company)
            print(result['report'])
            
        else:  # full mode
            result = agent.research_person_and_company(args.person, args.company)
            report = result['report']
            print(report)
            
            # Show additional info for full mode
            print(f"\n📊 Research Summary:")
            print(f"- Person Type: {result.get('person_type', 'Unknown')}")
            print(f"- Company Type: {result.get('company_type', 'Unknown')}")
        
        # Save report if requested
        if args.save:
            from utils.report_generator import ReportGenerator
            generator = ReportGenerator()
            filepath = generator.save_report(report, args.output)
            if filepath:
                print(f"\n💾 Report saved to: {filepath}")
            else:
                print("\n❌ Failed to save report")
                
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please check your .env file and API keys.")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n⏹️  Research interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def interactive_mode():
    """Interactive mode for easier usage"""
    print("🤖 AI Research Agent - Interactive Mode")
    print("=" * 50)
    
    try:
        Config.validate()
        agent = ResearchAgent()
        
        while True:
            print("\n" + "-" * 30)
            person_name = input("👤 Enter person name (or 'quit' to exit): ").strip()
            
            if person_name.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not person_name:
                print("❌ Person name cannot be empty")
                continue
                
            company_name = input("🏢 Enter company name: ").strip()
            if not company_name:
                print("❌ Company name cannot be empty")
                continue
                
            print("\n📋 Research modes:")
            print("1. Full Research (comprehensive)")
            print("2. Quick Research (basic info)")
            print("3. Investor Focus (for VCs)")
            
            mode_choice = input("Choose mode (1-3, default: 1): ").strip()
            
            mode_map = {'1': 'full', '2': 'quick', '3': 'investor', '': 'full'}
            mode = mode_map.get(mode_choice, 'full')
            
            print(f"\n🔍 Starting {mode} research...")
            print(f"📝 Person: {person_name}")
            print(f"🏢 Company: {company_name}")
            print("-" * 50)
            
            try:
                if mode == 'quick':
                    report = agent.quick_research(person_name, company_name)
                elif mode == 'investor':
                    result = agent.research_investor_focus(person_name, company_name)
                    report = result['report']
                else:
                    result = agent.research_person_and_company(person_name, company_name)
                    report = result['report']
                
                print(report)
                
                # Ask if user wants to save
                save_choice = input("\n💾 Save report to file? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    from utils.report_generator import ReportGenerator
                    generator = ReportGenerator()
                    filepath = generator.save_report(report)
                    if filepath:
                        print(f"✅ Report saved to: {filepath}")
                
            except Exception as e:
                print(f"❌ Research error: {e}")
                
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please check your .env file and API keys.")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, start interactive mode
        interactive_mode()
    else:
        # Arguments provided, use CLI mode
        main()