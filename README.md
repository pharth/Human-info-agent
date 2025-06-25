# Human Info Agent

An intelligent research tool that automatically gathers and analyzes information about people and companies for business meetings and networking.

## What it does

- **Person Research**: Finds professional background, achievements, and recent activities
- **Company Analysis**: Gathers business model, funding, and market position info
- **Social Insights**: Extracts opinions and viewpoints from blogs and social media
- **Meeting Prep**: Generates actionable insights for business meetings

## Quick Start

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up API keys**
Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
JINA_API_KEY=your_jina_api_key
```

3. **Run the tool**
```bash
# Interactive mode (easiest)
python main.py

# Command line mode
python main.py --person "John Doe" --company "Acme Corp"
```

## Usage Examples

### Interactive Mode
```bash
python main.py
```
Follow the prompts to enter person and company names.

### Command Line
```bash
# Full research (comprehensive)
python main.py -p "Jane Smith" -c "TechStartup Inc" -m full

# Quick research (basic info only)
python main.py -p "Jane Smith" -c "TechStartup Inc" -m quick

# Investor focus (for VCs and investors)
python main.py -p "Alex Johnson" -c "Venture Capital LLC" -m investor

# Save report to file
python main.py -p "Jane Smith" -c "TechStartup Inc" --save
```

## Research Modes

- **Full**: Comprehensive analysis with social insights and meeting prep
- **Quick**: Basic professional and company information
- **Investor**: Specialized research for VCs, focusing on investment thesis and portfolio

## API Keys Required

- **Gemini API**: For AI analysis and insights generation
- **Jina API**: For web search functionality

Get your API keys from:
- [Google AI Studio](https://makersuite.google.com/app/apikey) (Gemini)
- [Jina AI](https://jina.ai/) (Jina Search)

## Output

The tool generates structured reports including:
- Professional background and achievements
- Company analysis and market position
- Key opinions and viewpoints
- Meeting preparation recommendations
- Action items and talking points

Reports are displayed in the terminal and can be saved as Markdown files.

## Requirements

- Python 3.8+
- Internet connection for web searches
- Valid API keys for Gemini and Jina


## Notes

- All data comes from publicly available sources
- Information accuracy depends on what's available online
- Respects rate limits and API usage guidelines
- Generated reports are for informational purposes only
