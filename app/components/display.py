import streamlit as st
from .visualizations import (
    create_keyword_chart,
    create_skill_match_chart,
    create_project_relevance_chart,
    create_keyword_table
)

def display_github_project(project, languages, stars, forks):
    """Display individual GitHub project details"""
    with st.expander(f"📂 {project['ProjectName']} - Relevance: {project['Relevance']}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Recommended Description:**")
            st.write(project['RecommendedDescription'])
            
            st.write("**Key Skills:**")
            skills_cols = st.columns(3)
            for i, skill in enumerate(project['KeySkills']):
                skills_cols[i % 3].markdown(f"- {skill}")
        
        with col2:
            st.metric("Impact Score", project['ImpactScore'])
            if languages:
                st.write("**Languages:**")
                for lang, percentage in languages.items():
                    st.write(f"- {lang}: {percentage}%")
            st.metric("Stars", stars)
            st.metric("Forks", forks)

def display_improvement_suggestions(response_dict, github_data=None):
    """Display resume improvement suggestions"""
    st.subheader("📈 Resume Improvement Suggestions")
    
    tabs = st.tabs(["General Improvements", "Skills Enhancement", "Project Highlights"])
    
    with tabs[0]:
        st.markdown("### General Suggestions")
        st.markdown("""
        1. **Format and Structure**
           - Use clear section headings
           - Maintain consistent formatting
           - Keep to 1-2 pages
           
        2. **Content Organization**
           - Place most relevant experience first
           - Use bullet points for clarity
           - Quantify achievements where possible
        """)
        
        if float(response_dict['JD Match'].replace('%', '')) < 85:
            st.warning("⚠️ Your resume needs significant alignment with the job requirements")
    
    with tabs[1]:
        st.markdown("### Skills to Highlight")
        missing_skills = response_dict.get('MissingKeywords', [])
        if missing_skills:
            st.markdown("**Add these key skills:**")
            cols = st.columns(2)
            for i, skill in enumerate(missing_skills):
                cols[i % 2].markdown(f"- {skill}")
    
    with tabs[2]:
        st.markdown("### Project Recommendations")
        if github_data:
            st.markdown("**GitHub Projects to Highlight:**")
            for repo in github_data[:3]:
                with st.expander(f"🔍 {repo['name']}"):
                    st.markdown(f"**Description:** {repo['description']}")
                    st.markdown("**Suggested Bullet Points:**")
                    st.markdown(f"- Developed {repo['name']} using {', '.join(list(repo['languages'].keys())[:3])}")
                    st.markdown(f"- Implemented features resulting in {repo['stars']} stars and {repo['forks']} forks")

def display_results(response_dict, github_data=None, include_github=False):
    """Main function to display all analysis results"""
    st.header("📊 Resume Analysis Results")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        match_percentage = response_dict["JD Match"].replace("%", "")
        st.metric(
            label="JD Match",
            value=f"{match_percentage}%",
            delta=None
        )
    
    # Display skill match chart
    fig_skills = create_skill_match_chart(response_dict)
    st.plotly_chart(fig_skills, use_container_width=True)
    
    # Display Missing Keywords section with switchable view
    st.subheader("🎯 Missing Keywords")
    if response_dict["MissingKeywords"]:
        view_type = st.radio(
            "Select View",
            ["Graph View", "Table View"],
            horizontal=True,
            key="keywords_view"
        )
        
        if view_type == "Graph View":
            fig = create_keyword_chart(response_dict["MissingKeywords"])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:  # Table View
            df = create_keyword_table(response_dict["MissingKeywords"])
            if df is not None:
                st.dataframe(
                    df,
                    column_config={
                        "Missing Keywords": st.column_config.TextColumn("Missing Keywords", width="medium"),
                        "Impact": st.column_config.TextColumn("Impact Level", width="small"),
                        "Suggested Implementation": st.column_config.TextColumn("Where to Add", width="large")
                    },
                    use_container_width=True
                )
    else:
        st.success("No missing keywords found!")
    
    # Display Profile Summary
    st.subheader("📋 Profile Summary")
    st.info(response_dict["Profile Summary"])
    
    # Display GitHub Analysis if available
    if include_github and "GitHub Analysis" in response_dict:
        st.header("🐙 GitHub Projects Analysis")
        github_analysis = response_dict["GitHub Analysis"]
        
        # Display overall GitHub score
        if "OverallGitHubScore" in github_analysis:
            st.metric("Overall GitHub Profile Score", github_analysis["OverallGitHubScore"])
        
        # Display recommendations
        if "Recommendations" in github_analysis:
            st.info(github_analysis["Recommendations"])
        
        # Create project relevance chart
        if "RecommendedProjects" in github_analysis:
            fig = create_project_relevance_chart(github_analysis["RecommendedProjects"])
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed project information
            for project in github_analysis["RecommendedProjects"]:
                github_project = next(
                    (p for p in github_data if p["name"] == project["ProjectName"]),
                    {"languages": {}, "stars": 0, "forks": 0}
                )
                display_github_project(
                    project,
                    github_project.get("languages", {}),
                    github_project.get("stars", 0),
                    github_project.get("forks", 0)
                )
    
    # Display improvement suggestions
    display_improvement_suggestions(response_dict, github_data) 