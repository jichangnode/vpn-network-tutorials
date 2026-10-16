#!/usr/bin/env python3
"""
从 yongjichang.com 网站源代码中提取机场真实数据
"""
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

def extract_airport_data_yongjichang(html_file):
    """从单个机场评测页面提取数据"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        airport_data = {}

        # 提取 Schema.org 结构化数据
        schema_scripts = soup.find_all('script', type='application/ld+json')

        for script in schema_scripts:
            try:
                schema_json = json.loads(script.string)

                # 提取评测信息
                if schema_json.get('@type') == 'Review':
                    airport_data['name'] = schema_json.get('name', '').replace('深度评测 2026', '').replace('评测2026', '').strip()

                    # 提取评分
                    if 'reviewRating' in schema_json:
                        rating = schema_json['reviewRating']
                        airport_data['rating'] = rating.get('ratingValue', '')

                    # 提取评测对象
                    if 'itemReviewed' in schema_json:
                        item = schema_json['itemReviewed']
                        if not airport_data.get('name'):
                            airport_data['name'] = item.get('name', '')

                    airport_data['date_published'] = schema_json.get('datePublished', '')
                    airport_data['date_modified'] = schema_json.get('dateModified', '')

            except (json.JSONDecodeError, AttributeError):
                pass

        # 从 title 提取机场名称
        title_tag = soup.find('title')
        if title_tag and not airport_data.get('name'):
            title = title_tag.string
            # 提取机场名称 (通常在标题开头)
            match = re.match(r'^([^评测]+?)(?:机场)?(?:评测|深度评测)', title)
            if match:
                airport_data['name'] = match.group(1).strip()

        # 从 meta description 提取信息
        desc_meta = soup.find('meta', attrs={'name': 'description'})
        if desc_meta:
            desc = desc_meta.get('content', '')
            airport_data['description'] = desc

            # 提取价格
            price_match = re.search(r'[¥￥](\d+)/月', desc)
            if price_match:
                airport_data['price_start'] = price_match.group(1)

            # 提取套餐价格范围
            price_range = re.search(r'[¥￥](\d+)[/-][¥￥]?(\d+)/月', desc)
            if price_range:
                airport_data['price_start'] = price_range.group(1)
                airport_data['price_end'] = price_range.group(2)

        # 从 keywords 提取
        keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_meta:
            airport_data['keywords'] = keywords_meta.get('content', '')

        # 从 canonical URL 提取评测链接
        canonical = soup.find('link', rel='canonical')
        if canonical:
            airport_data['review_url'] = canonical.get('href', '')

        # 提取文件名作为标识
        airport_data['source_file'] = html_file.name

        return airport_data

    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return None

def main():
    airport_blog_path = Path('/Users/mac/airport-blog/reviews')

    # 查找所有机场评测页面
    review_files = list(airport_blog_path.glob('review-*.html'))

    print(f"找到 {len(review_files)} 个机场评测页面")

    all_airports = []

    for html_file in sorted(review_files):
        print(f"正在提取: {html_file.name}")
        data = extract_airport_data_yongjichang(html_file)

        if data and data.get('name'):
            all_airports.append(data)
            print(f"  ✓ {data['name']}")
            if 'rating' in data:
                print(f"    评分: {data['rating']}/10")
            if 'price_start' in data:
                if 'price_end' in data:
                    print(f"    价格: ¥{data['price_start']}-{data['price_end']}/月")
                else:
                    print(f"    价格: ¥{data['price_start']}/月起")

    # 保存到 JSON 文件
    output_file = Path('data/yongjichang_airports_data.json')
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_airports, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 成功提取 {len(all_airports)} 个机场的数据")
    print(f"✅ 数据已保存到: {output_file}")

    # 生成统计摘要
    total_airports = len(all_airports)
    avg_rating = sum(float(a.get('rating', 0)) for a in all_airports if 'rating' in a) / total_airports if total_airports > 0 else 0

    summary = {
        'total_airports': total_airports,
        'average_rating': round(avg_rating, 2),
        'extraction_date': '2026-10-16',
        'source': 'yongjichang.com'
    }

    with open('data/yongjichang_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n📊 统计摘要:")
    print(f"  总机场数: {summary['total_airports']}")
    print(f"  平均评分: {summary['average_rating']}/10")
    print(f"  数据来源: {summary['source']}")

    return all_airports

if __name__ == '__main__':
    main()
