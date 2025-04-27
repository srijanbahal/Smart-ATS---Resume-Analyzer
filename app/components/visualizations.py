import plotly.express as px
import pandas as pd

def create_keyword_chart(keywords):
    """Create bar chart for missing keywords"""
    if not keywords:
        return None
    df = pd.DataFrame({
        'Keyword': keywords,
        'Count': [1] * len(keywords)
    })
    fig = px.bar(df, x='Keyword', y='Count', title='Missing Keywords')
    fig.update_layout(showlegend=False)
    return fig

def create_skill_match_chart(response_dict):
    """Create bar chart for skill matches"""
    skills_data = {
        'Technical Skills': float(response_dict['JD Match'].replace('%', '')),
        'Project Experience': float(response_dict.get('ProjectMatch', '60').replace('%', '')),
        'Work Experience': float(response_dict.get('WorkExpMatch', '70').replace('%', '')),
        'Education': float(response_dict.get('EduMatch', '80').replace('%', '')),
    }
    
    df = pd.DataFrame({
        'Category': list(skills_data.keys()),
        'Match Percentage': list(skills_data.values())
    })
    
    fig = px.bar(df, x='Category', y='Match Percentage',
                 title='Resume Component Match Analysis',
                 labels={'Match Percentage': 'Match %'},
                 color='Match Percentage',
                 color_continuous_scale='viridis')
    
    fig.update_layout(yaxis_range=[0, 100])
    return fig

def create_project_relevance_chart(projects):
    """Create bar chart for project relevance"""
    df = pd.DataFrame([
        {
            'Project': p['ProjectName'],
            'Relevance': float(p['Relevance'].strip('%')),
            'Impact': float(p['ImpactScore'].split('/')[0])
        } for p in projects
    ])
    
    fig = px.bar(df, x='Project', y=['Relevance', 'Impact'],
                 title='Project Relevance and Impact',
                 barmode='group')
    return fig

def create_keyword_table(keywords):
    """Create table for missing keywords"""
    if not keywords:
        return None
    df = pd.DataFrame({
        'Missing Keywords': keywords,
        'Impact': ['High'] * len(keywords),
        'Suggested Implementation': [
            'Add to Skills/Technologies section' if 'framework' in kw.lower() or 'language' in kw.lower() or 'tool' in kw.lower()
            else 'Include in Work Experience' if 'experience' in kw.lower() or 'year' in kw.lower()
            else 'Add to Project Highlights' if 'project' in kw.lower() or 'develop' in kw.lower()
            else 'General Addition'
            for kw in keywords
        ]
    })
    return df 