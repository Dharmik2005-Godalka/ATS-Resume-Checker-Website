import re
from pypdf import PdfReader

SKILLS = [
    'python', 'java', 'javascript', 'c++', 'c#', 'php', 'sql', 'mysql',
    'postgresql', 'mongodb', 'sqlite', 'html', 'css', 'bootstrap',
    'django', 'flask', 'fastapi', 'react', 'angular', 'node.js',
    'rest api', 'json', 'git', 'github', 'docker', 'linux', 'aws',
    'pandas', 'numpy', 'machine learning', 'data analysis',
    'data structures', 'algorithms', 'oop', 'testing', 'debugging',
    'communication', 'teamwork', 'problem solving',
]

SECTIONS = {
    'Education': ['education', 'academic'],
    'Skills': ['skills', 'technical skills'],
    'Projects': ['projects', 'project'],
    'Experience': ['experience', 'internship', 'work history'],
    'Contact': ['email', 'phone', 'linkedin', 'github'],
}


def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += (page.extract_text() or '') + '\n'
    return text


def find_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r'(?<![a-z0-9+#])' + re.escape(skill) + r'(?![a-z0-9+#])'
        if re.search(pattern, text):
            found.append(skill)
    return found


def check_sections(text):
    text = text.lower()
    found = []
    for section, keywords in SECTIONS.items():
        for word in keywords:
            if word in text:
                found.append(section)
                break
    return found


def calculate_match(job_skills, resume_skills):
    found = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]
    if job_skills:
        percentage = round(len(found) / len(job_skills) * 100)
    else:
        percentage = 0
    return found, missing, percentage
