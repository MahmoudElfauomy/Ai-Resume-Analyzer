import json

KNOWLEDGE_BASE = {
    "python": {
        "roadmap": "Backend Development",
        "courses": ["FastAPI Crash Course", "Advanced Python OOP"],
    },
    "fastapi": {
        "roadmap": "API Engineering",
        "courses": ["REST APIs with FastAPI", "Asynchronous Python"],
    },
    "sql": {
        "roadmap": "Database Management",
        "courses": ["SQL & Database Design", "PostgreSQL & SQLite Basics"],
    },
    "javascript": {
        "roadmap": "Frontend Development",
        "courses": ["Modern JS ES6+", "DOM Manipulation Basics"],
    },
    "docker": {
        "roadmap": "DevOps Foundations",
        "courses": ["Docker for Beginners", "Containerization Essentials"],
    },
}

class ResumeAnalyzerAgent:
    @staticmethod
    def analyze(extracted_text: str):
        text_lower = extracted_text.lower()
        detected_skills = [
            skill for skill in KNOWLEDGE_BASE.keys() if skill in text_lower
        ]
        summary = f"تضم السيرة الذاتية نصاً بـ {len(extracted_text)} حرف. تم اكتشاف مهارات أساسية مثل: {', '.join(detected_skills) if detected_skills else 'لم تحدد بوضوح'}."
        return {"summary": summary, "skills": detected_skills}


class JobMatchingAgent:
    @staticmethod
    def calculate_match(resume_skills: list, job_required_skills: str):
        required_list = [
            s.strip().lower() for s in job_required_skills.split(",") if s.strip()
        ]
        if not required_list:
            return 0.0
        matched_skills = [s for s in required_list if s in resume_skills]
        score = (len(matched_skills) / len(required_list)) * 100
        return round(score, 2)


class CareerAdvisorAgent:
    @staticmethod
    def recommend(resume_skills: list, target_job_skills: str):
        required_list = [
            s.strip().lower() for s in target_job_skills.split(",") if s.strip()
        ]
        missing_skills = [s for s in required_list if s not in resume_skills]
        recommendations = []
        for skill in missing_skills:
            if skill in KNOWLEDGE_BASE:
                recommendations.append(
                    {
                        "missing_skill": skill,
                        "roadmap": KNOWLEDGE_BASE[skill]["roadmap"],
                        "courses": KNOWLEDGE_BASE[skill]["courses"],
                    }
                )
            else:
                recommendations.append(
                    {
                        "missing_skill": skill,
                        "roadmap": "General Tech Skills",
                        "courses": [f"Intro to {skill.capitalize()}"],
                    }
                )
        return {"missing_skills": missing_skills, "learning_resources": recommendations}
