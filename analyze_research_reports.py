# coding=utf-8
"""
研报分析示例脚本

演示如何获取研报数据并使用AI进行分析
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trendradar.ai.analyzer import AIAnalyzer
from trendradar.data.research_reports import (
    fetch_research_reports,
    transform_to_rss_stats,
    fetch_multi_industry_reports,
    get_institutions_from_reports,
    get_keywords_from_reports
)


def analyze_single_industry(keyword: str):
    """
    分析单个行业的研报

    Args:
        keyword: 行业关键词
    """
    print(f"=== 开始分析 {keyword} 行业研报 ===")
    
    # 1. 获取研报数据
    reports = fetch_research_reports(keyword, page_count=3)
    print(f"获取到 {len(reports)} 份研报")
    
    if not reports:
        print("未获取到研报数据")
        return
    
    # 2. 转换格式
    rss_stats = transform_to_rss_stats(reports, keyword)
    
    # 3. 提取机构
    institutions = get_institutions_from_reports(rss_stats)
    print(f"机构覆盖: {len(institutions)} 家")
    if institutions:
        print(f"主要机构: {', '.join(institutions[:5])}")
    
    # 4. 初始化分析器
    ai_config = {
        "MODEL": "deepseek/deepseek-chat",
        "API_KEY": "your_api_key",  # 替换为实际API Key
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 8000,  # 增加tokens以支持研报分析
        "TIMEOUT": 180  # 延长超时时间
    }
    
    analysis_config = {
        "MAX_NEWS_FOR_ANALYSIS": 50,
        "INCLUDE_RSS": True,
        "LANGUAGE": "Chinese",
        "PROMPT_FILE": "ai_analysis_prompt.txt"
    }
    
    analyzer = AIAnalyzer(
        ai_config=ai_config,
        analysis_config=analysis_config,
        get_time_func=datetime.now,
        debug=True
    )
    
    # 5. 执行分析
    print("\n正在进行AI分析...")
    result = analyzer.analyze(
        stats=[],
        rss_stats=rss_stats,
        report_mode="incremental",
        report_type=f"{keyword}行业研报分析",
        platforms=institutions,
        keywords=[keyword]
    )
    
    # 6. 输出结果
    print("\n=== AI分析结果 ===")
    print(f"核心热点态势:\n{result.core_trends}\n")
    print(f"舆论风向争议:\n{result.sentiment_controversy}\n")
    print(f"异动与弱信号:\n{result.signals}\n")
    print(f"研报深度洞察:\n{result.rss_insights}\n")
    print(f"研判策略建议:\n{result.outlook_strategy}\n")
    
    return result


def analyze_multi_industry(industries: list):
    """
    分析多个行业的研报

    Args:
        industries: 行业列表
    """
    print(f"=== 开始分析多个行业研报 ===")
    print(f"分析行业: {', '.join(industries)}")
    
    # 1. 获取多行业研报数据
    rss_stats = fetch_multi_industry_reports(industries, page_count=2)
    
    # 2. 统计数据
    total_reports = sum(len(item["titles"]) for item in rss_stats)
    print(f"获取到 {total_reports} 份研报")
    
    for item in rss_stats:
        industry = item["word"]
        count = len(item["titles"])
        print(f"{industry}: {count} 份研报")
    
    if total_reports == 0:
        print("未获取到研报数据")
        return
    
    # 3. 提取机构和关键词
    institutions = get_institutions_from_reports(rss_stats)
    keywords = get_keywords_from_reports(rss_stats)
    
    print(f"机构覆盖: {len(institutions)} 家")
    if institutions:
        print(f"主要机构: {', '.join(institutions[:5])}")
    
    # 4. 初始化分析器
    ai_config = {
        "MODEL": "deepseek/deepseek-chat",
        "API_KEY": "your_api_key",  # 替换为实际API Key
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
    
    analyzer = AIAnalyzer(
        ai_config=ai_config,
        analysis_config=analysis_config,
        get_time_func=datetime.now,
        debug=True
    )
    
    # 5. 执行分析
    print("\n正在进行AI分析...")
    result = analyzer.analyze(
        stats=[],
        rss_stats=rss_stats,
        report_mode="incremental",
        report_type="多行业研报分析",
        platforms=institutions,
        keywords=keywords
    )
    
    # 6. 输出结果
    print("\n=== AI分析结果 ===")
    print(f"核心热点态势:\n{result.core_trends}\n")
    print(f"舆论风向争议:\n{result.sentiment_controversy}\n")
    print(f"异动与弱信号:\n{result.signals}\n")
    print(f"研报深度洞察:\n{result.rss_insights}\n")
    print(f"研判策略建议:\n{result.outlook_strategy}\n")
    
    return result


def main():
    """
    主函数
    """
    print("研报分析系统")
    print("=" * 50)
    
    # 示例1: