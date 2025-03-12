import requests

# UTS 课表 URL
URL = "https://mytimetablecloud.uts.edu.au/odd/rest/calendar/ical/bfe4bd9a-7114-4575-a582-9ea1ee74d449"
ICS_FILE = "filtered_calendar.ics"

def download_and_filter_calendar():
    """下载 UTS 课程表并过滤掉 PRERECORDED 课程"""
    response = requests.get(URL)
    if response.status_code != 200:
        print("下载失败，状态码:", response.status_code)
        return
    
    ics_data = response.text
    new_lines = []
    inside_event = False
    skip_event = False

    for line in ics_data.split("\n"):
        if line.startswith("BEGIN:VEVENT"):
            inside_event = True
            skip_event = False
        elif line.startswith("END:VEVENT"):
            inside_event = False
            if not skip_event:
                new_lines.append(line)
            continue
        
        if inside_event and "Location: PRERECORDED" in line:
            skip_event = True

        if not skip_event:
            new_lines.append(line)

    # 保存到文件
    with open(ICS_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(new_lines))

    print(f"更新完成！{ICS_FILE} 已生成。")

if __name__ == "__main__":
    download_and_filter_calendar()
