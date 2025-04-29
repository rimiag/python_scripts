# S3 Bucket Cost Optimization Analyzer

A Python script to analyze AWS S3 storage usage, identify cost-saving opportunities, and generate detailed reports for optimization.

## Features

- 🔍 **Comprehensive S3 Scanning**: Recursively scans specified S3 bucket paths
- 🧐 **Duplicate Detection**: Identifies duplicate files based on filename, size, and ETag
- ⏳ **Old File Detection**: Flags files older than a configurable threshold
- 📊 **Detailed Reporting**: Generates CSV reports with actionable insights
- 💰 **Cost Analysis**: Estimates potential savings across all S3 storage classes
- 🚀 **AWS Integration**: Uses boto3 for seamless AWS integration

## Prerequisites

- Python 3.6+
- AWS credentials configured (with S3 read permissions)
- pip package manager

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/s3-cost-optimizer.git
cd s3-cost-optimizer
2. Set Up Virtual Environment (Recommended)
bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
Note: If you don't have a requirements.txt file, install dependencies manually:

bash
pip install boto3
4. Configure the Script
Edit the configuration section at the top of s3_cost_optimizer.py:

python
# ========== CONFIG ========== #
bucket_name = 'your_s3_bucket_name'    # your s3 bucket name
prefix = 'path/to/dir/'         # Directory in your S3 bucket
days_threshold = 1000           # Files older than this many days will be flagged
output_csv = 's3_file_analysis_report.csv'
storage_cost_report = 's3_storage_cost_report.txt'
5. Run the Script
bash
python s3_cost_optimizer.py
6. View the Reports
After successful execution, check the generated reports in the project directory:

s3_file_analysis_report.csv

s3_storage_cost_report.txt

Sample Reports
File Analysis Report (CSV)
Columns include:

File type (Duplicate/Old)

File name and path

Size in MB

Last modified date

Age in days

Action recommendation

Storage Cost Report
Includes:

Total storage scanned

Duplicate storage that can be deleted

Remaining storage size

Monthly cost estimates across all S3 storage classes

Customization Options
Storage Pricing: Update the storage_prices dictionary with current AWS pricing

Threshold: Adjust days_threshold to change what's considered an "old" file

Output Formats: Modify the report generators for different output formats

Security Considerations
Ensure your AWS credentials have only the necessary permissions (S3 read)

The script doesn't modify or delete any files - it's a read-only analysis tool

Review reports before taking any action on your S3 bucket

Contributing
Contributions are welcome! Please open an issue or pull request for any:

Bug fixes

Additional features

Documentation improvements

License
MIT License


### Additional Recommendations:

1. **Create a requirements.txt file** in your repository with:
boto3>=1.28.0


2. **Add a .gitignore file** to exclude virtual environment files and reports:
venv/
*.csv
*.txt
pycache/
*.pyc


3. **Consider adding a setup script** (setup.sh) for Linux/Mac users:
```bash
#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
For Windows users, you could add a setup.ps1:

powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
Would you like me to make any other additions or modifications to the README?

New chat
