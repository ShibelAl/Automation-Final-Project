# Asana Web Application Testing

Welcome to the Asana Web Application Testing project! This project ensures that the Asana web application performs seamlessly through comprehensive UI, API, and combined API+UI testing. Asana is a leading project management platform that helps teams organize, track, and manage their work efficiently.

## Project Overview

- **UI Testing**: Using Selenium WebDriver to automate interactions with the Asana website.
- **API Testing**: Using the Asana REST API to validate API endpoints and responses.
- **Combined API+UI Testing**: Integrates both UI and API testing to ensure that all components work together flawlessly, delivering a complete and smooth user experience.

## API Documentation

For API requests and details, refer to the [Asana Developers API Reference](https://developers.asana.com/reference/rest-api-reference).

## Asana Website

The Asana web application can be accessed at: [Asana Home](https://app.asana.com/0/home/1207971857090891).

## Setup and Configuration

1. **Dependencies**:
   - Python 3.x
   - Selenium WebDriver
   - Allure
   - Logging
   - Pytest-html
   - Jira


2. **Configuration**:
   - Ensure you have a valid Asana API token.
   - Update the configuration files with necessary API credentials and settings.

3. **Installation**:
   - Clone the repository:
     ```bash
     git clone https://github.com/ShibelAl/Automation-Final-Project.git
     ```
   - Navigate to the project directory:
     ```bash
     cd Automation-Final-Project
     ```
   - Install the required dependencies:
     ```bash
     pip install selenium allure logging pytest-html jira
     ```

## Running Tests

1. **UI Tests**:
   - Navigate to the `test/ui` directory:
     ```bash
     cd test/ui
     ```
   - Run the Selenium test scripts.

2. **API Tests**:
   - Navigate to the `test/api` directory:
     ```bash
     cd test/api
     ```
   - Run the API test scripts.

3. **API+UI Tests**:
   - Navigate to the `test/api and ui` directory:
     ```bash
     cd test/"api and ui"
     ```
   - Run the API+UI test scripts. These tests involve performing actions via the API and then asserting that the results are reflected correctly in the UI.

## Reporting

Test results and reports are generated using various formats:
- **HTML Reports**: Generated using `pytest-html`.
- **XML Reports**: Generated for detailed test execution data.
- **Allure Reports**: For rich and interactive reports.
- **Jira**: Issues and test results are reported to Jira for tracking.
- **Logging**: Detailed logs are maintained for debugging and tracking purposes.

## Test Cases

- **UI Tests**:
  - Test the main features of the Asana web application.
  - Verify UI elements and interactions.

- **API Tests**:
  - Validate API endpoints and response data.
  - Ensure proper error handling and data integrity.

- **API+UI Tests**:
  - Perform actions via the API and assert that these actions and their results are accurately reflected in the UI, ensuring end-to-end functionality and consistency.

## Notes

- Ensure that you have the necessary permissions and access to the Asana API.
- Keep your API tokens secure and do not expose them in the repository.

## Contributing

Feel free to submit pull requests or open issues for any bugs or enhancements.
