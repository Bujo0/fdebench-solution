# FDEBench Solution Runbook

This runbook provides step-by-step instructions for setting up, running, and deploying the FDEBench solution.

## 1. Prerequisites

- **Python 3.12+**: Required for the backend services
- **uv package manager**: For efficient Python dependency management
- **Azure CLI (az)**: Must be logged in with `az login`
- **Docker**: For container builds and local deployment
- **Pulumi CLI**: For infrastructure-as-code deployment to Azure

Verify prerequisites:
```bash
python --version  # Should be 3.12+
uv --version
az account show   # Should show your logged-in account
docker --version
pulumi version
```

## 2. Local Setup

### Clone the Repository
```bash
git clone https://github.com/Bujo0/be-an-fde-for-a-day.git
cd be-an-fde-for-a-day
```

### Install Python Dependencies
```bash
cd py && make setup
```

This will:
- Create a virtual environment
- Install all dependencies from `pyproject.toml`
- Set up the development environment

### Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI credentials:
```
AZURE_OPENAI_ENDPOINT=https://YOUR-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key-here
DOCUMENT_INTELLIGENCE_ENDPOINT=https://YOUR-resource.cognitiveservices.azure.com/
DOCUMENT_INTELLIGENCE_API_KEY=your-key-here
```

## 3. Running Locally

Start the API server in one terminal:
```bash
cd py
make run
# Server will start on http://localhost:8000
```

In a separate terminal, run evaluations:
```bash
cd py

# Score all 3 tasks
make eval

# Score specific tasks
make eval-triage      # Task 1: Email Triage
make eval-extract     # Task 2: Invoice Extraction
make eval-orchestrate # Task 3: Multi-Step Orchestration
```

**Expected output**: JSON scores with reasoning for each evaluation.

### Testing Individual Endpoints

Once the server is running:
```bash
# Health check
curl http://localhost:8000/health

# Test triage (Task 1)
curl -X POST http://localhost:8000/triage \
  -H 'Content-Type: application/json' \
  -d '{
    "email_subject": "Urgent: Account Disabled",
    "email_body": "Your account has been disabled due to suspicious activity...",
    "user_id": "user-123"
  }'

# Test extract (Task 2)
curl -X POST http://localhost:8000/extract \
  -H 'Content-Type: application/json' \
  -d '{
    "document_url": "https://example.com/invoice.pdf",
    "document_type": "invoice"
  }'

# Test orchestrate (Task 3)
curl -X POST http://localhost:8000/orchestrate \
  -H 'Content-Type: application/json' \
  -d '{
    "input": "Process this customer email and extract invoice details",
    "document_url": "https://example.com/customer-invoice.pdf"
  }'
```

## 4. Azure Infrastructure Setup

### Create Resource Group
```bash
az group create \
  --name YOUR-fdebench-rg \
  --location eastus2
```

### Create Azure OpenAI Resource
```bash
# Note: Create in eastus for capacity availability
az cognitiveservices account create \
  --name YOUR-fdebench-aoai \
  --resource-group YOUR-fdebench-rg \
  --kind AIServices \
  --sku S0 \
  --location eastus \
  --yes
```

### Deploy Models to Azure OpenAI
```bash
# Get your AOAI resource name
AOAI_NAME="YOUR-fdebench-aoai"
RG_NAME="YOUR-fdebench-rg"

# Deploy GPT-5.4
az cognitiveservices account deployment create \
  --name $AOAI_NAME \
  --resource-group $RG_NAME \
  --deployment-name gpt-5-4 \
  --model-name gpt-5.4 \
  --model-version 2026-03-05 \
  --model-format OpenAI \
  --sku-name GlobalStandard \
  --sku-capacity 200

# Deploy GPT-4 Turbo (for fallback)
az cognitiveservices account deployment create \
  --name $AOAI_NAME \
  --resource-group $RG_NAME \
  --deployment-name gpt-4-turbo \
  --model-name gpt-4 \
  --model-version 0125-preview \
  --model-format OpenAI \
  --sku-name StandardLLM \
  --sku-capacity 100

# Deploy GPT-4 Vision (for document analysis)
az cognitiveservices account deployment create \
  --name $AOAI_NAME \
  --resource-group $RG_NAME \
  --deployment-name gpt-4-vision \
  --model-name gpt-4 \
  --model-version vision-preview \
  --model-format OpenAI \
  --sku-name Vision \
  --sku-capacity 50
```

### Create Document Intelligence Resource
```bash
az cognitiveservices account create \
  --name YOUR-fdebench-di \
  --resource-group YOUR-fdebench-rg \
  --kind FormRecognizer \
  --sku S0 \
  --location eastus2 \
  --yes
```

### Retrieve Connection Strings
```bash
# Get endpoints and keys for .env configuration
az cognitiveservices account show \
  --name YOUR-fdebench-aoai \
  --resource-group YOUR-fdebench-rg \
  --query properties.endpoint -o tsv

az cognitiveservices account keys list \
  --name YOUR-fdebench-aoai \
  --resource-group YOUR-fdebench-rg \
  --query key1 -o tsv
```

## 5. Docker Build & Run

### Build Docker Image
```bash
# From repo root
docker build -t fdebench-api:latest .

# Or with custom tag
docker build -t fdebench-api:v1.0 .
```

### Run Locally with Docker
```bash
docker run -p 8000:8000 \
  --env-file .env \
  fdebench-api:latest

# With specific environment variables
docker run -p 8000:8000 \
  -e AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/ \
  -e AZURE_OPENAI_API_KEY=your-key \
  fdebench-api:latest
```

### Push to Azure Container Registry
```bash
# Create ACR (if not exists)
az acr create \
  --resource-group YOUR-fdebench-rg \
  --name YOUR-fdebench-acr \
  --sku Basic

# Login to ACR
az acr login --name YOUR-fdebench-acr

# Tag image
docker tag fdebench-api:latest \
  YOUR-fdebench-acr.azurecr.io/fdebench-api:latest

# Push image
docker push YOUR-fdebench-acr.azurecr.io/fdebench-api:latest
```

## 6. Deploy to Azure Container Apps

### Prerequisites
- Pulumi CLI installed and authenticated
- Azure subscription with owner/contributor permissions
- Container Registry with image pushed

### Deployment Steps
```bash
cd infra/app
uv sync

# Initialize Pulumi
pulumi login --local

# Create a random passphrase for the stack
export PULUMI_CONFIG_PASSPHRASE=$(openssl rand -hex 32)

# Create/select stack
pulumi stack select dev --create

# Set configuration values
pulumi config set azure_openai_endpoint "https://YOUR-resource.openai.azure.com/"
pulumi config set --secret azure_openai_api_key "YOUR-KEY"
pulumi config set document_intelligence_endpoint "https://YOUR-resource.cognitiveservices.azure.com/"
pulumi config set --secret document_intelligence_api_key "YOUR-KEY"
pulumi config set container_registry_name "YOUR-fdebench-acr"
pulumi config set container_image_tag "latest"
pulumi config set environment_name "dev"

# Preview deployment
pulumi preview

# Deploy
pulumi up
```

**Output**: The Pulumi stack will output:
- `containerAppUrl`: The public HTTPS endpoint
- `resourceGroup`: The Azure resource group name
- `containerAppName`: The Container App name

Save these values for testing and submission.

## 7. Validate Deployment

### Basic Health Check
```bash
ENDPOINT="https://YOUR-app.azurecontainerapps.io"

# Test health endpoint
curl $ENDPOINT/health
# Expected: {"status": "healthy"}
```

### Test All Endpoints
```bash
# Test Triage (Task 1)
curl -X POST $ENDPOINT/triage \
  -H 'Content-Type: application/json' \
  -d '{
    "email_subject": "Urgent: Account Disabled",
    "email_body": "Your account has been disabled due to suspicious activity...",
    "user_id": "user-123"
  }'

# Test Extract (Task 2)
curl -X POST $ENDPOINT/extract \
  -H 'Content-Type: application/json' \
  -d '{
    "document_url": "https://example.com/invoice.pdf",
    "document_type": "invoice"
  }'

# Test Orchestrate (Task 3)
curl -X POST $ENDPOINT/orchestrate \
  -H 'Content-Type: application/json' \
  -d '{
    "input": "Process this customer email and extract invoice details",
    "document_url": "https://example.com/customer-invoice.pdf"
  }'
```

### Verify Response Headers
```bash
# Check for X-Model-Name header
curl -i $ENDPOINT/health | grep -i "X-Model-Name"
# Expected: X-Model-Name: gpt-5.4
```

### Load Testing
```bash
# Simple concurrent requests test
for i in {1..10}; do
  curl $ENDPOINT/health &
done
wait

# For more comprehensive load testing, use wrk or ab:
# apt-get install wrk
wrk -t4 -c10 -d10s $ENDPOINT/health
```

## 8. Running Experiments

### Setup Experiment Environment
```bash
cd py/apps/sample

# Create experiments directory if needed
mkdir -p experiments/results
```

### Run Baseline Experiment
```bash
python experiments/run_experiment.py \
  --experiment-id baseline \
  --endpoint http://localhost:8000
```

**Expected output**:
- Experiment results saved to `experiments/results/baseline.json`
- Performance metrics printed to console

### Run Parameter Sweep
```bash
python experiments/sweep.py \
  --endpoint http://localhost:8000 \
  --param temperature 0.0,0.3,0.5,0.7,0.9 \
  --param max_tokens 512,1024,2048
```

**Expected output**:
- Results for all parameter combinations
- Summary report of best performing configurations

### Run with Azure Deployment
```bash
python experiments/run_experiment.py \
  --experiment-id production \
  --endpoint https://YOUR-app.azurecontainerapps.io \
  --api-key YOUR-API-KEY
```

## 9. Running Tests

### Unit Tests
```bash
cd py/apps/sample

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_triage.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Integration Tests
```bash
# Start the API server first
# In terminal 1:
cd py && make run

# In terminal 2:
cd py/apps/sample
python -m pytest tests/integration/ -v
```

### Test Fixtures and Mocks
```bash
# Use provided test data
ls tests/fixtures/

# Run specific test with fixture
python -m pytest tests/test_extract.py::test_invoice_extraction -v
```

## 10. Submission Checklist

Before submitting to the FDE Hackathon, verify all requirements:

### API Endpoints
- [ ] **GET /health** returns HTTP 200 with `{"status": "healthy"}`
- [ ] **POST /triage** returns valid JSON with all 8 required fields:
  - `priority` (high/medium/low)
  - `category` (urgent/important/standard/spam)
  - `confidence_score` (0-1)
  - `summary` (string)
  - `action_required` (boolean)
  - `recommended_actions` (array)
  - `reasoning` (string)
  - `reasoning_steps` (array)

- [ ] **POST /extract** returns valid JSON with required fields:
  - `document_id` (string)
  - `extracted_data` (object)
  - `confidence_scores` (object)
  - `processing_time_ms` (number)

- [ ] **POST /orchestrate** returns valid JSON with required fields:
  - `task_id` (string)
  - `status` (running/completed/failed)
  - `steps_executed` (array)
  - `results` (object)

### Response Headers
- [ ] **X-Model-Name** header present on all responses
  - Example: `X-Model-Name: gpt-5.4`
- [ ] **Content-Type** is `application/json`
- [ ] **CORS headers** properly configured for cross-origin requests

### Performance Requirements
- [ ] Handles **10+ concurrent requests** without errors
- [ ] Each request completes in **< 30 seconds**
- [ ] Average response time logged and monitored
- [ ] Load test results documented

### Deployment Requirements
- [ ] Service deployed via **HTTPS** (HTTP redirects to HTTPS)
- [ ] Azure Container Apps URL is **publicly accessible**
- [ ] Endpoint is **stable and responsive** (no timeout errors)
- [ ] Graceful error handling with meaningful error messages

### Repository Requirements
- [ ] **Public GitHub repository** with all source code
- [ ] **docs/architecture.md** describing system design
- [ ] **docs/methodology.md** explaining LLM approach and prompting
- [ ] **docs/evals.md** with evaluation methodology and results
- [ ] **.github/workflows** with CI/CD pipeline (tests, builds, deploys)
- [ ] **README.md** with setup and usage instructions
- [ ] **RUNBOOK.md** (this file) with comprehensive operations guide
- [ ] **Dockerfile** for containerization
- [ ] **pyproject.toml** with all dependencies pinned

### Documentation
- [ ] Architecture diagram in docs/
- [ ] API endpoint documentation with examples
- [ ] Evaluation metrics and scoring methodology
- [ ] Known limitations and future improvements
- [ ] Team and contributors section

### Final Submission
- [ ] All endpoints tested and working
- [ ] Documentation complete and accurate
- [ ] Code is clean, well-commented, and follows standards
- [ ] No sensitive data (keys, credentials) in repository
- [ ] Submit at **aka.ms/fde/hackathon** before deadline

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
make run -- --port 8001
```

#### Azure Credentials Not Found
```bash
# Re-authenticate with Azure
az login

# Verify credentials in .env
echo $AZURE_OPENAI_API_KEY
```

#### Docker Image Build Fails
```bash
# Clean up Docker artifacts
docker system prune -a

# Rebuild with verbose output
docker build -t fdebench-api:latest . --progress=plain
```

#### Pulumi Deployment Errors
```bash
# Check Pulumi logs
pulumi logs -f

# Rollback failed deployment
pulumi up --refresh

# Destroy and redeploy
pulumi destroy
pulumi up
```

#### Tests Failing
```bash
# Install test dependencies
cd py && make setup

# Run tests with verbose output
python -m pytest tests/ -vv -s

# Check for missing fixtures
python -m pytest tests/ --fixtures
```

## Support and Resources

- **FDE Hackathon**: https://aka.ms/fde/hackathon
- **Azure OpenAI Docs**: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **Pulumi Documentation**: https://www.pulumi.com/docs/
- **GitHub Copilot Resources**: https://github.com/features/copilot

---

**Last Updated**: 2024
**Version**: 1.0
