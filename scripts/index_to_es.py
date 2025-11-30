from elasticsearch import Elasticsearch
import json
import os

# 连接 Elasticsearch（关闭安全认证的本地实例）
es = Elasticsearch(["http://localhost:9200"])

# 检查连接
if not es.ping():
    print("❌ 无法连接到 Elasticsearch，请确保它已启动")
    exit(1)

index_name = "gov_data_catalog"

# 删除旧索引（如果存在）
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# 创建新索引
es.indices.create(index=index_name, body={
    "mappings": {
        "properties": {
            "resource_name": {"type": "text"},
            "department": {"type": "keyword"},
            "sensitivity": {"type": "keyword"},
            "field_names": {"type": "text"},
            "data_lineage": {"type": "text"}
        }
    }
})

# 读取元数据
metadata_path = "output/gov_metadata.json"
if not os.path.exists(metadata_path):
    print("❌ 未找到元数据文件，请先运行 build_metadata.py")
    exit(1)

with open(metadata_path, "r", encoding="utf-8") as f:
    metas = json.load(f)

# 导入数据
for meta in metas:
    # 汇总所有字段名用于搜索
    field_names = " ".join([f["name"] for f in meta["fields"]])
    
    doc = {
        "resource_name": meta["resource_name"],
        "department": meta["department"],
        "sensitivity": meta.get("sensitivity", "public"),
        "field_names": field_names,
        "data_lineage": meta["data_lineage"]
    }
    es.index(index=index_name, document=doc)

print("✅ 数据已导入 Elasticsearch 索引: gov_data_catalog")