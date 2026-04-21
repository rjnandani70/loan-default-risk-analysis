# Loan Default Risk Analysis

This repository contains multiple Python scripts for analyzing loan default risk. Below is a brief description of each script, including their input/output specifications, key functions, and usage examples.

## Scripts Overview

### 1. `data_preprocessing.py`
**Description:** Cleans and prepares data for analysis.  
**Input:** CSV file with raw loan data.  
**Output:** Cleaned DataFrame saved as a new CSV file.  
**Key Functions:**  
- `load_data(path)`: Loads data from a specified path.  
- `clean_data(df)`: Cleans the DataFrame.  
- `save_data(df, path)`: Saves the cleaned DataFrame to a specified path.  
**Usage Example:**  
```python
import data_preprocessing as dp  
raw_data = dp.load_data('raw_loans.csv')  
cleaned_data = dp.clean_data(raw_data)  
dp.save_data(cleaned_data, 'cleaned_loans.csv')  
```  

### 2. `feature_engineering.py`
**Description:** Creates new features for model training.  
**Input:** Cleaned DataFrame from `data_preprocessing.py`.  
**Output:** DataFrame with additional features.  
**Key Functions:**  
- `add_features(df)`: Adds engineered features to the DataFrame.  
**Usage Example:**  
```python
import feature_engineering as fe  
features_df = fe.add_features(cleaned_data)  
```  

### 3. `model_training.py`
**Description:** Trains machine learning models on processed data.  
**Input:** DataFrame with features and target variable.  
**Output:** Pickled model file.  
**Key Functions:**  
- `train_model(X, y)`: Trains the model and returns it.  
- `save_model(model, path)`: Saves the trained model.  
**Usage Example:**  
```python
import model_training as mt  
model = mt.train_model(features_df.drop('target_variable', axis=1), features_df['target_variable'])  
mt.save_model(model, 'loan_default_model.pkl')  
```  

### 4. `model_evaluation.py`
**Description:** Evaluates the trained model on test data.  
**Input:** Test DataFrame and the trained model.  
**Output:** Evaluation metrics (e.g., accuracy, precision).  
**Key Functions:**  
- `evaluate_model(model, X_test, y_test)`: Returns evaluation metrics.  
**Usage Example:**  
```python
import model_evaluation as me  
evaluation_results = me.evaluate_model(model, X_test, y_test)  
```  

## Conclusion

This documentation provides a concise overview of the scripts available in the repository. For further details, consult the comments within each script and the associated documentation.
