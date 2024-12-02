# Apache Hive Bug Prediction Models

This project aims to enhance software quality by predicting bugs before new code versions are released. By identifying files likely to contain bugs, it prioritizes testing efforts, especially in the critical final stages before a release. Leveraging machine learning models, this approach optimizes resource allocation and improves the reliability of Apache Hive software.

---

## Key Features

- **Bug Prediction**: Predict buggy files using machine learning models.
- **Data Integration**: Combine Jira bug reports with code metrics for a comprehensive analysis.
- **Optimized Testing**: Focus testing efforts on high-risk files to save time and resources.
- **Model Evaluation**: Train and compare Logistic Regression and Random Forest models to ensure robust predictions.

---

## Requirements

- **Programming Tools**: 
  - Git: Clone the Hive repository.
  - Python 3.8+: Programming environment.
- **Libraries**: 
  - Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn.
- **Code Metrics Tool**:
  - SciTools Understand: For gathering detailed metrics on code files.
  
---

## Data Sources

- **Bug Reports**: [Jira Bug Collection](https://issues.apache.org/jira/projects/HIVE/issues/HIVE-13282?filter=allopenissues)
- **Codebase**: [Apache Hive Software](https://github.com/apache/hive)

---

## Setup Instructions

1. **Clone the Repositories**:  
   - Clone this repository (*project repo*).  
   - Clone the Apache Hive repository (*hive repo*).

2. **Install Dependencies**:  
   - Ensure all required libraries are installed.

3. **Execute Notebooks**:  
   - The workflow is split across three Jupyter notebooks. Execute them sequentially:
---

### Workflow

#### 1. **Data Extraction** (*Data_Extraction.ipynb*)

This notebook handles bug report extraction and preprocessing:  
- Fetch bug reports from Jira.  
- Remove redundancies and streamline the dataset.  
- Identify Java and C++ files affected by bugs.

#### 2. **UND Data Collection** (*Data_UND_Collection.ipynb*)

Leverage *SciTools Understand* to collect independent variables for each file across different versions of Hive. This step provides insights into code structure and complexity, critical for modeling bug-prone files.

#### 3. **Data Cleanup** (*Data_Cleanup.ipynb*)

Refine and structure the dataset:  
- Identify buggy files to focus analysis on problem areas.  
- Enrich the dataset by adding classes and methods, enhancing structural context.

#### 4. **Data Partitioning and Training** (*Data_Partition_Training.ipynb*)

Prepare the data for machine learning and model training:  
- Perform feature selection and data organization.  
- Partition data and conduct correlation analysis.  
- Apply sampling techniques (over-sampling and under-sampling) to address data imbalances.  
- Train and compare Logistic Regression and Random Forest models.  
- Analyze model interpretability using nomograms and top feature analysis.  
- Compare metrics and model behavior across minor and major project versions.

---

## Licensing

This project is licensed under the MIT License. Refer to the [LICENSE](LICENSE) file for more details.

---
