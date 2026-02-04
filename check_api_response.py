# coding=utf-8
"""
检查API响应结构

查看研报API返回的实际数据结构，以便正确映射字段
"""

import sys
import os
import requests
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_api_response():
    """
    检查API响应结构
    """
    print("=== 检查研报API响应结构 ===")
    
    # 测试光伏行业
    keyword = "光伏"
    base_url = "https://api.reportify.cn/reports"
    params = {
        "page_num": 1,
        "page_size": 5,
        "report_types": "7,8,9,10,11,16,19,20,21,22,23,24,25",
        "query": keyword,
        "rt": int(datetime.now().timestamp() * 1000)
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n整体结构: {list(data.keys())}")
            print(f"total_count: {data.get('total_count')}")
            print(f"page_num: {data.get('page_num')}")
            print(f"page_size: {data.get('page_size')}")
            
            # 查看items结构
            items = data.get('items', [])
            print(f"\nitems数量: {len(items)}")
            
            if items:
                print("\n第一份研报的完整结构:")
                first_item = items[0]
                print(f"键名: {list(first_item.keys())}")
                print()
                
                # 打印所有字段
                for key, value in first_item.items():
                    if isinstance(value, str) and len(value) > 50:
                        value = value[:50] + "..."
                    print(f"{key}: {value}")
                    
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_api_response()
