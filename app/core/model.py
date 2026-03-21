from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class PersonalInfo(BaseModel):
    full_name: str
    phone: str
    email: str
    linkedin_url: str
    linkedin_disp_name: str
    github_url: str
    github_disp_name: str

class Education(BaseModel):
    institution: str
    location: str
    degree: str
    gpa: Optional[str] = None
    date_range: str = Field(..., example="August 2018 - May 2022")
    courses: List[str] = []

class SkillItem(BaseModel):
    category: str
    items: List[str]

class Experience(BaseModel):
    title: str
    location: str
    company: str
    date_range: str  
    highlights: List[str]

class Project(BaseModel):
    name: str
    affiliation: Literal["Self-Initiated Project", "Academic Project", "Professional Project"]
    date_range: str  
    description: List[str]

class ResumeData(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    skills: List[SkillItem]  
    experience: List[Experience]
    projects: List[Project]