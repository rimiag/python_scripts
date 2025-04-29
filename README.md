# AWS S3 Cost Optimization Analyzer 🚀

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A  Python tool which have created to analyze my company AWS S3 storage usage, identify cost-saving opportunities, and generate actionable reports.

## 📦 Repository Contents
s3-cost-optimizer/
├── s3_cost_optimizer.py # Main analysis script
├── README.md # This documentation
├── requirements.txt # Dependencies file
└── .gitignore # Git ignore rules


## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/s3-cost-optimizer.git
cd s3-cost-optimizer
2. Set Up Virtual Environment (Recommended)

# For Linux/Mac:
python3 -m venv venv
source venv/bin/activate

# For Windows:
python -m venv venv
.\venv\Scripts\activate
3. Install Dependencies

pip install -r requirements.tx


⚙️ Configuration
Edit the configuration section in s3_cost_optimizer.py:

python
# ========== CONFIG ========== #
bucket_name = 'your-production-bucket'  # Target S3 bucket
prefix = 'project-files/'               # Directory to analyze
days_threshold = 365                    # Files older than this will be flagged
output_csv = 's3_optimization_report.csv'
storage_cost_report = 's3_cost_analysis.txt'
🚀 Running the Analysis

python s3_cost_optimizer.py
📊 Understanding the Output
The script generates two reports:

  Detailed File Analysis (CSV)

  Identifies duplicate files

  Flags old files based on your threshold

  Shows potential storage savings

  Storage Cost Report (TXT)

  Breaks down current storage usage

  Shows potential savings from cleanup

  Estimates costs across all S3 storage tiers

🧰 Advanced Usage
Analyze specific date ranges
Modify the threshold in the script:

python
# Example: 180 days threshold
days_threshold = 180
Customize storage pricing
Update the storage_prices dictionary with current AWS rates:

python
storage_prices = {
    'S3 Standard': 0.023,
    'S3 Standard-IA': 0.0125,
    # ... other tiers
}
🔒 Security Note
This script requires only S3 read permissions. Ensure your AWS credentials are configured with minimal required permissions:

json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
🤝 Contributing
Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information.

📧 Contact
Your Name - rizwancl@gmail.com

Project Link: https://github.com/rimiag/s3-cost-optimizer


### Additional Files to Create:

1. **requirements.txt**
```text
boto3>=1.28.0
.gitignore

text
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.pyc

# Virtual Environment
venv/
.env

# Reports
*.csv
*.txt

# IDE
.vscode/
.idea/
LICENSE (MIT License template)

text
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted...
[include full license text]