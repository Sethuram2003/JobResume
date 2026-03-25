NODE_TYPES = [
    {
        "label": "Person",
        "properties": [
            {"name": "name", "type": "STRING", "description": "Full name of the person"},
            {"name": "email", "type": "STRING"},
            {"name": "phone", "type": "STRING"},
            {"name": "location", "type": "STRING"}
        ]
    },
    {
        "label": "Education",
        "properties": [
            {"name": "degree", "type": "STRING", "description": "e.g., Master of Science in Data Science"},
            {"name": "institution", "type": "STRING"},
            {"name": "duration", "type": "STRING"},
            {"name": "gpa", "type": "STRING"}
        ]
    },
    {
        "label": "Course",
        "properties": [
            {"name": "name", "type": "STRING", "description": "Name of the course"},
            {"name": "description", "type": "STRING", "description": "Topics covered in the course"}
        ]
    },
    {
        "label": "Experience",
        "properties": [
            {"name": "role", "type": "STRING", "description": "Job title or position"},
            {"name": "organization", "type": "STRING", "description": "Company or organization name"},
            {"name": "duration", "type": "STRING"}
        ]
    },
    {
        "label": "Project",
        "properties": [
            {"name": "name", "type": "STRING", "description": "Project title"},
            {"name": "description", "type": "STRING", "description": "Brief summary of what the project does"}
        ]
    },
    {
        "label": "Skill",
        "properties": [
            {"name": "name", "type": "STRING", "description": "Name of the tool, language, framework, or concept (e.g., Python, Neo4j, LangChain)"},
            {"name": "category", "type": "STRING", "description": "e.g., Programming Languages, Databases, Cloud"}
        ]
    },
    {
        "label": "Certification",
        "properties": [
            {"name": "name", "type": "STRING", "description": "Name of the certificate or course"},
            {"name": "issuer", "type": "STRING", "description": "Organization that issued the certificate"}
        ]
    },
    {
        "label": "Publication",
        "properties": [
            {"name": "title", "type": "STRING"},
            {"name": "conference", "type": "STRING"}
        ]
    }
]

RELATIONSHIP_TYPES = [
    {"label": "HAS_EDUCATION", "description": "Person -> Education. Links a person to their degrees."},
    {"label": "COMPLETED_COURSE", "description": "Education -> Course. Links a degree program to specific coursework."},
    {"label": "HAS_EXPERIENCE", "description": "Person -> Experience. Links a person to their jobs."},
    {"label": "WORKED_ON", "description": "Person -> Project OR Experience -> Project. Links a person or a job to a specific project."},
    {"label": "USES_SKILL", "description": "Person -> Skill, Project -> Skill, OR Experience -> Skill. Tracks what technologies were used where."},
    {"label": "HAS_CERTIFICATION", "description": "Person -> Certification."},
    {"label": "PUBLISHED", "description": "Person -> Publication."}
]

PATTERNS = [
    ["Person", "HAS_EDUCATION", "Education"],
    ["Education", "COMPLETED_COURSE", "Course"],
    ["Person", "HAS_EXPERIENCE", "Experience"],
    ["Person", "WORKED_ON", "Project"],
    ["Experience", "WORKED_ON", "Project"],
    ["Person", "USES_SKILL", "Skill"],
    ["Project", "USES_SKILL", "Skill"],
    ["Experience", "USES_SKILL", "Skill"],
    ["Person", "HAS_CERTIFICATION", "Certification"],
    ["Person", "PUBLISHED", "Publication"]
]

RESUME_GRAPH_SCHEMA = {
    "node_types": NODE_TYPES,
    "relationship_types": RELATIONSHIP_TYPES,
    "patterns": PATTERNS
}