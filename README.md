# DataScience Project

This repository contains data, Python analysis, and work done with other data science tools like RapidMiner, Tableau, RStudio, and PowerBI. It's organized into several folders to keep the different aspects of the project separate and manageable.

## Getting Started

### Prerequisites

*   **Python:** It is **highly recommended** to use Anaconda to manage your Python environment. You can download it from [anaconda.com](https://www.anaconda.com/).

*   **Anaconda Environment:**  A shared Anaconda environment is provided in the `Setup` folder as `environment.yml`.  You can recreate the environment using:

    ```bash
    conda env create -f Setup/environment.yml
    conda activate DataScienceStudy  # Or whatever name is in your environment.yml
    ```

*   **Jupyter Notebook:** Install Jupyter Notebook (if not already included in your environment):

    ```bash
    conda install jupyter
    ```

*   **Other Software:**  The `Setup` folder contains documentation on how to install and configure other software used in this project (Git, VS Code, Anaconda, etc.).

### Instructions

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/thaopham98/DataScience.git](https://github.com/thaopham98/DataScience.git)
    cd DataScience
    ```

2.  **Create and activate a virtual environment (Anaconda - recommended):** (See above)

3.  **Explore the project folders:**  The repository is organized as follows:

## Project Folders

*   **[data](data):** This folder contains the datasets used in the analysis. The datasets are typically in CSV, TSV, or other common data formats. *Describe the type of data stored here (e.g., "Customer data," "Sales data," etc.)*

*   **[python_analysis](python_analysis):** This folder contains Jupyter Notebooks with examples of data science and machine learning using the datasets provided in the `data` folder. Each notebook focuses on a specific analysis or project.  Notebooks in this folder should be considered finished and reviewed.
    *   Load and preprocess the data.
    *   Perform exploratory data analysis (EDA).
    *   Apply machine learning models (if applicable).
    *   Visualize the results.
    *   Interpretations for visual and statistical results.

*   **[draft](draft):** This folder contains Jupyter Notebooks that are still in progress.  These notebooks may be incomplete or contain experimental code.

*   **[RapidMiner](RapidMiner):** This folder contains documentation (PDF files) outlining the steps taken to create models in RapidMiner.

*   **[Tableau](Tableau):** This folder contains Tableau workbooks (`.twbx` or `.twb`) and supporting documentation (e.g., `.docx` files with images of visualizations).

*   **[RStudio](RStudio):** This folder contains R scripts (`.R` files) and any related data or output from data analysis performed in R.
    *    [My First R Markdown](https://thaopham98.github.io/DataScience/RStudio/My-First-R-Markdown-in-R-Studio.html)

*   **[PowerBI](PowerBI):** This folder contains Power BI files (`.pbix`) and any related documentation.

## Usage Examples (Within `python_analysis`)

*Provide a brief example for each notebook in the `python_analysis` folder. For example:*

*   `analysis_notebook_1.ipynb`: This notebook performs customer segmentation using k-means clustering.

## Data (Within `data`)

The `data` folder contains the datasets used for analysis. *Provide more details about the data, such as its source, format, and any preprocessing steps performed.*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Authors

*   Thao Pham (thaopham98)
