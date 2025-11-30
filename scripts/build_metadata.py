import pandas as pd
import json
import os

# 确保输出目录存在
os.makedirs("output", exist_ok=True)

def extract_metadata(csv_path, resource_name, department):
    df = pd.read_csv(csv_path)
    fields = []
    for col in df.columns:
        # 类型推断
        if df[col].dtype == 'object':
            field_type = "string"
        elif 'float' in str(df[col].dtype):
            field_type = "float"
        elif 'int' in str(df[col].dtype):
            field_type = "integer"
        else:
            field_type = "string"
        
        # 敏感级别判断
        sens = "sensitive" if "id" in col.lower() or "credit" in col.lower() or "number" in col.lower() else "public"
        
        fields.append({
            "name": col,
            "type": field_type,
            "sensitivity": sens,
            "description": f"来自 {department}"
        })
    
    metadata = {
        "resource_name": resource_name,
        "department": department,
        "fields": fields,
        "source_file": csv_path,
        "data_lineage": f"原始表: {csv_path} | 提供单位: {department}"
    }
    return metadata

# 定义数据资源
resources = [
    ("data/enterprise_registration.csv", "企业注册信息", "市场监管局"),
    ("data/social_insurance.csv", "社保参保信息", "人力资源和社会保障局"),
    ("data/real_estate.csv", "不动产登记信息", "自然资源和规划局")
]

all_metadata = []
for csv, name, dept in resources:
    if os.path.exists(csv):
        meta = extract_metadata(csv, name, dept)
        all_metadata.append(meta)
        print(f"✅ 已处理: {name}")
    else:
        print(f"⚠️ 文件不存在: {csv}")

# 保存为 JSON
with open("output/gov_metadata.json", "w", encoding="utf-8") as f:
    json.dump(all_metadata, f, ensure_ascii=False, indent=2)

print("\n🎉 元数据已生成 → output/gov_metadata.json")