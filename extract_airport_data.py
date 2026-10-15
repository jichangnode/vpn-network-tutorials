#!/usr/bin/env python3
"""
从 jcpm 网站源代码中提取机场真实数据
"""
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

def extract_airport_data(html_file):
    """从单个机场评测页面提取数据"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # 提取 Schema.org 结构化数据
        schema_script = soup.find('script', type='application/ld+json')
        airport_data = {}

        if schema_script:
            try:
                schema_json = json.loads(schema_script.string)

                # 提取机场名称
                airport_data['name'] = schema_json.get('name', '')

                # 提取描述
                airport_data['description'] = schema_json.get('description', '')

                # 提取价格
                if 'offers' in schema_json:
                    offers = schema_json['offers']
                    airport_data['price_low'] = offers.get('lowPrice', '')
                    airport_data['price_high'] = offers.get('highPrice', '')
                    airport_data['currency'] = offers.get('priceCurrency', 'CNY')

                # 提取评分
                if 'aggregateRating' in schema_json:
                    rating = schema_json['aggregateRating']
                    airport_data['rating'] = rating.get('ratingValue', '')
                    airport_data['rating_count'] = rating.get('ratingCount', '')

                # 提取评测内容
                if 'review' in schema_json:
                    review = schema_json['review']
                    airport_data['review_body'] = review.get('reviewBody', '')

            except json.JSONDecodeError:
                pass

        # 从 meta 标签提取额外信息
        title_tag = soup.find('title')
        if title_tag:
            airport_data['title'] = title_tag.string

        desc_meta = soup.find('meta', attrs={'name': 'description'})
        if desc_meta and not airport_data.get('description'):
            airport_data['description'] = desc_meta.get('content', '')

        keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_meta:
            airport_data['keywords'] = keywords_meta.get('content', '')

        # 提取速度、延迟等数据（从描述中解析）
        desc = airport_data.get('description', '')

        # 提取速度 (MB/s)
        speed_match = re.search(r'(\d+\.?\d*)\s*MB/s', desc)
        if speed_match:
            airport_data['speed_mbps'] = float(speed_match.group(1))

        # 提取延迟 (ms)
        latency_match = re.search(r'(\d+)\s*ms', desc)
        if latency_match:
            airport_data['latency_ms'] = int(latency_match.group(1))

        # 提取节点数量
        nodes_match = re.search(r'(\d+)\s*个?(?:优质)?节点', desc)
        if nodes_match:
            airport_data['node_count'] = int(nodes_match.group(1))

        # 提取稳定率
        stability_match = re.search(r'稳定率?\s*(\d+\.?\d*)%', desc)
        if stability_match:
            airport_data['stability'] = float(stability_match.group(1))

        return airport_data

    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return None

def main():
    jcpm_path = Path('/Users/mac/Documents/open/jcpm')

    # 查找所有机场评测页面
    airport_files = list(jcpm_path.glob('*-jichang-pingce.html'))

    print(f"找到 {len(airport_files)} 个机场评测页面")

    all_airports = []

    for html_file in sorted(airport_files):
        print(f"正在提取: {html_file.name}")
        data = extract_airport_data(html_file)

        if data and data.get('name'):
            data['source_file'] = html_file.name
            all_airports.append(data)
            print(f"  ✓ {data['name']}")
            if 'speed_mbps' in data:
                print(f"    速度: {data['speed_mbps']} MB/s")
            if 'latency_ms' in data:
                print(f"    延迟: {data['latency_ms']} ms")
            if 'price_low' in data:
                print(f"    价格: ¥{data['price_low']}-{data['price_high']}/月")

    # 保存到 JSON 文件
    output_file = Path('data/airports_data.json')
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_airports, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 成功提取 {len(all_airports)} 个机场的数据")
    print(f"✅ 数据已保存到: {output_file}")

    # 生成统计摘要
    total_airports = len(all_airports)
    avg_speed = sum(a.get('speed_mbps', 0) for a in all_airports if 'speed_mbps' in a) / total_airports if total_airports > 0 else 0
    avg_latency = sum(a.get('latency_ms', 0) for a in all_airports if 'latency_ms' in a) / total_airports if total_airports > 0 else 0

    summary = {
        'total_airports': total_airports,
        'average_speed_mbps': round(avg_speed, 2),
        'average_latency_ms': round(avg_latency, 2),
        'extraction_date': '2026-10-15'
    }

    with open('data/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n📊 统计摘要:")
    print(f"  总机场数: {summary['total_airports']}")
    print(f"  平均速度: {summary['average_speed_mbps']} MB/s")
    print(f"  平均延迟: {summary['average_latency_ms']} ms")

    return all_airports

if __name__ == '__main__':
    main()
