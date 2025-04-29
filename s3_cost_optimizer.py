import boto3
import csv
from datetime import datetime, timezone, timedelta
from collections import defaultdict

# ========== CONFIG ========== #
bucket_name = 'your_s3_bucket_name'    # your s3 bucket name
prefix = 'path/to/dir/'         # Directory in your S3 bucket
days_threshold = 1000
output_csv = 'nirp_file_analysis_report.csv'
storage_cost_report = 'nirp_storage_cost_report.txt'

# Complete AWS S3 Storage Costs per GB per month (USD)
storage_prices = {
    'S3 Standard': 0.023,
    'S3 Intelligent-Tiering': 0.023,
    'S3 Standard-IA': 0.0125,
    'S3 One Zone-IA': 0.01,
    'S3 Glacier Instant Retrieval': 0.004,
    'S3 Glacier Flexible Retrieval': 0.0036,
    'S3 Glacier Deep Archive': 0.00099
}

# ========== AWS CLIENT ========== #
s3 = boto3.client('s3')
threshold_date = datetime.now(timezone.utc) - timedelta(days=days_threshold)

def scan_files(bucket, prefix):
    """Scan S3 bucket and return all files with metadata"""
    all_files = []
    total_size_bytes = 0
    paginator = s3.get_paginator('list_objects_v2')
    
    print(f"🔍 Scanning S3 bucket: {bucket}/{prefix}")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('/'):
                continue
                
            total_size_bytes += obj['Size']
            all_files.append({
                'Path': obj['Key'],
                'FileName': obj['Key'].split('/')[-1],
                'LastModified': obj['LastModified'],
                'Size_MB': round(obj['Size'] / (1024 * 1024), 2),
                'ETag': obj['ETag'].strip('"'),
                'IsOld': obj['LastModified'] < threshold_date
            })
    
    total_size_gb = round(total_size_bytes / (1024 ** 3), 2)
    print(f"✅ Scanned {len(all_files)} files. Total size: {total_size_gb} GB")
    return all_files, total_size_gb

def identify_duplicates(files):
    """Identify and mark duplicate files"""
    duplicate_map = defaultdict(list)
    for f in files:
        key = f"{f['FileName'].lower()}_{f['Size_MB']}_{f['ETag']}"
        duplicate_map[key].append(f)
    
    duplicate_size_gb = 0
    group_id = 1
    
    for group in duplicate_map.values():
        if len(group) > 1:
            group_sorted = sorted(group, key=lambda x: (len(x['Path']), x['LastModified']))
            for idx, f in enumerate(group_sorted):
                f['DuplicateStatus'] = 'Original' if idx == 0 else 'Copy'
                f['DuplicateGroupID'] = f"DUP-{group_id:03d}"
                if idx > 0:
                    duplicate_size_gb += f['Size_MB'] / 1024
    
    duplicate_size_gb = round(duplicate_size_gb, 2)
    return files, duplicate_size_gb

def generate_reports(files, total_size_gb, duplicate_size_gb):
    """Generate CSV and storage cost reports"""
    # Generate CSV Report
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Type', 'FileName', 'Size_MB', 'LastModified', 
            'AgeDays', 'Path', 'DuplicateGroupID', 'Status'
        ])
        writer.writeheader()
        
        # Write duplicates
        dup_files = [f for f in files if 'DuplicateStatus' in f and f['DuplicateStatus'] == 'Copy']
        writer.writerow({'Type': '=== DUPLICATE FILES ==='})
        for f in sorted(dup_files, key=lambda x: x['DuplicateGroupID']):
            writer.writerow({
                'Type': 'Duplicate',
                'FileName': f['FileName'],
                'Size_MB': f['Size_MB'],
                'LastModified': f['LastModified'].strftime('%Y-%m-%d'),
                'AgeDays': (datetime.now(timezone.utc) - f['LastModified']).days,
                'Path': f['Path'],
                'DuplicateGroupID': f['DuplicateGroupID'],
                'Status': 'Can be deleted'
            })
        
        # Write old files
        old_files = [f for f in files if f['IsOld'] and 'DuplicateStatus' not in f]
        writer.writerow({'Type': '=== OLD FILES ==='})
        for f in sorted(old_files, key=lambda x: x['LastModified']):
            writer.writerow({
                'Type': 'Old',
                'FileName': f['FileName'],
                'Size_MB': f['Size_MB'],
                'LastModified': f['LastModified'].strftime('%Y-%m-%d'),
                'AgeDays': (datetime.now(timezone.utc) - f['LastModified']).days,
                'Path': f['Path'],
                'Status': 'Review for archival'
            })

    # Generate Storage Cost Report
    remaining_size_gb = round(total_size_gb - duplicate_size_gb, 2)
    
    report_lines = [
        "🛢️ Storage Summary:",
        f"   🔹 Total Size Scanned         : {total_size_gb} GB",
        f"   🔹 Duplicate Size to Delete   : {duplicate_size_gb} GB",
        f"   ✅ Remaining Size After Clean : {remaining_size_gb} GB",
        "   💰 Monthly Storage Costs:"
    ]
    
    for tier, price in storage_prices.items():
        cost = round(remaining_size_gb * price, 2)
        report_lines.append(f"   🔸 {tier.ljust(30)}: ${cost}")
    
    report_text = "\n".join(report_lines)
    
    with open(storage_cost_report, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print("\n" + report_text)
    print(f"\n📊 Reports generated:")
    print(f"  - Detailed file analysis: {output_csv}")
    print(f"  - Storage cost analysis: {storage_cost_report}")

def main():
    print("🚀 Starting S3 Storage Optimization Analysis\n")
    
    # Step 1: Scan all files
    files, total_size_gb = scan_files(bucket_name, prefix)
    
    # Step 2: Identify duplicates
    files, duplicate_size_gb = identify_duplicates(files)
    
    # Step 3: Generate reports
    generate_reports(files, total_size_gb, duplicate_size_gb)
    
    print("\n✅ Analysis complete")

if __name__ == "__main__":
    main()