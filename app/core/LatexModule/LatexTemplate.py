from app.core.model import ResumeData

def sanitize_latex(text: str) -> str:
    """Escape LaTeX special characters in user content"""
    if not isinstance(text, str):
        text = str(text)
    # Don't escape backslashes here - assume input is plain text
    # Only escape chars that are special to LaTeX
    chars = {
        '&': '\\&',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '^': '\\textasciicircum{}',
        '~': '\\textasciitilde{}',
    }
    for char, escaped in chars.items():
        text = text.replace(char, escaped)
    return text


def generate_latex(resume_data: ResumeData) -> str:
    """Generate LaTeX code from ResumeData"""
    
    # Build Education section - sanitize individual fields
    education_section = ""
    for edu in resume_data.education:
        courses_str = ", ".join(sanitize_latex(course) for course in edu.courses)
        institution = sanitize_latex(edu.institution)
        location = sanitize_latex(edu.location)
        degree = sanitize_latex(edu.degree)
        gpa = sanitize_latex(edu.gpa) if edu.gpa else ""
        date_range = sanitize_latex(edu.date_range)
        
        education_section += f"""
    \\resumeSubheading
      {{{institution}}}{{{location}}}
      {{{degree} GPA:{gpa}}}{{{date_range}}}

      \\textbf{{Courses:}}
        {courses_str}."""

    # Build Skills section
    skills_section = ""
    for skill in resume_data.skills:
        items_str = ", ".join(sanitize_latex(item) for item in skill.items)
        category = sanitize_latex(skill.category)
        skills_section += f"""
    \\resumeSubItem{{{category}}}{{{items_str}}}"""

    # Build Experience section
    experience_section = ""
    for exp in resume_data.experience:
        highlights_str = ""
        for highlight in exp.highlights:
            escaped_highlight = sanitize_latex(highlight)
            highlights_str += f"""
    \\resumeItemWithoutTitle{{{escaped_highlight}}}"""
        
        title = sanitize_latex(exp.title)
        location = sanitize_latex(exp.location)
        company = sanitize_latex(exp.company)
        date_range = sanitize_latex(exp.date_range)
        
        experience_section += f"""
    \\resumeSubheading
      {{{title}}}{{{location}}}
      {{{company}}}{{{date_range}}}
      \\resumeItemListStart
      {highlights_str}
      \\resumeItemListEnd"""

    # Build Projects section
    projects_section = ""
    for project in resume_data.projects:
        desc_items = "\n".join([f"    \\item {sanitize_latex(desc)}" for desc in project.description])
        name = sanitize_latex(project.name)
        affiliation = sanitize_latex(project.affiliation)
        date_range = sanitize_latex(project.date_range)
        
        projects_section += f"""
    \\resumeSubheading
      {{{name}}}{{}}
      {{{affiliation}}}{{{date_range}}}
    \\begin{{itemize}}
    {desc_items}
    \\end{{itemize}}"""

    # Sanitize personal info
    full_name = sanitize_latex(resume_data.personal_info.full_name)
    phone = sanitize_latex(resume_data.personal_info.phone)
    email = sanitize_latex(resume_data.personal_info.email)
    linkedin_url = resume_data.personal_info.linkedin_url  # Don't sanitize URLs (breaks href)
    linkedin_disp_name = sanitize_latex(resume_data.personal_info.linkedin_disp_name)
    github_url = resume_data.personal_info.github_url  # Don't sanitize URLs
    github_disp_name = sanitize_latex(resume_data.personal_info.github_disp_name)

    LATEX_TEMPLATE = f"""
\\documentclass[a4paper,10pt]{{article}}

\\usepackage{{latexsym}}
\\usepackage[empty]{{fullpage}}
\\usepackage{{titlesec}}
\\usepackage{{marvosym}}
\\usepackage[usenames,dvipsnames]{{color}}
\\usepackage{{enumitem}}
\\usepackage[pdftex, hidelinks]{{hyperref}}
\\usepackage{{fancyhdr}}
\\usepackage{{fontawesome}}
\\usepackage{{xcolor}}
\\usepackage{{graphicx}}
\\usepackage{{geometry}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyfoot{{}}
\\renewcommand{{\\headrulewidth}}{{0pt}}
\\renewcommand{{\\footrulewidth}}{{0pt}}
\\geometry{{bottom=0.5in, right=0.75in}}

\\addtolength{{\\oddsidemargin}}{{-1in}}
\\addtolength{{\\evensidemargin}}{{-1in}}
\\addtolength{{\\textwidth}}{{1.25in}}
\\addtolength{{\\topmargin}}{{-1.25in}}
\\addtolength{{\\textheight}}{{1.25in}}

\\urlstyle{{rm}}

\\raggedbottom
\\raggedright
\\setlength{{\\tabcolsep}}{{0in}}

\\titleformat{{\\section}}{{
  \\vspace{{-8pt}}\\scshape\\raggedright\\large
}}{{}}{{0em}}{{}}[\\color{{black}}\\titlerule \\vspace{{-4pt}}]

\\newcommand{{\\resumeItem}}[2]{{
  \\item\\small{{
    \\textbf{{#1}}{{ : #2 \\vspace{{-2pt}}}}
  }}
}}

\\newcommand{{\\resumeItemWithoutTitle}}[1]{{
  \\item\\small{{
    #1 \\vspace{{-2pt}}
  }}
}}

\\newcommand{{\\resumeSubheading}}[4]{{
  \\vspace{{-1pt}}\\item
    \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
      \\textbf{{#1}} & #2 \\\\
      \\textit{{#3}} & \\textit{{#4}} \\\\
    \\end{{tabular*}}\\vspace{{-3pt}}
}}

\\newcommand{{\\resumeSubItem}}[2]{{\\resumeItem{{#1}}{{#2}}\\vspace{{-3pt}}}}

\\renewcommand{{\\labelitemii}}{{$\\circ$}}

\\newcommand{{\\resumeSubHeadingListStart}}{{\\begin{{itemize}}[leftmargin=*]}}
\\newcommand{{\\resumeSubHeadingListEnd}}{{\\end{{itemize}}}}
\\newcommand{{\\resumeItemListStart}}{{\\begin{{itemize}}}}
\\newcommand{{\\resumeItemListEnd}}{{\\end{{itemize}}\\vspace{{-5pt}}}}

\\begin{{document}}

\\begin{{center}}
    {{\\Huge \\scshape {full_name}}} \\\\[8pt]
    \\small
    \\faPhone ~ \\href{{tel:{phone}}}{{{phone}}} ~|~ 
    \\faEnvelope ~ \\href{{mailto:{email}}}{{{email}}} ~|~ 
    \\faLinkedin ~ \\href{{{linkedin_url}}}{{{linkedin_disp_name}}} ~|~ 
    \\faGithub ~ \\href{{{github_url}}}{{{github_disp_name}}}
\\end{{center}}

\\section{{Education}}
  \\resumeSubHeadingListStart
{education_section}
  \\resumeSubHeadingListEnd

\\section{{Technical Skills}}
  \\resumeSubHeadingListStart
{skills_section}
  \\resumeSubHeadingListEnd

\\section{{Experience}}
  \\resumeSubHeadingListStart
{experience_section}
\\resumeSubHeadingListEnd

\\section{{Projects}}
  \\resumeSubHeadingListStart
{projects_section}
  \\resumeSubHeadingListEnd

\\end{{document}}
"""

    return LATEX_TEMPLATE