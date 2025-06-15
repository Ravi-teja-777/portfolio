from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn
from pathlib import Path
import os

app = FastAPI(
    title="Ravi Teja Portfolio API",
    description="Backend API for Prasanna Sai Ravi Teja Kambham's Portfolio",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")

# Mount static files if they exist
static_path = Path("static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic Models
class ContactInfo(BaseModel):
    phone: str
    email: EmailStr
    github: str
    linkedin: str
    location: str

class Skill(BaseModel):
    category: str
    skills: List[str]

class Achievement(BaseModel):
    title: str
    organization: str
    year: Optional[int] = None

class Education(BaseModel):
    degree: str
    institution: str
    duration: str
    cgpa: float

class Experience(BaseModel):
    position: str
    company: str
    duration: str
    description: str

class Project(BaseModel):
    name: str
    category: str
    description: str
    github_url: str
    technologies: List[str]

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

# Data Storage (In production, use a database)
portfolio_data = {
    "personal_info": {
        "name": "Prasanna Sai Ravi Teja Kambham",
        "title": "Aspiring Developer",
        "bio": "Passionate AI/ML developer with expertise in cloud computing and full-stack development. Currently working as an AI & Machine Learning Intern, focusing on innovative solutions and cutting-edge technologies.",
        "contact": {
            "phone": "+91 6305509208",
            "email": "sairaviteja793@gmail.com",
            "github": "https://github.com/Ravi-teja-777",
            "linkedin": "https://www.linkedin.com/in/raviteja492",
            "location": "Vinukonda, Andhra Pradesh, India"
        },
        "profile_image": "/static/images/profile.jpg"  # Add this field for your profile image
    },
    "skills": [
        {
            "category": "Programming Languages",
            "skills": ["Python", "Java", "HTML", "CSS", "JavaScript"]
        },
        {
            "category": "Frameworks & Tools",
            "skills": ["Flask", "Django", "FastAPI", "AWS", "GitHub"]
        },
        {
            "category": "Data Tools",
            "skills": ["Power BI", "Pandas", "NumPy", "Matplotlib"]
        },
        {
            "category": "Machine Learning",
            "skills": ["Supervised Learning", "Unsupervised Learning", "Feature Engineering", "Predictive Modeling"]
        },
        {
            "category": "AI & ML",
            "skills": ["Model Deployment", "AI Model Optimization", "Prompt Engineering", "Deep Learning"]
        },
        {
            "category": "Cloud Computing",
            "skills": ["AWS EC2", "AWS RDS", "AWS Rekognition", "AWS IAM", "AWS SNS"]
        }
    ],
    "achievements": [
        {"title": "PAWS Certified Cloud Practitioner", "organization": "AWS"},
        {"title": "Java Certification", "organization": "CodeTantra"},
        {"title": "Python Certification", "organization": "NIT Calicut"},
        {"title": "AIEEE Leadership Award", "organization": "Secretary"},
        {"title": "IEI Leadership Award", "organization": "Treasurer"},
        {"title": "Best Event Organizer Award", "organization": "College"}
    ],
    "education": [
        {
            "degree": "Bachelor of Technology",
            "institution": "Seshadri Rao Gudlavalleru Engineering College",
            "duration": "2021 - 2025",
            "cgpa": 8.68
        },
        {
            "degree": "Intermediate (Board of Intermediate Education)",
            "institution": "Sri Chaitanya Junior College",
            "duration": "2018 - 2020",
            "cgpa": 8.9
        },
        {
            "degree": "Secondary Education (Board of Secondary Education)",
            "institution": "Geethanjali High School",
            "duration": "2017 - 2018",
            "cgpa": 9.5
        }
    ],
    "experience": [
        {
            "position": "AI & Machine Learning Intern",
            "company": "The SmartBridge",
            "duration": "Jan 2025 – Present",
            "description": "Currently working as an AI/ML intern, focusing on machine learning model development, optimization, and deployment using Python and AWS."
        }
    ],
    "projects": [
        {
            "name": "UrbanFinds",
            "category": "AWS Projects",
            "description": "Property Management on AWS: Built a property management platform using EC2, DynamoDB, IAM, and SNS for secure access, data handling, and alerts.",
            "github_url": "https://github.com/Ravi-teja-777/UrbanFinds.git",
            "technologies": ["AWS EC2", "DynamoDB", "AWS IAM", "AWS SNS"]
        },
        {
            "name": "RoadBuddy",
            "category": "AWS Projects",
            "description": "Travel Assistance App on AWS: Developed an emergency service app (petrol, repair, food, rentals) using EC2, DynamoDB, IAM, and SNS for real-time updates.",
            "github_url": "https://github.com/Ravi-teja-777/RoadBuddy.git",
            "technologies": ["AWS EC2", "DynamoDB", "AWS IAM", "AWS SNS"]
        },
        {
            "name": "MedTrack",
            "category": "AWS Projects",
            "description": "Patient-Doctor Portal on AWS: Created a healthcare portal with separate logins for doctors and patients using EC2, DynamoDB, IAM, and SNS.",
            "github_url": "https://github.com/Ravi-teja-777/medtrack.git",
            "technologies": ["AWS EC2", "DynamoDB", "AWS IAM", "AWS SNS"]
        },
        {
            "name": "Wellness",
            "category": "AWS Projects",
            "description": "AWS-based wellness platform providing comprehensive health and wellness solutions with cloud infrastructure for scalability and reliability.",
            "github_url": "https://github.com/Ravi-teja-777/Wellness.git",
            "technologies": ["AWS", "Python", "Cloud Computing", "Health Tech"]
        },
        {
            "name": "2D Architecture Design Generation",
            "category": "Generative AI Projects",
            "description": "AI-powered tool for generating architectural designs based on user specifications using advanced generative AI techniques.",
            "github_url": "https://github.com/Ravi-teja-777/2d-architecture-planer.git",
            "technologies": ["Python", "Generative AI", "Deep Learning"]
        },
        {
            "name": "PocketSmart",
            "category": "Generative AI Projects",
            "description": "An AI-powered assistant that offers personalized suggestions for products like interiors, jewelry, and party planning based on your budget, with a built-in history tracking feature.",
            "github_url": "https://github.com/Ravi-teja-777/Wellness.git",
            "technologies": ["Python", "AI", "Machine Learning"]
        },
        {
            "name": "Skin Cancer Detection",
            "category": "Django Project",
            "description": "A Django web app that classifies skin lesions using deep learning for early and accurate diagnosis.",
            "github_url": "https://github.com/Ravi-teja-777/Wellness.git",
            "technologies": ["Django", "Deep Learning", "Python", "CNN"]
        },
        {
            "name": "Email Spam Detection",
            "category": "Machine Learning",
            "description": "ML model for detecting spam emails using natural language processing and classification algorithms.",
            "github_url": "https://github.com/Ravi-teja-777/Email_spam_detection-in-ML.git",
            "technologies": ["Python", "NLP", "Scikit-learn", "Machine Learning"]
        },
        {
            "name": "Wine Quality Detection",
            "category": "Machine Learning",
            "description": "Machine learning model to predict wine quality based on chemical properties and characteristics.",
            "github_url": "https://github.com/Ravi-teja-777/Wine_Quaility_Detection_in_ML.git",
            "technologies": ["Python", "Machine Learning", "Data Analysis"]
        },
        {
            "name": "Power Plant Output Prediction",
            "category": "Machine Learning",
            "description": "Prediction of Full Load Electrical Power Output of a Base Load Operated Combined Cycle Power Plant using machine learning algorithms.",
            "github_url": "https://github.com/Ravi-teja-777/Prediction-of-Full-Load-Electrical-Power-Output-of-a-Base-Load-Operated-Combined-Cycle-Power-Plant.git",
            "technologies": ["Python", "Machine Learning", "Regression", "Data Science"]
        },
        {
            "name": "Insurance Prediction",
            "category": "Machine Learning",
            "description": "Insurance premium prediction system using Logistic Regression to analyze customer data and predict insurance costs based on various demographic and health factors.",
            "github_url": "https://github.com/Ravi-teja-777/Insurance_prdiction_LogisticRegression.git",
            "technologies": ["Python", "Logistic Regression", "Machine Learning", "Data Analysis", "Scikit-learn"]
        },
        {
            "name": "Home Prices Prediction",
            "category": "Machine Learning",
            "description": "Real estate price prediction model using Linear Regression to forecast home prices based on location, size, amenities, and market trends.",
            "github_url": "https://github.com/Ravi-teja-777/home_prices_prediction_using_LinearRegression.git",
            "technologies": ["Python", "Linear Regression", "Machine Learning", "Real Estate", "Data Science"]
        }
    ]
}

# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main portfolio page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """Serve the about page"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    """Serve the projects page"""
    return templates.TemplateResponse("project.html", {"request": request})

@app.get("/skills", response_class=HTMLResponse)
async def skills_page(request: Request):
    """Serve the skills page"""
    return templates.TemplateResponse("skills.html", {"request": request})

@app.get("/experience", response_class=HTMLResponse)
async def experience_page(request: Request):
    """Serve the experience page"""
    return templates.TemplateResponse("experience.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Serve the contact page"""
    return templates.TemplateResponse("contact.html", {"request": request})

# API Routes
@app.get("/api/personal-info")
async def get_personal_info():
    """Get personal information and contact details"""
    return portfolio_data["personal_info"]

@app.get("/api/skills")
async def get_skills():
    """Get all skills categorized by type"""
    return {"skills": portfolio_data["skills"]}

@app.get("/api/projects")
async def get_projects():
    """Get all projects"""
    return {"projects": portfolio_data["projects"]}

@app.get("/api/projects/{category}")
async def get_projects_by_category(category: str):
    """Get projects filtered by category"""
    filtered_projects = [
        project for project in portfolio_data["projects"]
        if project["category"].lower().replace(" ", "").replace("&", "") == category.lower().replace(" ", "").replace("&", "")
    ]
    if not filtered_projects:
        raise HTTPException(status_code=404, detail=f"No projects found for category: {category}")
    return {"projects": filtered_projects, "category": category}

@app.get("/api/experience")
async def get_experience():
    """Get work experience"""
    return {"experience": portfolio_data["experience"]}

@app.get("/api/education")
async def get_education():
    """Get educational background"""
    return {"education": portfolio_data["education"]}

@app.get("/api/achievements")
async def get_achievements():
    """Get achievements and certifications"""
    return {"achievements": portfolio_data["achievements"]}

@app.post("/api/contact")
async def send_contact_message(message: ContactMessage):
    """Handle contact form submissions"""
    # In production, implement email sending or database storage
    contact_data = {
        "timestamp": datetime.now().isoformat(),
        "name": message.name,
        "email": message.email,
        "subject": message.subject,
        "message": message.message,
        "status": "received"
    }
    
    # Here you would typically:
    # 1. Send email notification
    # 2. Store in database
    # 3. Send confirmation email to sender
    
    return {
        "status": "success",
        "message": "Thank you for your message! I'll get back to you soon.",
        "data": contact_data
    }

@app.get("/api/stats")
async def get_portfolio_stats():
    """Get portfolio statistics"""
    return {
        "total_projects": len(portfolio_data["projects"]),
        "project_categories": len(set(project["category"] for project in portfolio_data["projects"])),
        "skills_count": sum(len(skill_cat["skills"]) for skill_cat in portfolio_data["skills"]),
        "achievements_count": len(portfolio_data["achievements"]),
        "years_of_education": 8,
        "current_position": portfolio_data["experience"][0]["position"] if portfolio_data["experience"] else None
    }

@app.get("/api/github-repos")
async def get_github_repos():
    """Get GitHub repository links"""
    repos = []
    for project in portfolio_data["projects"]:
        repos.append({
            "name": project["name"],
            "url": project["github_url"],
            "description": project["description"],
            "technologies": project["technologies"]
        })
    return {"repositories": repos}

@app.get("/api/search")
async def search_portfolio(q: str):
    """Search across portfolio content"""
    results = {
        "projects": [],
        "skills": [],
        "achievements": []
    }
    
    query = q.lower()
    
    # Search projects
    for project in portfolio_data["projects"]:
        if (query in project["name"].lower() or 
            query in project["description"].lower() or 
            any(query in tech.lower() for tech in project["technologies"])):
            results["projects"].append(project)
    
    # Search skills
    for skill_category in portfolio_data["skills"]:
        matching_skills = [skill for skill in skill_category["skills"] if query in skill.lower()]
        if matching_skills or query in skill_category["category"].lower():
            results["skills"].append({
                "category": skill_category["category"],
                "matching_skills": matching_skills if matching_skills else skill_category["skills"]
            })
    
    # Search achievements
    for achievement in portfolio_data["achievements"]:
        if query in achievement["title"].lower() or query in achievement["organization"].lower():
            results["achievements"].append(achievement)
    
    return {
        "query": q,
        "results": results,
        "total_matches": len(results["projects"]) + len(results["skills"]) + len(results["achievements"])
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    if request.url.path.startswith("/api/"):
        return {"error": "API endpoint not found", "status_code": 404}
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)