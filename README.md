# Terraform AI Plan Review Assistant

An AI-powered Proof of Concept that analyzes Terraform plan JSON and provides a human-readable review of infrastructure changes, risks, destructive operations, and recommended actions.

## Problem

Terraform plan output can contain hundreds or thousands of lines.

Developers and DevOps engineers need to manually identify:

- What resources will change?
- Which resources will be created, updated, deleted, or replaced?
- Are there destructive changes?
- What could cause downtime?
- Does the change require manual approval?

This POC uses AI to simplify that review process.

## Solution

The application accepts a Terraform plan JSON file and produces:

- Overall impact assessment
- Resource change counts
- Important configuration changes
- Destructive changes
- Potential risks
- Security concerns
- Developer attention items
- Final recommendation
- Affected resources

## Architecture

Terraform Plan
       |
       v
terraform show -json
       |
       v
Terraform Plan JSON
       |
       v
Streamlit UI
       |
       v
Python Parser
       |
       v
Resource Changes
       |
       v
Gemini API
       |
       v
AI Terraform Review

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Terraform
- JSON
- python-dotenv

## Project Structure

terraform-ai-review/
|
|-- app.py
|-- ai.py
|-- parser.py
|-- requirements.txt
|-- .env
|-- .gitignore
|
|-- sample_plan.json
|-- test_create.json
|-- test_update.json
|-- test_destructive.json

## How It Works

### 1. Generate Terraform plan JSON

Run:

    terraform plan -out=tfplan

Then:

    terraform show -json tfplan > sample_plan.json

### 2. Start the application

Activate the virtual environment:

    .\venv\Scripts\activate

Run Streamlit:

    streamlit run app.py

Open:

    http://localhost:8501

### 3. Upload the Terraform plan

Upload the generated JSON file through the Streamlit interface.

### 4. Analyze the plan

The application parses the Terraform resources and sends the relevant information to Gemini for AI analysis.

### 5. Review the result

The application displays:

- Risk level
- Resource changes
- Configuration changes
- Destructive operations
- Potential risks
- Security concerns
- Recommended developer actions
- Final recommendation

## Example

For a plan containing:

- 1 Create
- 1 Update
- 1 Delete
- 1 Replace

The application identifies the plan as high risk and recommends manual review before applying the changes.

## Test Scenarios

The POC has been tested with:

### Create-only

Expected result:

    Create: 1
    Update: 0
    Delete: 0
    Replace: 0

### Update-only

Expected result:

    Create: 0
    Update: 1
    Delete: 0
    Replace: 0

### Destructive

Expected result:

    Create: 0
    Update: 0
    Delete: 1
    Replace: 1

The destructive scenario should trigger a high-risk assessment and manual review recommendation.

## Security

API credentials are stored in `.env` and should never be committed to Git.

Example:

    GEMINI_API_KEY=your_api_key_here

Make sure `.env` is included in `.gitignore`.

## Future Improvements

Possible future enhancements:

- GitHub Actions integration
- Automatic Terraform plan generation
- Pull Request comments
- Policy and compliance checks
- Cost impact analysis
- Terraform security scanning
- Historical plan comparison
- Approval workflow
- Integration with Jira or ServiceNow

## Project Status

Proof of Concept completed.

The current version supports Terraform plan upload, parsing, risk assessment, AI-powered review, and an interactive Streamlit interface.