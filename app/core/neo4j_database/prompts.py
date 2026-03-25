from neo4j_graphrag.generation import RagTemplate


DEFAULT_TEMPLATE = """
You are a top-tier algorithm designed for extracting a labeled property graph schema in
structured formats.

Generate a generalized graph schema based on the input text. Identify key node types,
their relationship types, and property types.

IMPORTANT RULES:
1. Return only abstract schema information, not concrete instances.
2. Use singular PascalCase labels for node types (e.g., Person, Company, Product).
3. **MANDATORY: Every node type MUST include a property named "name" with the type "STRING".**
4. Use UPPER_SNAKE_CASE labels for relationship types (e.g., WORKS_FOR, MANAGES).
5. Include additional property definitions only when the type can be confidently inferred.
6. When defining patterns, ensure that every node label and relationship label mentioned exists in your lists of node types and relationship types.
7. Do not create node types that aren't clearly mentioned in the text.
8. Keep your schema minimal and focused on clearly identifiable patterns in the text.

Accepted property types are: BOOLEAN, DATE, DURATION, FLOAT, INTEGER, LIST,
LOCAL_DATETIME, LOCAL_TIME, POINT, STRING, ZONED_DATETIME, ZONED_TIME.

Return a valid JSON object that follows this precise structure:
{{
  "node_types": [
    {{
      "label": "NodeLabel",
      "properties": [
        {{
          "name": "name",
          "type": "STRING"
        }},
        ...
      ]
    }},
    ...
  ],
  "relationship_types": [
    {{
      "label": "RELATIONSHIP_TYPE"
    }},
    ...
  ],
  "patterns": [
    ["SourceNode", "RELATIONSHIP_TYPE", "TargetNode"],
    ...
  ]
}}

Examples:
{examples}

Input text:
{text}
"""

RESUME_EXTRACTION_TEMPLATE = """
You are an expert data extraction algorithm specialized in parsing professional profiles, resumes, and portfolios.
Your task is to extract a knowledge graph from the input text, STRICTLY adhering to the provided graph schema.

Here is the allowed Graph Schema:
{schema}

IMPORTANT RULES:
1. STRICT SCHEMA COMPLIANCE: You must ONLY extract node labels and relationship types that are explicitly defined in the provided schema. Do NOT invent new node types (like "Company" or "Technology") or relationships. If it doesn't fit the schema, ignore it.
2. ENTITY RESOLUTION: Ensure that nodes representing the same entity (e.g., the same person, the same skill like 'Python') have exactly the same "name" to avoid duplication in the graph.
3. PROPERTY EXTRACTION: Extract properties for each node as defined in the schema. If a property (like 'duration' or 'gpa') is not mentioned in the text, omit it. Every node MUST have a "name" property.
4. ACCURACY: Only extract facts that are explicitly stated in the input text. Do not hallucinate skills or experiences.
5. DIRECTIONALITY: Ensure relationships strictly follow the patterns defined in the schema (e.g., 'Person' -> 'HAS_EXPERIENCE' -> 'Experience').

Return a valid JSON object containing the extracted nodes and relationships. The structure must follow this exact format:
{{
  "nodes": [
    {{ 
      "id": "unique_string_id_1", 
      "label": "Person", 
      "properties": {{ "name": "Sethuram Gautham", "location": "New York" }} 
    }},
    {{ 
      "id": "unique_string_id_2", 
      "label": "Skill", 
      "properties": {{ "name": "Python", "category": "Programming Languages" }} 
    }}
  ],
  "relationships": [
    {{ 
      "type": "USES_SKILL", 
      "start_node_id": "unique_string_id_1", 
      "end_node_id": "unique_string_id_2", 
      "properties": {{}} 
    }}
  ]
}}

Examples:
{examples}

Input text:
{text}
"""


PROMPT_TEMPLATE = """
You are a top-tier knowledge engineering algorithm. Your task is to transform travel data into a high-fidelity Knowledge Graph JSON.

### SELECTIVE MERGING RULES
1. **GLOBAL NODES (MERGE):** Use standard names for [Country] and [City] (e.g., "Denmark", "Aarhus"). This allows multiple ports to connect to the same geographic branch.
2. **PRIVATE NODES (DO NOT MERGE):** For [Category], [Activity], [Cuisine], [Shopping], [Museum], [HistoricalSite], and [InsiderTip], you MUST prefix both the 'id' and the 'name' with the Port Name.
   - Example: Instead of name "Local Cuisine", use "Aarhus Port Local Cuisine".
   - Example: Instead of id "local_cuisine", use "AarhusPort_LocalCuisine".
   - This ensures that if two ports have "Local Cuisine", they remain separate nodes.

### HIERARCHY & STRUCTURE
- [Country] -> [City] -> [Port] -> [Category] -> [Leaf Node] -> [Tip].
- Each [Port] MUST have its own unique set of [Category] nodes.
- Each [Category] MUST connect to exactly ONE Port.
- Each [Leaf Node] MUST connect to exactly ONE Category.

### OUTPUT FORMAT
Return ONLY a raw JSON object. No markdown, no backticks.
{{
  "nodes": [
    {{
      "id": "PortName_UniqueNodeID",
      "label": "Entity_Type",
      "properties": {{
        "name": "PortName Specific Name",
        "description": "Contextual summary for this specific port (min 10 words)."
      }}
    }}
  ],
  "relationships": [
    {{
      "type": "RELATIONSHIP_TYPE",
      "start_node_id": "unique_id",
      "end_node_id": "unique_id",
      "properties": {{
        "description": "Why these are linked in this specific port context (min 10 words)."
      }}
    }}
  ]
}}

### CONSTRAINTS
- **Schema:** Use only: {schema}
- **Branding:** Every node below the Port level MUST be "branded" with the Port name in its properties to prevent accidental merging.

Input text:
{text}
"""


rag_template = RagTemplate(template='''Answer the Question using the following Context. Only respond with information mentioned in the Context. Do not inject any speculative information not mentioned.

# Question:
{query_text}

# Context:
{context}

# Answer:
''', expected_inputs=['query_text', 'context'])


rag_template_resume = RagTemplate(template='''
You are a professional assistant specialized in analyzing career profiles and technical repositories. 
Your goal is to provide accurate, concise answers based ONLY on the provided Context, which includes both text excerpts and structured graph relationships.

# Context Description:
The context below contains "Text Chunks" (narrative descriptions) and "Graph Relationships" (structured connections between Entities, Skills, Projects, and Experiences).

# Context:
{context}

# Instructions:
1. Use the Graph Relationships to identify specific links between skills and projects (e.g., if a Project USES_SKILL Python).
2. If the question asks for "what," "how," or "where," prioritize information found in the structured relationships.
3. If the information is not present in the Context, state clearly that you do not have enough information. 
4. Do not mention the existence of the "Context" or "Graph" in your final answer; speak naturally.

# Question:
{query_text}

# Answer:
''', expected_inputs=['query_text', 'context'])