
# AuditAI - Smart Contract Security Analysis with Slither & AI

AuditAI is a security analysis tool for smart contracts, leveraging **Slither** and AI-powered insights to detect vulnerabilities in Solidity code. Designed for developers and auditors, it provides comprehensive reports, customizable analysis options, and exportable results in multiple formats.

## Features

✅ **Slither Integration** – Static analysis for Solidity smart contracts.  
✅ **AI-Powered Insights** – Enhance vulnerability reports using AI.  
✅ **Customizable Reports** – Export results in JSON, PDF, or SARIF.  
✅ **Efficient & Scalable** – Optimized for performance and parallel execution.  


# AuditAI - Smart Contract Security Analysis with Slither & AI

![AuditAI Dashboard](assets/auditai-dashboard.png)


## Getting Started

### Prerequisites
Ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)
- [Node.js](https://nodejs.org/)
- [Git](https://git-scm.com/)

### Installation

#### Clone the Repository
```sh
git clone https://github.com/YOUR-USERNAME/AuditAI.git
cd AuditAI
```

#### Setup Backend
```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

#### Run Backend (FastAPI)
```sh
uvicorn main:app --reload
```

#### Setup Frontend
```sh
cd frontend
npm install
npm run dev
```

#### Run the Analyzer (Docker)
```sh
docker-compose up
```

## Usage
1. Upload a Solidity contract (`.sol`) in the AuditAI web interface.
2. Select analysis options and execute the audit.
3. View, analyze, and export the security report.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contact
For questions or collaborations, feel free to open an issue or reach out!
