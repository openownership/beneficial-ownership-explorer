import dateparser
from parsel import Selector

def parse_html(html_text):
    selector = Selector(text=html_text)
    return selector.xpath('//body')

def extract_text(elem):
    out = []
    for t in elem.xpath('.//text()').getall():
        out.append(t.strip())
    return " ".join(out).strip()

def process_row(row, item):
    for head, data in zip(row.xpath('./th'), row.xpath('./td')):
        h = extract_text(head)
        d = extract_text(data)
        if "den" in h.lower().split():
            item[h] = dateparser.parse(d).strftime("%Y-%m-%d")
        elif 'IČO' in h:
            item[h] = d.replace(" ","")
        else:
            item[h] = d

def extract_items(html_data):
    data = []
    html = parse_html(html_data)
    results = html.xpath('.//div[@class="search-results"]')
    print(len(results.xpath('./ol/li[contains(@class,"result")]')))
    for result in results.xpath('./ol/li[contains(@class,"result")]'):
        item = {}
        for row in result.xpath('.//table[@class="result-details"]/tbody/tr'):
            process_row(row, item)
        data.append(item)
    return data
