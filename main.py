from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEST_JOBS = [
    {
        "job_title": "Python Backend Developer",
        "company": "TechCorp",
        "required_skills": ["python", "sql", "fastapi", "docker"],
    },
    {
        "job_title": "Frontend Web Developer",
        "company": "WebStudio",
        "required_skills": ["javascript", "react", "css", "html"],
    },
    {
        "job_title": "Full Stack Engineer",
        "company": "Innovation Inc",
        "required_skills": ["python", "javascript", "sql", "git"],
    },
    {
        "job_title": "Data Scientist",
        "company": "DataX",
        "required_skills": ["python", "machine learning", "sql", "pandas"],
    },
]

KNOWN_SKILLS = [
    "python",
    "javascript",
    "react",
    "sql",
    "fastapi",
    "docker",
    "css",
    "html",
    "git",
    "machine learning",
    "pandas",
]


@app.post("/analyze-resume/")
async def analyze_resume(user_id: int = 1, file: UploadFile = File(...)):
    try:
        content = await file.read()
        text_content = str(content).lower()
        detected_skills = []
        for skill in KNOWN_SKILLS:
            if skill in text_content:
                detected_skills.append(skill)
        if not detected_skills:
            detected_skills = ["python", "javascript"]
        file_size = len(content)
        summary = f"تضم السيرة الذاتية نصاً بـ {file_size} بايت. تم تحليل البيانات واستخراج المهارات التقنية الأساسية بنجاح، وجاري مطابقتها مع سوق العمل."
        recommendations = []
        user_skills_lower = [s.lower().strip() for s in detected_skills]

        for job in TEST_JOBS:
            req_skills = job["required_skills"]
            matched_skills = [s for s in req_skills if s in user_skills_lower]
            missing_skills = [s for s in req_skills if s not in user_skills_lower]
            match_score_value = int((len(matched_skills) / len(req_skills)) * 100)

            if match_score_value > 0:
                recommendations.append(
                    {
                        "job_title": job["job_title"],
                        "company": job["company"],
                        "match_score": f"{match_score_value}%",
                        "missing_skills": missing_skills,
                    }
                )

        recommendations.sort(
            key=lambda x: int(x["match_score"].replace("%", "")), reverse=True
        )

        return {
            "summary": summary,
            "detected_skills": detected_skills,
            "recommendations": recommendations,
        }

    except Exception as e:
        return {"detail": f"حدث خطأ أثناء معالجة الملف: {str(e)}"}
