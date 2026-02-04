# coding=utf-8
"""
多行业研报分析示例脚本

演示如何使用AI分析多个行业的研报数据
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trendradar.ai.analyzer import AIAnalyzer
from trendradar.data.research_reports import (
    fetch_multi_industry_reports,
    get_institutions_from_reports,
    get_keywords_from_reports
)


def analyze_multi_industry(industries: list):
    """
    分析多个行业的研报

    Args:
        industries: 行业列表
    """
    print(f"=== 开始分析多个行业研报 ===")
    print(f"分析行业: {', '.join(industries)}")
    
    # 1. 获取多行业研报数据
    multi_data = fetch_multi_industry_reports(industries, page_count=2)
    
    # 2. 统计数据
    total_reports = sum(len(item["titles"]) for item in multi_data)
    print(f"获取到 {total_reports} 份研报")
    
    for item in multi_data:
        industry = item["word"]
        count = len(item["titles"])
        print(f"{industry}: {count} 份研报")
    
    if total_reports == 0:
        print("未获取到研报数据")
        return
    
    # 3. 提取机构和关键词
    institutions = get_institutions_from_reports(multi_data)
    keywords = get_keywords_from_reports(multi_data)
    
    print(f"机构覆盖: {len(institutions)} 家")
    if institutions:
        print(f"主要机构: {', '.join(institutions[:10])}")
    
    # 4. 初始化分析器
    ai_config = {
        "MODEL": "deepseek/deepseek-chat",  # 推荐使用DeepSeek模型进行中文财经分析
        "API_KEY": "your_api_key",  # 请替换为实际的API密钥
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 10000,  # 多行业分析需要更多tokens
        "TIMEOUT": 240  # 延长超时时间
    }
    
    analysis_config = {
        "MAX_NEWS_FOR_ANALYSIS": 80,  # 增加分析上限
        "INCLUDE_RSS": True,
        "LANGUAGE": "Chinese",
        "PROMPT_FILE": "ai_analysis_prompt.txt"
    }
    
    # 检查API密钥配置
    if ai_config["API_KEY"] == "your_api_key":
        print("\n⚠️  请在代码中配置实际的AI模型API密钥")
        print("例如：")
        print("- DeepSeek: 从 https://platform.deepseek.com/ 获取")
        print("- OpenAI: 从 https://platform.openai.com/ 获取")
        print("- 其他支持LiteLLM的模型")
        return
    
    analyzer = AIAnalyzer(
        ai_config=ai_config,
        analysis_config=analysis_config,
        get_time_func=datetime.now,
        debug=True
    )
    
    # 5. 执行分析
    print("\n正在进行AI分析...")
    print("多行业分析需要更长时间，请耐心等待...")
    
    result = analyzer.analyze(
        stats=[],
        rss_stats=multi_data,
        report_mode="incremental",
        report_type="多行业研报分析",
        platforms=institutions,
        keywords=keywords
    )
    
    # 6. 输出结果
    print("\n=== AI分析结果 ===")
    print("=" * 60)
    print("\n1. 核心热点态势")
    print("-" * 40)
    print(result.core_trends)
    
    print("\n2. 舆论风向争议")
    print("-" * 40)
    print(result.sentiment_controversy)
    
    print("\n3. 异动与弱信号")
    print("-" * 40)
    print(result.signals)
    
    print("\n4. 研报深度洞察")
    print("-" * 40)
    print(result.rss_insights)
    
    print("\n5. 研判策略建议")
    print("-" * 40)
    print(result.outlook_strategy)
    
    print("\n" + "=" * 60)
    print("分析完成！")
    
    return result


def main():
    """
    主函数
    """
    print("多行业研报分析示例")
    print("=" * 50)
    
    # 分析多个行业
    analyze_multi_industry(["光伏", "新能源汽车", "人工智能"])


if __name__ == "__main__":
    main()
