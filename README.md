# Smart ATS - Resume Analyzer

A powerful ATS (Applicant Tracking System) that analyzes resumes against job descriptions and provides comprehensive feedback using AI. The system also integrates with GitHub to analyze your projects and provide tailored recommendations.

## Features

- 📊 ATS Compatibility Analysis
- 🎯 Missing Keywords Detection
- 📈 Skill Match Visualization
- 🐙 GitHub Project Analysis
- 📋 Detailed Improvement Suggestions
- 📊 Interactive Visualizations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-ats.git
cd smart-ats
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_personal_access_token
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app/main.py
```

2. Upload your resume (PDF format)
3. Paste the job description
4. (Optional) Add your GitHub username for comprehensive analysis
5. Click "Analyze" to get detailed feedback

## Project Structure

```
ATS-llm/
├── app/
│   ├── __init__.py
│   ├── main.py           # Main Streamlit app
│   ├── config.py         # Configuration and environment setup
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── pdf_utils.py  # PDF handling functions
│   │   └── github_utils.py  # GitHub API utilities
│   ├── models/
│   │   ├── __init__.py
│   │   └── gemini.py     # Gemini API handling
│   ├── components/
│   │   ├── __init__.py
│   │   ├── visualizations.py  # All plotting functions
│   │   ├── display.py    # Display components
│   │   └── sidebar.py    # Sidebar components
│   └── prompts/
│       ├── __init__.py
│       └── templates.py   # All prompt templates
├── requirements.txt
└── README.md
```

## Features in Detail

### 1. Resume Analysis
- ATS compatibility score
- Keyword matching
- Skills assessment
- Format and structure analysis

### 2. GitHub Integration
- Repository analysis
- Project relevance scoring
- Language distribution
- Impact metrics (stars, forks)

### 3. Visualizations
- Skill match charts
- Missing keywords visualization
- Project relevance graphs
- Interactive tables

### 4. Improvement Suggestions
- Keyword recommendations
- Format improvements
- Project highlights
- Content organization tips

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini API for AI analysis
- GitHub API for repository analysis
- Streamlit for the web interface
- All contributors and users of the project 