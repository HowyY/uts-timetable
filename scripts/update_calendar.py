import requests

# UTS 课表 URL
URL = "https://mytimetablecloud.uts.edu.au/odd/rest/calendar/ical/bfe4bd9a-7114-4575-a582-9ea1ee74d449"
ICS_FILE = "filtered_calendar.ics"

def download_and_filter_calendar():
    """下载 UTS 课程表并正确过滤掉 PRERECORDED 课程"""
    response = requests.get(URL)
    if response.status_code != 200:
        print("下载失败，状态码:", response.status_code)
        return
    
    ics_data = response.text.splitlines()
    new_lines = []
    inside_event = False
    skip_event = False

    for line in ics_data:
        if line.startswith("BEGIN:VEVENT"):
            inside_event = True
            skip_event = False  # 默认不跳过

        if inside_event and "LOCATION:PRERECORDED" in line:
            skip_event = True  # 发现 PRERECORDED，标记为跳过整个事件

        if not skip_event:
            new_lines.append(line)

        if line.startswith("END:VEVENT"):
            inside_event = False  # 事件结束
            if skip_event:
                new_lines.pop()  # 确保不保存 `END:VEVENT`，如果该事件被跳过

    # 重新组合内容并保存
    with open(ICS_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(new_lines) + "\n")  # 确保末尾有换行符

    print(f"✅ 更新完成！{ICS_FILE} 已生成。")

if __name__ == "__main__":
    download_and_filter_calendar()
