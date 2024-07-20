

# Sumsub Verification Integration

This project integrates Sumsub's identity verification service with a Flask application, allowing you to create applicants, add documents, and retrieve their status. It uses Google Cloud Firestore for storing verification data.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Creating an Applicant](#creating-an-applicant)
  - [Adding a Document](#adding-a-document)
  - [Getting Status](#getting-status)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- Flask
- Google Cloud SDK
- Sumsub API credentials (https://docs.sumsub.com/reference/about-sumsub-api)
- Access to Google Cloud Firestore

## Installation

1. **Clone the repository:**

   ```bash
   git clone <https://github.com/BABABUSOLA/sumsub>
   cd <sumsub>
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Unix/macOS
   venv\Scripts\activate     # For Windows
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials:**

   Ensure you have your `GOOGLE_APPLICATION_CREDENTIALS` environment variable set to the path of your service account JSON file, the service account should be in the root folder. You can set it up as follows:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"  # For Unix/macOS
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-file.json  # For Windows
   ```

## Configuration

1. **Create a `.env` file** in the root directory of your project to store configuration variables. An example configuration might look like this:

   ```env
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   SUMSUB_API_URL=https://api.sumsub.com
   SUMSUB_API_TOKEN=your-api-token
   ```

2. **Update `config.py`** with your specific configuration details.

## Usage

### Creating an Applicant

Send a POST request to `/create_applicant` with the following JSON body:

```json
{
  "externalUserId": "user123",
  "email": "user@example.com",
  "phone": "+1234567890",
  "lang": "en",
  "type": "individual"
}
```

### Adding a Document

Send a POST request to `/add_document` with form-data including:

- `applicant_id`: The ID of the applicant
- `file`: The document file
- `metadata`: Additional metadata (optional)

### Getting Status

Send a GET request to `/get_status/<applicant_id>` to retrieve the status of the applicant.

## Troubleshooting

### Common Errors

- **PermissionDenied (403)**: Ensure your service account has the correct permissions for Firestore and Sumsub.
- **NotFound (404)**: Verify that you have set up Firestore correctly and the project is correctly configured.

### JSONDecodeError

This error often occurs if the JSON response from an API is empty or malformed. Ensure that your API requests are properly configured and that the response is valid JSON.
