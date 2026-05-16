# 自动代码审查与优化 Agent Demo
# 使用 Claude 或 DeepSeek 模型（示例使用伪接口）
# 适合作为项目 demo 演示

import os
import requests
import json

# -------------------------
# 配置部分
# -------------------------
GITHUB_REPO_URL = 'https://github.com/example/demo-repo'  # 示例仓库
LOCAL_REPO_PATH = './demo-repo'
AI_MODEL_API_URL = 'https://api.example.com/claude'       # 替换为真实 API
API_KEY = 'YOUR_API_KEY'

# -------------------------
# 拉取 GitHub 仓库代码
# -------------------------
def clone_repo(url, path):
    if not os.path.exists(path):
        os.system(f'git clone {url} {path}')
    else:
        os.system(f'cd {path} && git pull')

# -------------------------
# 扫描代码文件
# -------------------------
def get_code_files(path):
    code_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.py', '.js', '.java', '.cpp')):
                code_files.append(os.path.join(root, file))
    return code_files

# -------------------------
# 读取代码内容
# -------------------------
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# -------------------------
# 调用 AI 生成审查结果
# -------------------------
def review_code(file_content):
    prompt = f"""
你是一个高级代码审查与优化 AI。请分析以下代码，输出潜在问题和优化建议（JSON 格式）：
{file_content}
"""
    response = requests.post(
        AI_MODEL_API_URL,
        headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
        data=json.dumps({'prompt': prompt, 'max_tokens': 500})
    )
    return response.json()

# -------------------------
# Demo 主流程
# -------------------------
if __name__ == '__main__':
    clone_repo(GITHUB_REPO_URL, LOCAL_REPO_PATH)
    files = get_code_files(LOCAL_REPO_PATH)
    results = {}

    for f in files:
        code = read_file(f)
        review = review_code(code)
        results[f] = review

    # 输出 demo 结果为 JSON 文件
    with open('code_review_demo.json', 'w', encoding='utf-8') as out:
        json.dump(results, out, indent=2, ensure_ascii=False)

    print(f"已生成代码审查 demo，处理 {len(files)} 个文件，结果保存为 code_review_demo.json")
