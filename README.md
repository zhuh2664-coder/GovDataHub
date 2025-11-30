# GovDataHub

> A lightweight, extensible data catalog system for government data governance.  
> Enables cross-departmental metadata management and semantic search — built for real-world policy and interoperability needs.

**GovDataHub** 是一个面向政务场景的轻量级数据目录系统，旨在解决政府数据“**找不到、看不懂、不敢用**”的核心痛点。项目从最小可行原型（MVP）起步，逐步构建支持元数据管理、跨域语义检索、数据血缘追踪与质量评估的能力，并与 **DCMM**（数据管理能力成熟度模型）和 **DAMA-DMBOK** 治理框架对齐。

---

## 🛠 本地运行指南

### 环境依赖

| 组件 | 版本要求 | 说明 |
|------|--------|------|
| **Python** | ≥ 3.8 | 推荐使用 3.9–3.11 |
| **Docker** | 最新版 | 用于本地运行 Elasticsearch |
| **Elasticsearch**（服务端） | 8.12.0 | 通过 Docker 启动 |
| **Python 客户端** | `elasticsearch>=7.17.0,<8.0.0` | **必须使用 7.x 客户端**以兼容关闭安全认证的 ES 8 实例（详见下方说明） |

> 💡 **为什么用 elasticsearch<8？**  
> Elasticsearch 8.x 默认启用 HTTPS 和安全认证。虽然我们通过 `-e "xpack.security.enabled=false"` 关闭了安全模块，但 **`elasticsearch>=8` 的 Python 客户端仍会强制验证 SSL 或使用新 API 风格**，导致连接失败或兼容性警告。  
> 使用 `elasticsearch<8`（即 7.17.x）可确保通过纯 HTTP 连接，避免认证问题，且完全兼容 ES 8 的兼容模式。

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/govdatahub.git
   cd govdatahub
2. **安装 Python 依赖**
   ```bash
   pip install -r requirements.txt
3. **启动 Elasticsearch（无安全认证模式）**
   ```bash
   docker run -d --name es -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.security.http.ssl.enabled=false" \
  elasticsearch:8.12.0
4. **运行数据治理流程**
   ```bash
   # 生成结构化元数据
    python scripts/build_metadata.py

    # 将元数据导入 Elasticsearch
    python scripts/index_to_es.py

    # 测试跨部门关键词检索
    python scripts/search.py