# coding=utf-8
"""
研报数据获取与处理模块

从研报API获取数据并转换为系统支持的格式
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional


def fetch_research_reports(
    keyword: str,
    page_count: int = 3,
    page_size: int = 20,
    days_limit: int = 90
) -> List[Dict]:
    """
    从研报API获取数据

    Args:
        keyword: 查询关键词
        page_count: 获取的页数
        page_size: 每页数量
        days_limit: 限制天数，只保留指定天数内的研报

    Returns:
        List[Dict]: 研报数据列表
    """
    reports = []
    base_url = "https://api.reportify.cn/reports"
    cutoff_date = datetime.now() - timedelta(days=days_limit)

    for page in range(1, page_count + 1):
        params = {
            "page_num": page,
            "page_size": page_size,
            "report_types": "7,8,9,10,11,16,19,20,21,22,23,24,25",
            "query": keyword,
            "rt": int(datetime.now().timestamp() * 1000)
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            print(f"[研报API] 请求URL: {response.url}")
            print(f"[研报API] 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[研报API] 响应数据结构: {list(data.keys())}")
                
                # 尝试不同的报告字段名
                report_fields = ["reports", "data", "items", "result"]
                page_reports = []
                
                for field in report_fields:
                    if field in data:
                        page_reports = data[field]
                        print(f"[研报API] 找到报告字段: {field}, 数量: {len(page_reports)}")
                        break
                
                if not page_reports:
                    print(f"[研报API] 未找到报告数据，响应: {data}")
                else:
                    # 过滤时间
                    for report in page_reports:
                        # 处理发布时间
                        publish_at = report.get("publish_at")
                        include_report = False
                        
                        if publish_at:
                            try:
                                # 转换时间戳
                                if isinstance(publish_at, (int, float)):
                                    # 处理毫秒时间戳
                                    if publish_at > 10**12:
                                        publish_at = publish_at / 1000
                                    report_date = datetime.fromtimestamp(publish_at)
                                    if report_date >= cutoff_date:
                                        include_report = True
                                else:
                                    # 处理字符串日期
                                    try:
                                        report_date = datetime.strptime(str(publish_at), "%Y-%m-%d")
                                        if report_date >= cutoff_date:
                                            include_report = True
                                    except Exception:
                                        include_report = True
                            except Exception:
                                include_report = True
                        else:
                            include_report = True
                        
                        if include_report:
                            reports.append(report)
            else:
                print(f"[研报API] 请求失败: {response.status_code}")
                print(f"[研报API] 响应内容: {response.text[:200]}...")
        except Exception as e:
            print(f"[研报API] 获取数据失败: {e}")

    return reports


def transform_to_rss_stats(
    reports: List[Dict],
    keyword: str
) -> List[Dict]:
    """
    将研报数据转换为系统支持的rss_stats格式

    Args:
        reports: 研报数据列表
        keyword: 关键词

    Returns:
        List[Dict]: 转换后的rss_stats格式数据
    """
    transformed_data = {
        "word": keyword,
        "titles": []
    }

    for report in reports:
        # 提取字段
        title = report.get("title", report.get("report_title", ""))
        source_name = report.get("institution_name", report.get("channel_name", ""))
        
        # 处理发布时间
        publish_at = report.get("publish_at")
        time_display = ""
        if publish_at:
            try:
                # 转换时间戳
                if isinstance(publish_at, (int, float)):
                    # 处理毫秒时间戳
                    if publish_at > 10**12:
                        publish_at = publish_at / 1000
                    time_display = datetime.fromtimestamp(publish_at).strftime("%Y-%m-%d")
                else:
                    time_display = publish_at
            except Exception:
                pass
        
        # 处理摘要
        summary = report.get("summary", "")[:300]
        
        # 处理评级
        rating = report.get("rating", report.get("grade", ""))
        report_star = report.get("report_star")
        if not rating and report_star:
            # 将数字评级转换为文字
            star_map = {
                5: "强烈推荐",
                4: "推荐",
                3: "买入",
                2: "持有",
                1: "卖出"
            }
            rating = star_map.get(report_star, "")
        
        # 处理目标价
        target_price = report.get("target_price", report.get("price", ""))

        # 构建研报条目
        report_item = {
            "title": title,
            "source_name": source_name,
            "time_display": time_display,
            "summary": summary,
            "rating": rating,
            "target_price": target_price
        }

        transformed_data["titles"].append(report_item)

    return [transformed_data]


def fetch_multi_industry_reports(
    industries: List[str],
    page_count: int = 2
) -> List[Dict]:
    """
    获取多个行业的研报数据

    Args:
        industries: 行业列表
        page_count: 每页数量

    Returns:
        List[Dict]: 多行业研报数据
    """
    all_data = []

    for industry in industries:
        reports = fetch_research_reports(industry, page_count=page_count)
        if reports:
            industry_data = {
                "word": industry,
                "titles": []
            }
            for report in reports:
                # 提取字段
                title = report.get("title", report.get("report_title", ""))
                source_name = report.get("institution_name", report.get("channel_name", ""))
                
                # 处理发布时间
                publish_at = report.get("publish_at")
                time_display = ""
                if publish_at:
                    try:
                        # 转换时间戳
                        if isinstance(publish_at, (int, float)):
                            # 处理毫秒时间戳
                            if publish_at > 10**12:
                                publish_at = publish_at / 1000
                            time_display = datetime.fromtimestamp(publish_at).strftime("%Y-%m-%d")
                        else:
                            time_display = publish_at
                    except Exception:
                        pass
                
                # 处理摘要
                summary = report.get("summary", "")[:300]
                
                # 处理评级
                rating = report.get("rating", report.get("grade", ""))
                report_star = report.get("report_star")
                if not rating and report_star:
                    # 将数字评级转换为文字
                    star_map = {
                        5: "强烈推荐",
                        4: "推荐",
                        3: "买入",
                        2: "持有",
                        1: "卖出"
                    }
                    rating = star_map.get(report_star, "")
                
                # 处理目标价
                target_price = report.get("target_price", report.get("price", ""))

                # 构建研报条目
                report_item = {
                    "title": title,
                    "source_name": source_name,
                    "time_display": time_display,
                    "summary": summary,
                    "rating": rating,
                    "target_price": target_price
                }
                industry_data["titles"].append(report_item)
            all_data.append(industry_data)

    return all_data


def get_institutions_from_reports(reports: List[Dict]) -> List[str]:
    """
    从研报数据中提取机构列表

    Args:
        reports: 研报数据

    Returns:
        List[str]: 机构列表
    """
    institutions = set()
    
    for report_group in reports:
        titles = report_group.get("titles", [])
        for report in titles:
            institution = report.get("source_name", "")
            if institution:
                institutions.add(institution)
    
    return list(institutions)


def get_keywords_from_reports(reports: List[Dict]) -> List[str]:
    """
    从研报数据中提取关键词列表

    Args:
        reports: 研报数据

    Returns:
        List[str]: 关键词列表
    """
    keywords = []
    
    for report_group in reports:
        keyword = report_group.get("word", "")
        if keyword:
            keywords.append(keyword)
    
    return keywords
