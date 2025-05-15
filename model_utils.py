# TF-IDF, Cosine similarity and ATS scoring
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import preprocess_text
from database_config import db
import re
from rapidfuzz import fuzz

def fetch_jobs():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT job_title, required_skills FROM job_listings")
    jobs = cursor.fetchall()
    return pd.DataFrame(jobs)

def recommend_jobs(resume_text):
    jobs_df = fetch_jobs()
    jobs_df['processed_skills'] = jobs_df['required_skills'].apply(preprocess_text)

    tfidf = TfidfVectorizer()
    job_vectors = tfidf.fit_transform(jobs_df['processed_skills'])

    resume_vector = tfidf.transform([preprocess_text(resume_text)])
    similarities = cosine_similarity(resume_vector, job_vectors).flatten()

    jobs_df["similarity"] = (similarities * 100).round(2)
    top_jobs = jobs_df.sort_values("similarity", ascending=False).head(5)

    return top_jobs[['job_title', 'similarity']].to_dict('records')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def extract_skills_section(text):
    text = text.lower()
    if 'skills' in text:
        start = text.find('skills')
        end = text.find('\n\n', start)
        if end == -1:
            end = len(text)
        return text[start:end]
    return text

def extract_skills(text, skill_list, fuzzy_threshold=85):
    text = clean_text(text)
    found_skills = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)
        else:
            for word in text.split():
                if fuzz.partial_ratio(skill.lower(), word) > fuzzy_threshold:
                    found_skills.append(skill)
                    break
    return found_skills

def calculate_ats_score(resume_text, job_description):
    universal_skills = {'python', 'sql', 'git', 'linux', 'excel'}  # downweighted
    role_skills = {
        'data analyst': ['python', 'sql', 'data analysis', 'data visualization', 'power bi', 'tableau',
                         'excel', 'numpy', 'pandas', 'seaborn', 'matplotlib', 'statistics'],
        'software developer': ['java', 'python', 'c++', 'c#', 'javascript', 'html', 'css', 'react', 'nodejs',
                               'git', 'linux', 'flask', 'django', 'mongodb', 'mysql', 'postgresql'],
        'machine learning engineer': ['python', 'machine learning', 'deep learning', 'tensorflow',
                                      'pytorch', 'data analysis', 'numpy', 'pandas', 'scikit-learn', 'keras'],
        'web developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'django',
                          'flask', 'php', 'laravel', 'git', 'linux'],
        'java developer': ['java', 'spring', 'spring boot', 'hibernate', 'sql', 'mysql', 'maven', 'junit', 'git', 'linux'],
        'mobile app developer': ['android', 'kotlin', 'java', 'swift', 'ios', 'react native', 'flutter', 'dart', 'xcode'],
        'frontend developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'bootstrap', 'sass', 'less'],
        'backend developer': ['nodejs', 'django', 'flask', 'spring', 'laravel', 'sql', 'mongodb', 'mysql', 'postgresql'],
        'cybersecurity analyst': ['network security', 'vulnerability assessment', 'penetration testing', 'firewalls',
                                  'siem', 'python', 'linux', 'incident response', 'encryption', 'wireshark'],
        'devops engineer': ['aws', 'azure', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'git', 'linux', 'bash'],
        'cloud engineer': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'linux', 'python', 'git'],
        'database administrator': ['sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'sql server', 'pl/sql',
                                   'performance tuning'],
        'ai engineer': ['python', 'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'keras',
                        'nlp', 'cv'],
        'network engineer': ['cisco', 'ccna', 'routing', 'switching', 'network protocols', 'firewalls', 'vpn',
                             'wireshark'],
        'qa engineer': ['selenium', 'cypress', 'pytest', 'junit', 'testng', 'postman', 'rest api testing',
                        'manual testing', 'automation testing'],
        'business analyst': ['requirement gathering', 'sql', 'excel', 'power bi', 'tableau', 'data analysis',
                             'stakeholder management'],
        'product manager': ['roadmap planning', 'agile', 'scrum', 'kanban', 'jira', 'confluence', 'ux', 'user stories',
                            'prioritization'],
        'project manager': ['project planning', 'agile', 'scrum', 'waterfall', 'jira', 'confluence',
                            'stakeholder management'],
        'technical writer': ['documentation', 'api documentation', 'markdown', 'xml', 'dita', 'tools',
                             'technical writing'],
        'graphic designer': ['photoshop', 'illustrator', 'indesign', 'figma', 'sketch', 'adobe xd', 'creativity',
                             'branding'],
        'ui/ux designer': ['figma', 'adobe xd', 'sketch', 'prototyping', 'wireframing', 'user research',
                           'usability testing'],
        'blockchain developer': ['solidity', 'ethereum', 'smart contracts', 'web3', 'truffle', 'ganache', 'ipfs'],
        'game developer': ['unity', 'unreal engine', 'c++', 'c#', 'blender', '3d modeling', 'animation'],
        'data scientist': ['python', 'r', 'sql', 'machine learning', 'deep learning', 'data visualization',
                           'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch'],
        'data engineer': ['python', 'sql', 'spark', 'hadoop', 'aws', 'azure', 'gcp', 'airflow', 'etl',
                          'data pipelines'],
        'hr manager': ['recruitment', 'employee engagement', 'performance management', 'hr policies', 'labor laws',
                       'interviewing'],
        'accountant': ['accounting', 'bookkeeping', 'taxation', 'tally', 'quickbooks', 'financial analysis', 'excel'],
        'default': ['communication', 'problem solving', 'teamwork', 'leadership', 'time management', 'collaboration',
                    'critical thinking', 'adaptability', 'creativity', 'conflict resolution', 'decision making']
    }

    synonyms = {
        'py': 'python', 'python3': 'python', 'js': 'javascript', 'node': 'nodejs', 'c sharp': 'c#',
        'cplusplus': 'c++', 'golang': 'go', 'amazon web services': 'aws', 'google cloud platform': 'gcp',
        'ms azure': 'azure', 'sklearn': 'scikit-learn', 'keras library': 'keras', 'torch': 'pytorch',
        'tensorflow framework': 'tensorflow', 'pytorch library': 'pytorch', 'pandas library': 'pandas',
        'numpy library': 'numpy', 'seaborn library': 'seaborn', 'matplotlib library': 'matplotlib',
        'mysql server': 'mysql', 'postgres': 'postgresql', 'mssql': 'sql server', 'pl sql': 'pl/sql',
        'mongodb database': 'mongodb', 'docker container': 'docker', 'k8s': 'kubernetes',
        'terraform cli': 'terraform', 'ansible playbook': 'ansible', 'jenkins pipeline': 'jenkins',
        'linux os': 'linux', 'penetration test': 'penetration testing', 'wireshark tool': 'wireshark',
        'jira software': 'jira', 'confluence wiki': 'confluence', 'rest assured': 'rest api testing',
        'test ng': 'testng', 'pytest framework': 'pytest', 'spring boot framework': 'spring boot',
        'flask framework': 'flask', 'django framework': 'django', 'laravel framework': 'laravel',
        'vuejs': 'vue', 'reactjs': 'react', 'angularjs': 'angular', 'adobe experience designer': 'adobe xd',
        'figma app': 'figma', 'scrum master': 'scrum', 'agile methodology': 'agile', 'team player': 'teamwork',
        'problem-solving': 'problem solving', 'lead': 'leadership', 'qb': 'quickbooks', 'tally software': 'tally',
        'smart contract': 'smart contracts', 'eth': 'ethereum', 'ms excel': 'excel', 'microsoft excel': 'excel'
    }

    def guess_role(text):
        text = text.lower()
        for role in role_skills.keys():
            if role in text:
                return role
        return 'default'

    def normalize_skills(skill_list):
        return [synonyms.get(skill.lower(), skill.lower()) for skill in skill_list]

    resume_text_clean = clean_text(resume_text)
    skills_section = extract_skills_section(resume_text)
    combined_resume = resume_text_clean + " " + skills_section
    job_description_clean = clean_text(job_description)

    all_skills = set(sum(role_skills.values(), []))
    fuzzy_threshold = 85 if not job_description.strip() else 65
    resume_skills = extract_skills(combined_resume, all_skills, fuzzy_threshold)
    resume_skills = normalize_skills(resume_skills)

    if job_description.strip():
        job_skills = extract_skills(job_description, all_skills, fuzzy_threshold)
        if not job_skills:
            detected_role = guess_role(resume_text)
            job_skills = role_skills[detected_role]
    else:
        detected_role = guess_role(resume_text)
        job_skills = role_skills[detected_role]
    job_skills = normalize_skills(job_skills)

    primary_skills = set(job_skills)
    matched_primary = set(resume_skills) & primary_skills
    missing_skills = list(primary_skills - set(resume_skills))

    # 👇 Down-weight universal skills
    adjusted_matched = [s for s in matched_primary if s not in universal_skills]
    universal_matched = [s for s in matched_primary if s in universal_skills]

    skill_score = ((len(adjusted_matched) * 1.0) + (len(universal_matched) * 0.5)) / len(
        primary_skills) * 100 if primary_skills else 0

    cosine_score = 0
    if job_description.strip():
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([combined_resume, job_description_clean])
        cosine_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100

        # 👇 Heavy penalty for unrelated JD
        if cosine_score < 20:
            skill_score *= 0.5

    ats_score = (0.8 * skill_score) + (0.2 * cosine_score)
    return round(ats_score, 2), missing_skills

def suggest_improvements(resume_text):
    # Simple logic to simulate improvement suggestions
    required_keywords = ["teamwork", "communication", "python", "sql", "leadership", "problem-solving"]
    resume_words = preprocess_text(resume_text).split()

    missing = [word.capitalize() for word in required_keywords if word.lower() not in resume_words]
    return missing