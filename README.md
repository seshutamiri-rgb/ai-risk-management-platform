# RiskLens — AI-Powered Project Risk Management Platform

RiskLens is an AI-assisted project risk management platform designed to help
Project Managers identify, assess, prioritize, and understand software project
risks using structured project data, deterministic risk scoring, controlled
AI tools, knowledge retrieval, workflow orchestration, and LLM-generated
management explanations.

## 🎯 Business Problem

Project risks are often distributed across project data, risk registers,
dependencies, and project knowledge.

RiskLens brings these capabilities together to help a Project Manager:

- Retrieve project risks
- Assess risk probability and impact
- Calculate deterministic risk scores
- Classify risk severity
- Retrieve relevant project knowledge
- Generate management-oriented explanations
- Support human decision-making

The AI assists the Project Manager; it does not replace the Project Manager's
final decision.

## ✨ Key Features

- Project risk retrieval and analysis
- Probability × Impact risk scoring
- Configurable risk severity classification
- Project knowledge retrieval
- AI-generated management-oriented explanations
- LangGraph-based workflow orchestration
- MCP-based controlled tool access
- Snowflake integration for structured project/risk data
- Human-in-the-loop decision support
- Input and structured-output validation
- Error handling and secure configuration

## 🏗️ Architecture

                    ┌──────────────────────┐
                    │   React + TypeScript │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Python + FastAPI   │
                    │     Backend API      │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │    LangGraph     │        │    MCP Tools     │
       │   Orchestration  │        │ Controlled Access│
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │  Deterministic   │        │ Project Knowledge│
       │    Risk Engine   │        │ Retrieval / RAG  │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌──────────────────────┐
                    │         LLM          │
                    │ Management Explanation│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Project Manager    │
                    │   Final Decision     │
                    └──────────────────────┘

🔄 AI Workflow
The RiskLens workflow follows a controlled multi-step process:

Project / Risk Data
        ↓
Risk Retrieval
        ↓
Risk Validation
        ↓
Deterministic Risk Calculation
        ↓
Severity Classification
        ↓
Project Knowledge Retrieval
        ↓
LLM Management Explanation
        ↓
Human Project Manager Decision

🧮 Deterministic Risk Engine
RiskLens uses deterministic business logic for risk scoring.
Risk Score = Probability × Impact

Probability and Impact are evaluated on a 1–5 scale.
The resulting score is classified into configurable severity bands.
The LLM does not calculate or override the risk score or severity.
This separation keeps deterministic business decisions independent from
probabilistic LLM output.

🧠 LangGraph Orchestration
LangGraph is used to coordinate the multi-step AI workflow.
The workflow coordinates:
1. Project risk retrieval
2. Risk validation
3. Deterministic risk scoring
4. Project knowledge retrieval
5. LLM-based management explanation
LangGraph provides the workflow structure and state transitions rather than
allowing the LLM to independently control the entire application.

🔌 MCP Tool Layer
RiskLens uses an MCP-based tool layer to provide controlled access to
project-related capabilities.
Example tools include: get_project_risks(project_id) and search_project_knowledge(query, top_k=3)
The tool layer separates tool access from the LLM reasoning/explanation layer
and provides a controlled interface for retrieving project information.

📚 Project Knowledge Retrieval / RAG
RiskLens retrieves relevant project-specific knowledge to provide additional
context to the LLM.
The retrieved information helps the LLM produce explanations grounded in
project context rather than relying only on general model knowledge.

🤖 LLM Responsibilities
The LLM is primarily used for:
- Interpreting project-risk context
- Using retrieved project knowledge
- Generating structured management-oriented explanations
- Summarizing risk information
- Supporting Project Manager decision-making
The LLM is not responsible for deterministic risk calculation.

👤 Human-in-the-Loop
RiskLens follows a human-in-the-loop approach.
AI analyzes
     ↓
AI explains
     ↓
Project Manager reviews
     ↓
Project Manager decides
The final project risk decision remains with the human Project Manager.

📊 Example Risk Analysis
    Example request: Analyze the risks for project PRJ-001 and explain the highest-priority risks.

User Request
     ↓
Project Risk Retrieval
     ↓
Risk Validation
     ↓
Probability × Impact
     ↓
Severity Classification
     ↓
Project Knowledge Retrieval
     ↓
LLM Management Explanation
     ↓
Project Manager Review

Example deterministic calculation:
Probability = 4
Impact = 5

Risk Score = 4 × 5 = 20

Severity = High

The LLM then provides a management-oriented explanation based on the
retrieved project context.
The Project Manager makes the final decision.

 🔗 Example API

Risk analysis endpoint:
GET /graph/projects/{project_id}/risk-analysis
Example: GET /graph/projects/PRJ-001/risk-analysis

The endpoint invokes the AI risk-analysis workflow and returns the
structured risk analysis and management-oriented explanation.

🛡️ Validation & Security
The application includes controls designed to improve reliability and protect
sensitive configuration:
- Input validation
- Structured output validation
- SQL/data validation where applicable
- Controlled MCP tool access
- Error handling
- Environment-based configuration
- Secret protection
- Automated testing
- Safe diagnostics without exposing credentials
Sensitive credentials such as API keys and Snowflake passwords are not stored
in source code.
Use .env.example as the configuration template.

🧰 Technology Stack
Frontend
- React
- TypeScript
Backend
- Python
- FastAPI
Data
- Snowflake
- SQL
AI / Agentic AI
- LLM
- LangGraph
- MCP
- Project Knowledge Retrieval / RAG
- Prompt Engineering
- Structured Output Validation
Development
- GitHub
- GitHub Copilot
- VS Code

📁 Project Structure
ai-risk-management-platform/
│
├── backend/
│   ├── app/
│   ├── services/
│   └── routes/
│
├── langgraph/
│   └── risk_workflow.py
│
├── mcp_servers/
│   └── risk_mcp_server.py
│
├── rag/
│
├── scripts/
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

 🧪 Testing & Validation
    The project includes automated testing covering key application and AI workflow components.
  
  Validation areas include:
- API input validation
- Risk calculation validation
- Structured output validation
- Workflow/error handling
- MCP tool access
- Data retrieval
- AI response handling
- Security and configuration checks

🚀 Current Status
Development Status: Local frontend and backend integration completed and
tested.
The project is currently being prepared for further deployment and
production-oriented improvements.
Cloud deployment is not currently claimed as part of this project.

🔮 Future Enhancements

Planned enhancements include:

- Cloud deployment
- Production-oriented observability
- Expanded project knowledge sources
- Additional AI-assisted project management capabilities
- Enhanced UI dashboards and analytics

🎓 Key Learning Areas
This project demonstrates practical experience with:
- AI Agent architecture
- Agentic AI workflows
- LLM application development
- LangGraph orchestration
- MCP-based tool integration
- RAG / knowledge retrieval
- Deterministic business logic + LLM separation
- Structured output validation
- Human-in-the-loop AI
- Enterprise data integration
- Snowflake
- FastAPI
- React / TypeScript
- AI application security and guardrails
