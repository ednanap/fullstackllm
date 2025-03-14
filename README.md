# AWS Bedrock & SEC EDGAR API Project

## Overview
This project leverages **AWS Bedrock** and **SEC EDGAR API** to fetch **10-Q financial filings** and use **Claude 3 Sonnet** to answer questions based on the provided financial documents. The system consists of:

- **AWS Lambda Functions**:
  - One function fetches **10-Q documents** from the **SEC EDGAR API**.
  - Another function processes user queries and invokes **Claude 3 Sonnet** via AWS Bedrock.
- **Backend Implementation**:
  - Uses **Boto3** to call AWS Bedrock.
  - Fetches SEC filings via a REST API.
  - Passes the 10-Q text as context to **Claude 3** for financial analysis.
- **Planned Front-End Implementation**:
  - A web-based interface for users to **search companies and financial reports**.
  - Allows users to **ask financial questions** and receive AI-powered responses.
  - Uses **React.js (or Next.js)** for a dynamic UI.
  - Backend will be connected via **AWS Lambda & API Gateway**.

---

## How It Works

### Fetching SEC Filings
- The **EDGAR API Lambda function** retrieves **10-Q financial documents** from the SEC database.
- The response contains financial statements, risk disclosures, and company performance details.

### Processing Queries with Claude
- Users input a **question about the financial data**.
- The backend **retrieves the latest 10-Q** for the requested company.
- AWS Bedrock **invokes Claude 3 Sonnet** with the **10-Q content as context**.
- The AI model generates an **insightful response** based on financial data.

---

## Future Front-End Design & Implementation

### Technology Stack
- **React.js** = for a **fast, interactive UI**.
- **AWS API Gateway** to route frontend queries to backend Lambda functions.
- **TailwindCSS** for modern, responsive styling.


### Planned Features
-  **Company Search Bar** – Allows users to search for companies by name or ticker.
-  **Financial Report Display** – Shows SEC filings in a readable format.
-  **AI-Powered Q&A** – Users can ask **natural language questions** about financial data.


---

## Setup & Deployment

### Prerequisites
- AWS CLI installed:
  ```sh
  pip install awscli
  ```
- Boto3 installed:
  ```sh
  pip install boto3
  ```
- Git & GitHub repository

### Deploying the Backend
```sh
# Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Deploy AWS Lambda functions
zip -r lambda1.zip lambda1_fetch_and_upload.py
aws lambda create-function --function-name SECDownloadLambda \
    --runtime python3.8 --role arn:aws:iam::your-account-id:role/lambda-role \
    --handler lambda1_fetch_and_upload.lambda_handler \
    --zip-file fileb://lambda1.zip
```

### Deploying the Frontend (Upcoming)
```sh
npm install
npm run dev
```

---

## Next Steps
- **Complete front-end development** with a modern UI.
- **Deploy API Gateway** to connect the frontend to AWS Lambda.
- **Improve AI responses** by fine-tuning prompt engineering.


