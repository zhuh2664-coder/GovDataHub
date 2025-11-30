from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])

def search_gov_data(keyword):
    try:
        resp = es.search(
            index="gov_data_catalog",
            body={
                "query": {
                    "multi_match": {
                        "query": keyword,
                        "fields": ["resource_name^2", "field_names"]
                    }
                },
                "size": 10
            }
        )
        print(f"\n🔍 搜索 '{keyword}'，找到 {resp['hits']['total']['value']} 个结果：\n")
        for hit in resp['hits']['hits']:
            src = hit['_source']
            print(f"▶ 资源: {src['resource_name']} | 部门: {src['department']}")
            print(f"  包含字段: {src['field_names']}\n")
    except Exception as e:
        print(f"❌ 搜索出错: {e}")

if __name__ == "__main__":
    print("=== GovDataHub 检索测试 ===")
    search_gov_data("企业")
    search_gov_data("社保")