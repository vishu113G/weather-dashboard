# Grafana Dashboard Automation Testing

## Project Overview

This project automates the testing of data visibility in a Grafana dashboard. It sets up a local Kubernetes environment, deploys necessary components (Grafana and MariaDB), and utilizes Playwright with the pytest framework to automate data loading, dashboard creation, and validation.

## Project Structure

### Local Kubernetes Setup:

* Deploy Grafana and MariaDB on Kubernetes.

### Data Loading:

* Load known data into a MariaDB table using a CSV file.

### Grafana Configuration:

* Connect to Grafana and configure mysql datasource.
* Create a Timeseries Visualization dashboard that queries the loaded data.

### Data Validation:

* Validate the visibility of the data in the dashboard by taking a screenshot and comparing it to a known reference screenshot.

## Prerequisites

### Kubernetes: 
Ensure you have a local Kubernetes cluster set up (e.g., using Minikube or Docker Desktop).

### Python:
Python 3.7 or higher.

### Required Python Packages:

* Playwright
* pytest

## Installation
* Clone the repository
* Install dependencies:
`pip install -r requirements.txt`
* Set up the Kubernetes environment:
  * Deploy Grafana and MariaDB using your preferred method (e.g., Helm charts or YAML manifests).
  * Please use default namespace and default ports for grafana - 3000, mariaDB - 3036
  * Please use port forwarding for grafana and mariaDB (could not get ingress to work at the time of writing this file)
    * kubectl port-forward service/mariadb 3036:3306 --namespace=default
    * kubectl port-forward service/grafana 3000:3000
  * Add a test user with credentials - qatest/test5 (should be provided admin role, otherwise data source edit is not possible)

## Running the Tests

### Start the Kubernetes cluster (if not already running): `minikube start`
### Run the tests: 
activate venv - `.\venv\Scripts\activate`
run the tests `pytest`
### View Test Reports: 
* After the tests complete, check the generated reports using the link shown in the shell or in the reports directory. 
* You can also specify the report path in your pytest configuration.
* You can view screenshots taken during the tests for validation.
