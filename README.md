---

# US Visa Approval Prediction - MLOps Production Ready Machine Learning Project

## Overview

This project focuses on building an end-to-end machine learning pipeline for predicting US Visa approvals. The objective is to demonstrate the integration of machine learning with MLOps principles, including model development, training, evaluation, and deployment using tools such as MLflow, Docker, and CI/CD pipelines.

The project uses best practices for model lifecycle management, ensuring it can be efficiently deployed to production.

## Folder Structure

The project structure is as follows:

```bash
├── .github/workflows          # CI/CD pipeline configurations
├── assignments                # Data science and machine learning assignments
├── config                     # Model configuration files and parameters
├── flowcharts                 # Flowcharts for project planning
├── notebook                   # Jupyter notebooks for exploratory data analysis
├── static/css                 # CSS files for web application styling
├── templates                  # HTML templates for the Flask web app
├── us_visa                    # Scripts related to US Visa approval model
├── .dockerignore              # Docker ignore rules
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker container build instructions
├── LICENSE                    # License information
├── README.md                  # Project documentation
├── app.py                     # Flask app to run the ML model as a web service
├── demo.py                    # Demo script to showcase model predictions
├── requirements.txt           # Python package dependencies
├── setup.py                   # Setup script for the local package
├── template.py                # Data validation scripts
├── src                        # Local package for MLOps components
│   ├── __init__.py            # Package initializer
│   ├── constant               # Constants used throughout the project
│   ├── entity                 # Handles configuration loading and management
│   ├── configuration          # Stores and manages intermediate results of the ML pipeline
│   ├── component              # Core components: data preprocessing, model training, etc.
│   ├── pipeline               # Orchestration of the full ML pipeline (ingestion, processing, evaluation)
│   └── utils                  # Helper functions and utilities
└── tests                      # Unit and integration tests
```

### Workflow Explanation

- **constant**: Contains constant values used across the project, such as file paths and model hyperparameters.
- **configuration**: Responsible for fetching data from MongoDB server and handle streamline process.
- **config_entity**: Responsible for loading and managing configuration settings, ensuring the pipeline uses consistent configurations.
- **artifact_entity**: Stores the artifacts created during the pipeline execution, such as processed data, trained models, and evaluation results.
- **component**: Core components for the data pipeline, including data ingestion, preprocessing, feature engineering, model training, and evaluation.
- **pipeline**: The main workflow that ties together all the components and ensures the end-to-end process runs smoothly.
- **app.py**: Flask app that serves the model as a web API for making predictions.
- **demo.py**: Script to showcase model predictions on test data.

## Technologies and Tools

- **Python**: Core programming language for the machine learning model.
- **Flask**: Web framework to serve the ML model via an API.
- **MLflow**: For tracking experiments and managing the model lifecycle.
- **Docker**: Containerization of the project for portability.
- **CI/CD**: Automation pipelines for testing and deploying the project.
- **HTML/CSS**: Frontend for the web-based interface.

## Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/Lavishgangwani/MLOPS-Production-Ready-Machine-Learning-Project.git
cd MLOPS-Production-Ready-Machine-Learning-Project
```

2. **Set up a virtual environment and install dependencies:**

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. **Run the application:**

```bash
python app.py
```

4. **Build and run the Docker container:**

```bash
docker build -t us-visa-prediction .
docker run -p 5000:5000 us-visa-prediction
```

5. **Run the demo script to see a sample prediction:**

```bash
python demo.py
```

## Local Package Setup (`src` folder)

The `src` folder contains the MLOps pipeline, organized into multiple submodules:

- **constant**: Stores constants such as model paths, dataset paths, and feature engineering parameters.
- **config_entity**: Loads and validates configurations (e.g., hyperparameters) needed for model training.
- **artifact_entity**: Stores intermediate and final artifacts, such as processed data, trained models, and evaluation metrics.
- **component**: The main components for data preprocessing, feature engineering, model training, and evaluation.
- **pipeline**: Manages the execution of the pipeline from ingestion to model deployment.
- **utils**: Utility functions used throughout the project (e.g., data handling, logging).

To install the local package:

```bash
pip install -e .
```

After installing, you can import any component in your scripts like this:

```python
from src.component import ModelTrainer
from src.pipeline import Pipeline
```

## CI/CD Pipeline

The CI/CD pipeline automates the testing, building, and deployment of the machine learning model. The pipeline is triggered with each push to the repository and ensures that the model is consistently tested and deployed with Docker.

The `.github/workflows` directory contains YAML files that define the pipeline steps for:

- **Testing**: Running unit and integration tests.
- **Building**: Creating a Docker image.
- **Deploying**: Deploying the Docker container to a cloud provider or local machine.

## Usage

1. **Training the Model**: Use the scripts in the `us_visa` folder to train a machine learning model for predicting US Visa approvals.
2. **Web Interface**: Once the model is trained, run `app.py` to deploy the model via Flask and serve a web interface for making predictions.
3. **Prediction API**: Use the API provided by `app.py` to make predictions by sending HTTP POST requests with the appropriate input data.

## Contributing

Contributions are welcome! Please feel free to fork this repository and submit a Pull Request with your changes.

For any questions or feedback, you can contact me at **lavishgangwani22@gmail.com**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
