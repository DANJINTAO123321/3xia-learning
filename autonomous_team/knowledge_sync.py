#!/usr/bin/env python3
"""
三虾自主协作系统 - 知识同步
"""

import os
import re
from datetime import datetime
from config import KNOWLEDGE_DIR, SHRIMP_ID, SHRIMP_NAME

def ensure_knowledge_dir():
    """确保知识库目录存在"""
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

def extract_key_points(text):
    """从文本中提取关键点"""
    # 简单的关键点提取
    lines = text.split('\n')
    key_points = []
    for line in lines:
        line = line.strip()
        if line.startswith('-') or line.startswith('*') or line.startswith('•'):
            key_points.append(line.lstrip('-*• '))
        elif line.startswith('##') or line.startswith('**'):
            key_points.append(line.lstrip('#* ').rstrip('*#'))
    return key_points

def save_learning(title, content, tags=None):
    """保存学习成果到知识库"""
    ensure_knowledge_dir()
    
    # 生成文件名
    safe_title = re.sub(r'[^\w\s-]', '', title)
    safe_title = re.sub(r'[\s]+', '_', safe_title)[:50]
    filename = f"{datetime.now().strftime('%Y%m%d')}_{safe_title}.md"
    filepath = os.path.join(KNOWLEDGE_DIR, filename)
    
    # 构建markdown
    key_points = extract_key_points(content)
    
    markdown = f"""# {title}

## 概述
{content}

## 关键要点
"""
    for point in key_points:
        markdown += f"- {point}\n"
    
    markdown += f"""
## 标签
"""
    for tag in (tags or []):
        markdown += f"- {tag}\n"
    
    markdown += f"""
## 学习记录
- **学习虾米**: {SHRIMP_NAME} ({SHRIMP_ID})
- **学习时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **来源**: 任务执行

---
*由三虾自主协作系统自动生成*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    return filepath

def get_recent_knowledge(limit=10):
    """获取最近的知识库更新"""
    ensure_knowledge_dir()
    files = []
    
    for f in os.listdir(KNOWLEDGE_DIR):
        if f.endswith('.md'):
            filepath = os.path.join(KNOWLEDGE_DIR, f)
            files.append({
                'name': f,
                'path': filepath,
                'modified': os.path.getmtime(filepath)
            })
    
    # 按修改时间排序
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    result = []
    for f in files[:limit]:
        with open(f['path'], 'r', encoding='utf-8') as fp:
            result.append({
                'name': f['name'],
                'content': fp.read()[:500]  # 只读前500字符
            })
    
    return result

def search_knowledge(keyword):
    """搜索知识库"""
    ensure_knowledge_dir()
    results = []
    
    for f in os.listdir(KNOWLEDGE_DIR):
        if f.endswith('.md'):
            filepath = os.path.join(KNOWLEDGE_DIR, f)
            with open(filepath, 'r', encoding='utf-8') as fp:
                content = fp.read()
                if keyword.lower() in content.lower():
                    results.append({
                        'name': f,
                        'path': filepath,
                        'preview': content[:200]
                    })
    
    return results
