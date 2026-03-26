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

    # Build Education section
    education_section = ""
    for edu in resume_data.education:
        courses_str = ", ".join(sanitize_latex(course) for course in edu.courses)
        institution = sanitize_latex(edu.institution)
        location = sanitize_latex(edu.location)
        degree = sanitize_latex(edu.degree)
        gpa = sanitize_latex(edu.gpa) if edu.gpa else ""
        date_range = sanitize_latex(edu.date_range)

        education_section += f"""
\\noindent\\textbf{{{institution}}} \\hfill {location}\\par
\\noindent {degree} \\quad GPA: {gpa} \\hfill \\textbf{{{date_range}}}\\par
\\noindent\\textbf{{Relevant Coursework :}} {courses_str}

\\vspace{{2pt}}
"""

    # Build Skills section
    skills_section = ""
    for skill in resume_data.skills:
        items_str = ", ".join(sanitize_latex(item) for item in skill.items)
        category = sanitize_latex(skill.category)
        skills_section += f"""
\\noindent\\textbf{{{category}:}} {items_str}
"""

    # Build Experience section
    experience_section = ""
    for exp in resume_data.experience:
        highlights_str = ""
        for highlight in exp.highlights:
            escaped_highlight = sanitize_latex(highlight)
            highlights_str += f"""
  \\item {escaped_highlight}"""

        title = sanitize_latex(exp.title)
        location = sanitize_latex(exp.location)
        company = sanitize_latex(exp.company)
        date_range = sanitize_latex(exp.date_range)

        experience_section += f"""
\\noindent\\textbf{{{title}}} \\hfill {date_range}\\par
\\noindent {company} \\hfill {location}\\par
\\begin{{itemize}}{highlights_str}
\\end{{itemize}}

\\vspace{{2pt}}
"""

    # Build Projects section
    projects_section = ""
    for project in resume_data.projects:
        desc_items = ""
        for desc in project.description:
            desc_items += f"""
  \\item {sanitize_latex(desc)}"""

        name = sanitize_latex(project.name)
        date_range = sanitize_latex(project.date_range)

        projects_section += f"""
\\noindent\\textbf{{{name}}} \\hfill {date_range}\\par
\\begin{{itemize}}{desc_items}
\\end{{itemize}}

\\vspace{{2pt}}
"""

    # Sanitize personal info
    full_name = sanitize_latex(resume_data.personal_info.full_name)
    phone = sanitize_latex(resume_data.personal_info.phone)
    location = sanitize_latex(resume_data.personal_info.location) if hasattr(resume_data.personal_info, 'location') else ""
    email = resume_data.personal_info.email          # Don't sanitize (used in href)
    linkedin_url = resume_data.personal_info.linkedin_url  # Don't sanitize URLs
    github_url = resume_data.personal_info.github_url      # Don't sanitize URLs

    LATEX_TEMPLATE = f"""\\documentclass[9pt]{{article}}

% Page geometry - very tight margins
\\usepackage[a4paper, top=0.25in, bottom=0.25in, left=0.4in, right=0.4in]{{geometry}}

% Times New Roman font
\\usepackage{{mathptmx}}

% Packages
\\usepackage{{setspace}}
\\usepackage{{parskip}}
\\usepackage{{titlesec}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}

% Line spacing
\\setstretch{{1.05}}

% Remove paragraph indentation
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{0pt}}

% Section formatting - uppercase with rule
\\titleformat{{\\section}}{{\\normalfont\\bfseries\\uppercase}}{{}}{{0em}}{{}}[\\titlerule]
\\titlespacing*{{\\section}}{{0pt}}{{5pt}}{{2pt}}

% Custom bullet style
\\setlist[itemize]{{label={{--}}, leftmargin=1.0em, itemsep=1pt, parsep=0pt, topsep=2pt}}

% No page numbers
\\pagestyle{{empty}}

\\begin{{document}}

% HEADER
\\begin{{center}}
  {{\\large\\bfseries {full_name}}}\\par
  \\vspace{{2pt}}
  {{\\small {location} \\textbar{{}}
   \\href{{mailto:{email}}}{{{email}}} \\textbar{{}}
   {phone} \\textbar{{}}
   \\href{{{linkedin_url}}}{{LinkedIn}} \\textbar{{}}
   \\href{{{github_url}}}{{GitHub}}}}\\par
\\end{{center}}
\\vspace{{3pt}}

% EDUCATION
\\section{{Education}}
{education_section}

% TECHNICAL SKILLS
\\section{{Technical Skills}}
{skills_section}

% RELEVANT EXPERIENCE
\\section{{Relevant Experience}}
{experience_section}

% PROJECTS
\\section{{Projects}}
{projects_section}

\\end{{document}}
"""

    return LATEX_TEMPLATE