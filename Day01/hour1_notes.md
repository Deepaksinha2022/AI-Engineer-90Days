Day 1 — Hour 1: ML Workflow Notes
1. Define the Problem

Understand what you want to predict.
Example: Customer churn prediction (Yes/No).

2. Collect Data

Data sources:

CSV files

Databases

APIs

Logs

CRM systems

3. Data Cleaning

🔹 Handle missing values
🔹 Remove duplicates
🔹 Fix incorrect data types
🔹 Remove outliers

80% of ML work = cleaning.

4. Exploratory Data Analysis (EDA)

Understand:

Distributions

Correlations

Patterns

Outliers

Class imbalance

5. Feature Engineering

Transform raw data:

Encode categorical variables

Scale numeric features

Create new features

Extract date/time components

6. Train/Test Split

Purpose:

Evaluate model on unseen data

Prevent overfitting

Simulate real-world performance

Typical split:

Train 80%

Test 20%

7. Model Selection

Try multiple algorithms:

Logistic Regression

Decision Trees

Random Forest

XGBoost

SVM

Neural Networks

8. Model Training

Fit the selected models on the training dataset.

9. Evaluation

Classification metrics:

Accuracy

Precision

Recall

F1 Score

ROC-AUC

Regression metrics:

RMSE

MAE

R-squared

10. Hyperparameter Tuning

Use:

GridSearchCV

RandomSearchCV

Bayesian Optimization

Goal → Improve model performance.

11. Deployment

Use:

FastAPI

Docker

Cloud (AWS/GCP/Azure)

Monitor model performance in production.