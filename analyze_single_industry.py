# coding=utf-8
"""
单行业研报分析示例脚本

演示如何使用AI分析单个行业的研报数据
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
    get_institutions_from_reports
)


def analyze_single_industry(keyword: str):
    """
    分析单个行业的研报

    Args:
        keyword: 行业关键词
    """
    print(f"=== 开始分析 {keyword} 行业研报 ===")
    
    # 1. 获取研报数据
    reports = fetch_research_reports(keyword, page_count=2, days_limit=60)
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
        print(f"主要机构: {', '.join(institutions[:8])}")
    
    # 4. 初始化分析器
    ai_config = {
        "MODEL": "deepseek/deepseek-chat",  # 推荐使用DeepSeek模型进行中文财经分析
        "API_KEY": "your_api_key",  # 请替换为实际的API密钥
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
    print("这可能需要几分钟时间，请耐心等待...")
    
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
    print("单行业研报分析示例")
    print("=" * 50)
    
    # 分析光伏行业
    analyze_single_industry("光伏")


if __name__ == "__main__":
    main()
