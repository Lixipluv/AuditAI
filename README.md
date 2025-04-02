
# AuditAI – Smart Contract Security Analysis with Slither & AI

![AuditAI Dashboard](assets/auditai-dashboard.png)

AuditAI is a comprehensive security analysis tool designed for smart contracts written in Solidity. It leverages the Slither static analyzer and AI-driven insights to identify vulnerabilities, generate intuitive, customizable reports, and export findings in multiple standard formats. Targeted at blockchain developers and security auditors, AuditAI enhances the clarity and accessibility of smart contract audits.

## Key Features

✅ **Slither Integration** – Robust static analysis for Solidity contracts.  
✅ **AI-Powered Insights** – Contextual and comprehensible vulnerability explanations.  
✅ **Customizable Reports** – Easily export findings in JSON, PDF, or SARIF formats.  
✅ **Efficient & Scalable** – Designed for high performance and parallel analyses.

![AuditAI Dashboard](docs/img/dashboard.png)

## Getting Started

### Prerequisites

Ensure you have the following tools installed before setup:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Node.js](https://nodejs.org/) (v16+ recommended)
- [Git](https://git-scm.com/downloads)

### Installation

**Clone the Repository**

```bash
git clone https://github.com/Lixipluv/AuditAI.git
cd AuditAI
```

**Setup Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

**Run Backend (FastAPI)**

```bash
uvicorn main:app --reload
```

**Setup Frontend**

```bash
cd frontend
npm install
npm run dev
```

**Run Analyzer (Docker)**

```bash
docker-compose up
```

## Usage

1. Open the AuditAI web interface at `http://localhost:3000`.
2. Upload your Solidity contract (`.sol`).
3. Select your desired analysis options and initiate the audit.
4. View, interact, and export the generated security report.

## Contributing

We warmly welcome contributions! To contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push your branch (`git push origin feature/new-feature`).
5. Open a Pull Request and clearly describe your changes.

## License

This project is licensed under the Apache License 2.0 – see the [LICENSE](LICENSE) file for details.

## Contact

For questions, issues, or collaborations, please open an issue or reach out directly via GitHub.
