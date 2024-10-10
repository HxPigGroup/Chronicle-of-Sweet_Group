from jinja2 import Template
import re
from collections import defaultdict

text = ""
with open("word_record.txt") as f:
    for i in f.readlines():
        text += i

result_dict = defaultdict(list)
image_dict = defaultdict(list)
pattern = r"\*\*(.*?)\*\*：(.*?)(?=\*\*|$)"
image_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
matches = re.findall(pattern, text, re.DOTALL)
image_matches = re.findall(image_pattern, text)
for key, value in matches:
    result_dict[key].append(value.strip())
pattern = r'\*\*(.*?)嘟\*\*\s*：\s*(.*?)(?=\n\n|\Z)'

matches = re.findall(pattern, text, re.DOTALL)

for key in result_dict.keys():
    images = re.findall(r'<img.*?>', '\n'.join(result_dict[key]))
    # Filter non-image content
    non_image_content = re.sub(r'<img.*?>', '', '<br>'.join(image_dict[key]))
    image_dict[key] = {'images': "<br>".join(images)}

key_ignore = []
for key, value in image_dict.items():
    if len(value["images"]) == 0:
        key_ignore.append(key)
for key in key_ignore:
    del(image_dict[key])
result_dict = dict(result_dict)
image_dict = dict(image_dict)

events = {}

for key, descriptions in result_dict.items():
    parts = key.split('.')
    if len(parts) == 3:
        year = parts[0]
        date = ".".join(parts[1:]).replace("嘟", "")
    else:
        year, date = parts[0].split('-')[0], '时间待考究'
    entry = {
        "date": date,
        "description": descriptions[0].replace("\n", "<br>")
    }
    if year not in events:
        events[year] = {"year": year, "entries": []}
    
    events[year]["entries"].append(entry)

events = list(events.values())
# print(events)

main_html_template = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生活记录</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>生活记录</h1>
        <div class="nav">
            <a href="photos.html">查看所有照片</a>
        </div>
        {% for event in events %}
        <div class="year-section">
            <h2 class="year" onclick="toggleEntries(this)">{{ event.year }}</h2>
            <div class="entry">
                {% for entry in event.entries %}
                <h3>{{ entry.date }}</h3>
                <p>{{ entry.description }}</p>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>

    <script>
        function toggleEntries(yearElement) {
            const entries = yearElement.nextElementSibling;
            entries.classList.toggle('hidden');
        }
    </script>
</body>
</html>
'''
template = Template(main_html_template)
html_content = template.render(events=events)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("main HTML file has been generated.")

image_events = {}
for key, descriptions in image_dict.items():
    parts = key.split('.')
    if len(parts) == 3:
        year = parts[0]
        date = ".".join(parts[1:]).replace("嘟", "")
    else:
        year, date = parts[0].split('-')[0], '时间待考究'

    entry = {
        "date": date,
        "images": descriptions["images"]
    }
    if year not in image_events:
        image_events[year] = {"year": year, "entries": []}
    
    image_events[year]["entries"].append(entry)

image_events = list(image_events.values())
photo_html_template = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>照片记录</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>所有照片</h1>
        <div class="nav">
            <a href="index.html">返回生活记录</a>
        </div>
        {% for event in image_events %}
        <div class="year-section">
            <h2 class="year" onclick="togglePhotos(this)">{{ event.year }}</h2>
            <div class="entry">
                {% for entry in event.entries %}
                <h3>{{ entry.date }}</h3>
                <p>{{ entry.images }}</p>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>

    <script>
        function togglePhotos(yearElement) {
            const photos = yearElement.nextElementSibling;
            photos.classList.toggle('hidden');
        }
    </script>
</body>
</html>
'''

template = Template(photo_html_template)
photo_content = template.render(image_events=image_events)
with open('photos.html', 'w', encoding='utf-8') as f:
    f.write(photo_content)

print("photos HTML file has been generated.")
