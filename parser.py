from bs4 import BeautifulSoup
import re

# 原始HTML代码（省略其他部分，仅保留需要处理的内容）
html = """
<!DOCTYPE html>
<html lang="en-US">
    <!-- 省略其他无关内容 -->
    <body>
        <!-- 省略其他无关内容 -->
        <main role="main" id="app" class="pb-3">
            <h1>GameBundle</h1>
            <h2>Bundles</h2>
            <ul>
                <li>
                    <a href="/Bundles/View?Path=%7B%22P%22%3A%5B0%5D%7D" class="btn btn-dark p-0 m-0">standalonewindows</a>
                </li>
                <li>
                    <a href="/Bundles/View?Path=%7B%22P%22%3A%5B1%5D%7D" class="btn btn-dark p-0 m-0">level1.ab</a>
                </li>
                <li>
                    <a href="/Bundles/View?Path=%7B%22P%22%3A%5B2%5D%7D" class="btn btn-dark p-0 m-0">Generated Hierarchy Assets</a>
                </li>
            </ul>
            <h2>Collections</h2>
            <ul>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A0%7D" class="btn btn-dark p-0 m-0">resources.assets</a>
                </li>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A1%7D" class="btn btn-dark p-0 m-0">unity_builtin_extra</a>
                </li>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A2%7D" class="btn btn-dark p-0 m-0">unity default resources</a>
                </li>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A3%7D" class="btn btn-dark p-0 m-0">globalgamemanagers.assets</a>
                </li>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A4%7D" class="btn btn-dark p-0 m-0">level0</a>
                </li>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A5%7D" class="btn btn-dark p-0 m-0">globalgamemanagers</a>
                </li>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A6%7D" class="btn btn-dark p-0 m-0">Generated Settings</a>
                </li>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A9%7D" class="btn btn-dark p-0 m-0">Generated Lighting Data Assets</a>
                </li>
                <li>
                    <a href="/Collections/View?Path=%7B%22B%22%3A%7B%22P%22%3A%5B%5D%7D%2C%22I%22%3A10%7D" class="btn btn-dark p-0 m-0">Sprite Data Storage</a>
                </li>
            </ul>
        </main>
        <!-- 省略其他无关内容 -->
    </body>
</html>
"""


def parse(html=html) -> dict:
    # 解析HTML
    soup = BeautifulSoup(html, "html.parser")

    # 初始化结果字典
    data = {"H1": "", "Parent": {}, "Bundles": {}, "Collections": {}, "Resources": {}}

    # 提取H1部分
    h1_tag = soup.find("h1")
    if h1_tag:
        data["H1"] = h1_tag.string

    # 提取Parent部分
    parent_heading = soup.find("h2", string="Parent")
    if parent_heading:
        link = parent_heading.find_next("a")
        if link:
            # 链接文本作为键，href作为值
            key = link.get_text(strip=True)
            value = link["href"]
            data["Parent"][key] = value

    # 提取Bundles部分
    bundles_heading = soup.find("h2", string="Bundles")
    if bundles_heading:
        bundles_list = bundles_heading.find_next("ul")
        for item in bundles_list.find_all("li"):
            link = item.find("a")
            if link:
                # 链接文本作为键，href作为值
                key = link.get_text(strip=True)
                value = link["href"]
                data["Bundles"][key] = value

    # 提取Collections部分
    collections_heading = soup.find("h2", string="Collections")
    if collections_heading:
        collections_list = collections_heading.find_next("ul")
        for item in collections_list.find_all("li"):
            link = item.find("a")
            if link:
                # 链接文本作为键，href作为值
                key = link.get_text(strip=True)
                value = link["href"]
                data["Collections"][key] = value

    # 提取Resources部分
    resources_heading = soup.find("h2", string="Resources")
    if resources_heading:
        resources_list = resources_heading.find_next("ul")
        for item in resources_list.find_all("li"):
            link = item.find("a")
            if link:
                # 链接文本作为键，href作为值
                key = link.get_text(strip=True)
                value = link["href"]
                data["Resources"][key] = value

    return data


from bs4 import BeautifulSoup


def extract_tables(html):
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    h1_tag = soup.find("h1")
    if h1_tag:
        result["H1"] = h1_tag.string

    # 获取所有<h2>标签
    h2_tags = soup.find_all("h2")

    for i, h2 in enumerate(h2_tags):
        h2_text = h2.get_text(strip=True)

        result[f"{h2_text}_links"] = list()

        # 查找当前<h2>后面的所有兄弟节点
        next_siblings = h2.find_next_siblings()
        table = None

        # 遍历兄弟节点，寻找第一个<table>（不跨<h2>）
        for sibling in next_siblings:
            # 如果遇到下一个<h2>，说明当前<h2>后没有表格
            if sibling.name == "h2":
                break
            # 遇到A链接就添加
            if sibling.name == "a":
                result[h2_text] = {sibling.string: sibling.get("href")}
                continue
            # 找到第一个<table>则停止
            if sibling.name == "table":
                table = sibling
                break

        if table:
            # 提取表格数据（列优先）
            thead = table.find("thead")
            tbody = table.find("tbody")
            if not thead or not tbody:
                result[h2_text] = None
                continue

            # 表头行
            headers = [th.get_text(strip=True) for th in thead.find_all("th")]
            # 数据行
            rows = []
            for tr in tbody.find_all("tr"):
                row_data = []
                line_links = []
                for td in tr.find_all("td"):
                    link = td.find("a")
                    row_data.append(
                        link.get_text(strip=True) if link else td.get_text(strip=True)
                    )
                    if link:
                        line_links += [link.get("href")]
                result[f"{h2_text}_links"] += (
                    [line_links[0]] if len(line_links) else [None]
                )
                rows.append(row_data)

            # 转换为列优先格式
            table_data = []
            for col_idx in range(len(headers)):
                column = [headers[col_idx]]
                for row in rows:
                    if col_idx < len(row):
                        column.append(row[col_idx])
                table_data.append(column)
            result[h2_text] = table_data
        else:
            # 没有找到表格，值为None
            if not h2_text in result.keys():
                result[h2_text] = None

    return result


from bs4 import BeautifulSoup


def parse_tab_tables(html):
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    h1_tag = soup.find("h1")
    if h1_tag:
        result["H1"] = h1_tag.string

    # 获取所有标签页按钮
    tab_buttons = soup.select('button[role="tab"][id$="-tab"]')

    for btn in tab_buttons:
        # 提取标签页名称
        tab_name = btn.get_text(strip=True)
        if not tab_name:
            result[tab_name] = None
            continue

        # 找到对应的标签页内容
        tab_target = btn.get("data-bs-target")
        if not tab_target:
            result[tab_name] = None
            continue

        tab_content = soup.select_one(f'{tab_target}[role="tabpanel"]')
        if not tab_content:
            result[tab_name] = None
            continue

        # 有图片就加图片
        image_lnk = tab_content.find("a")
        if image_lnk:
            image = image_lnk.find("img")
            if image:
                result[tab_name] = {image_lnk.get("download"): image.get("src")}
                continue

        # 有文本就加文本
        pre = tab_content.find("pre")
        if pre:
            if pre.get("dynamic-text-content"):
                text_link = tab_content.find("a")
                if text_link:
                    download = text_link.get("download")
                    if download:
                        result[tab_name] = {download: pre.get("dynamic-text-content")}
                        continue

        # 处理字体标签页
        h1 = tab_content.find("h1")
        if h1:
            # 更宽松的匹配方式，只要包含"Preview Font"即可
            if "Preview Font" in h1.get_text():
                # 精确查找带有download属性的a标签（符合你的HTML结构）
                a_tag = tab_content.find("a", {"download": ""})
                if a_tag and a_tag.get("href"):
                    result[tab_name] = a_tag.get("href")
                    continue

        # 有视频加视频
        vdo = tab_content.find("video")
        if vdo:
            src = vdo.find("source")
            if src:
                result[tab_name] = src.get("src")
                continue

        pre = tab_content.find("pre")
        if pre:
            if pre.get("dynamic-text-content"):
                link = tab_content.find("a")
                if link:
                    if link.get("download"):
                        result[tab_name] = {
                            link.get("download"): pre.get("dynamic-text-content")
                        }
                        continue

        # 查找标签页内的表格
        table = tab_content.find("table", class_="table")
        if not table:
            model_table = tab_content.find("table")
            if model_table:
                if tab_content.find_all("canvas"):
                    canvas = tab_content.find_all("canvas")[0]
                    if canvas.get("glb-data-path"):
                        result[tab_name] = canvas.get("glb-data-path")
                        continue
                elif tab_content.find_all("audio"):
                    audo = tab_content.find_all("audio")[0]
                    if audo.get("src"):
                        result[tab_name] = audo.get("src")
                        continue

            result[tab_name] = None
            continue

        # 提取表格行（不区分thead和tbody，统一处理所有行）
        rows = []
        links = []
        for tr in table.find_all("tr"):
            # 每行第一个th作为表头，后续td作为数据
            th_element = tr.find("th")
            td_elements = tr.find_all("td")

            if th_element:
                # 表头文本（左侧表头）
                header = th_element.get_text(strip=True)
                # 数据部分（处理链接）
                data = []
                for td in td_elements:
                    link = td.find("a")
                    data.append(
                        link.get_text(strip=True) if link else td.get_text(strip=True)
                    )
                    if link:
                        if link.get("href"):
                            links.append(link.get("href"))
                        else:
                            links.append(None)
                    else:
                        links.append(None)
                rows.append([header] + data)

        # 验证是否有有效数据
        if not rows:
            result[tab_name] = None
            continue

        # 转换为列优先格式（左侧表头作为第一列）
        # 计算最大列数（处理可能的列数不一致情况）
        max_cols = max(len(row) for row in rows)
        column_data = []

        for col_idx in range(max_cols):
            column = []
            for row in rows:
                if col_idx < len(row):
                    column.append(row[col_idx])
            column_data.append(column)

        result[tab_name] = column_data
        result[f"{tab_name}_links"] = links

    return result


def extract_filename(content_disposition):
    # 正则表达式：匹配三种常见格式
    # 1. filename="xxx.ttf"（带引号）
    # 2. filename=xxx.ttf（不带引号）
    # 3. filename*=UTF-8''xxx.ttf（UTF-8编码）
    pattern = r'filename(?:\*=UTF-8\'\'|=)["\']?(.*?)["\';]'
    # 解释：
    # - filename(?:\*=UTF-8\'\'|=)：匹配 "filename=" 或 "filename*=UTF-8''"
    # - ["\']?：可选的引号（单引号或双引号）
    # - (.*?)：非贪婪匹配文件名
    # - ["\';]：匹配结束的引号、分号或其他分隔符

    match = re.search(pattern, content_disposition, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


from bs4 import BeautifulSoup
from typing import Dict, Any


def parse_resources_html(html: str) -> Dict[str, Any]:
    """
    解析HTML代码，提取h1、指定a链接、p标签内容，并按h2标题分组

    参数:
        html: 待解析的HTML字符串
    返回:
        包含提取信息的字典，结构如示例所示
    """
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    # 1. 提取h1标签内容
    h1_tag = soup.find("h1")
    if h1_tag:
        result["h1"] = h1_tag.get_text(strip=True)

    # 2. 提取所有h2标签，按顺序处理其后续兄弟节点
    h2_tags = soup.find_all("h2")
    current_h2_key = None  # 记录当前活跃的h2标题（作为字典键）

    for tag in soup.find_all(["h2", "a", "p"]):  # 只关注这三种标签
        if tag.name == "h2":
            # 遇到新的h2，更新当前键（转为小写便于统一处理）
            current_h2_key = tag.get_text(strip=True).lower()
            result[current_h2_key] = {}  # 初始化该h2对应的字典
        else:
            if current_h2_key is None:
                continue  # 忽略h2之前的内容

            # 3. 提取文本状a链接（class含btn-dark，无download属性）
            if tag.name == "a" and "btn-dark" in tag.get("class", []):
                link_text = tag.get_text(strip=True)
                link_href = tag.get("href", "")
                if link_text and link_href:
                    result[current_h2_key][link_text] = link_href

            # 4. 提取p标签内容（对应h2标题）
            elif tag.name == "p":
                p_text = tag.get_text(strip=True)
                result[current_h2_key] = p_text  # 覆盖初始空字典

    # 5. 提取按钮状a链接（class含btn-primary，有download属性）
    btn_primary_a = soup.find("a", class_="btn-primary", download=True)
    if btn_primary_a:
        download_text = btn_primary_a.get("download", "").strip()
        download_href = btn_primary_a.get("href", "").strip()
        if download_text and download_href:
            # 以按钮文本（download属性值）作为键
            button_key = btn_primary_a.get_text(strip=True).lower()
            result[button_key] = {download_text: download_href}

    return result


from bs4 import BeautifulSoup
from typing import Dict, Optional


def extract_version_info(html: str) -> Dict[str, str]:
    """
    从HTML中解析出版本号及其对应的链接，返回格式为{"版本号": "链接"}的字典

    参数:
        html: 包含版本信息的HTML字符串
    返回:
        包含版本号和对应链接的字典，若未找到则返回空字典
    """
    # 解析HTML
    soup = BeautifulSoup(html, "html.parser")

    # 定位包含版本信息的链接：
    # 特征是位于"Export"下拉菜单下，且href以"unityhub://"开头
    version_link = soup.find(
        "a",
        class_="dropdown-item",
        href=lambda href: href and href.startswith("unityhub://"),
    )

    # 提取版本号和链接
    if version_link:
        # 版本号是链接的文本内容
        version_number = version_link.get_text(strip=True)
        # 链接是href属性值
        version_href = version_link.get("href", "").strip()
        if version_number and version_href:
            return {version_number: version_href}

    # 未找到时返回空字典
    return {}


from bs4 import BeautifulSoup
from typing import Dict, Any


def extract_form_data(html: str) -> Dict[str, Any]:
    """
    从HTML中提取表单数据，按类型整理为字典：
    - select：键为前置label文本，值为选中option的索引
    - input[type="text"]：键为前置label文本，值为输入内容
    - checkbox：键为后置label文本，值为是否勾选（bool）
    """
    soup = BeautifulSoup(html, "html.parser")
    form_data = {}

    # 1. 处理 select 元素
    for select in soup.find_all("select"):
        # 找到对应的 label（for 属性与 select 的 id 匹配）
        select_id = select.get("id") or select.get("name")
        label = soup.find("label", attrs={"for": select_id})
        if not label:
            continue  # 跳过无标签的 select
        label_text = label.get_text(strip=True)

        # 找到选中的 option 并计算索引
        options = select.find_all("option")
        for idx, option in enumerate(options):
            if option.has_attr("selected"):
                form_data[label_text] = idx
                break  # 只取第一个选中项

    # 2. 处理 input[type="text"]
    for text_input in soup.find_all("input", type="text"):
        # 找到对应的 label（for 属性与 input 的 id 匹配）
        input_id = text_input.get("id") or text_input.get("name")
        label = soup.find("label", attrs={"for": input_id})
        if not label:
            continue  # 跳过无标签的输入框
        label_text = label.get_text(strip=True)

        # 获取输入框的值（value属性）
        input_value = text_input.get("value", "").strip()
        form_data[label_text] = input_value

    # 3. 处理 checkbox（input[type="checkbox"]）
    for checkbox in soup.find_all("input", type="checkbox"):
        # 找到对应的 label（紧跟在 checkbox 后面的 label）
        # 优先通过 for 属性匹配，无匹配则取相邻的下一个 label
        checkbox_id = checkbox.get("id")
        label = soup.find("label", attrs={"for": checkbox_id})
        if not label:
            # 查找相邻的下一个 label 标签
            label = checkbox.find_next_sibling("label")
        if not label:
            continue  # 跳过无标签的复选框
        label_text = label.get_text(strip=True)

        # 判断是否勾选（存在 checked 属性则为 True）
        is_checked = checkbox.has_attr("checked")
        form_data[label_text] = is_checked

    return form_data


from bs4 import BeautifulSoup


def parse_form_names(html_content):
    """
    解析HTML表单内容，提取各种表单元素的信息

    参数:
        html_content: 包含表单的HTML内容字符串

    返回:
        包含表单元素信息的字典
    """
    soup = BeautifulSoup(html_content, "html.parser")
    result = {}

    # 处理复选框(checkbox)
    checkboxes = soup.find_all("input", type="checkbox")
    for checkbox in checkboxes:
        name = checkbox.get("name")
        if not name:
            continue

        # 查找对应的label文本
        label = soup.find("label", {"for": checkbox.get("id")})
        label_text = label.get_text(strip=True) if label else f"未找到标签_{name}"

        result[label_text] = name

    # 处理下拉选择框(select)
    selects = soup.find_all("select")
    for select in selects:
        name = select.get("name")
        if not name:
            continue

        # 查找前面的label文本
        label = select.find_previous("label", {"for": select.get("id")})
        # 如果没找到通过for关联的label，尝试查找最近的label
        if not label:
            label = select.find_previous("label")
        label_text = label.get_text(strip=True) if label else f"未找到标签_{name}"

        result[label_text] = name

        # 提取所有option的value
        options = []
        for option in select.find_all("option"):
            option_value = option.get("value")
            if option_value:
                options.append(option_value)

        # 以"name_options"为键存储选项列表
        result[f"{name}_options"] = options

    # 处理文本输入框(text input)
    text_inputs = soup.find_all("input", type="text")
    for input_elem in text_inputs:
        name = input_elem.get("name")
        if not name:
            continue

        # 查找对应的label文本
        label = soup.find("label", {"for": input_elem.get("id")})
        # 如果没找到通过for关联的label，尝试查找最近的label
        if not label:
            label = input_elem.find_previous("label")
        label_text = label.get_text(strip=True) if label else f"未找到标签_{name}"

        result[label_text] = name

    return result


from bs4 import BeautifulSoup


def extract_config_data(html_content):
    """
    从HTML中提取配置数据，返回包含键值对的字典

    参数:
        html_content: 包含配置信息的HTML内容字符串

    返回:
        字典，键为nav标签的文本，值为包含pre内容和hidden input值的列表
    """
    soup = BeautifulSoup(html_content, "html.parser")
    result = {}

    # 找到第一个class包含'tab-pane'的div元素
    first_tab_pane = soup.find("div", class_="tab-pane")
    if not first_tab_pane:
        return result  # 未找到目标元素则返回空字典

    # 获取该div中所有的nav标签（导航按钮）
    nav_buttons = first_tab_pane.find_all("button", class_="nav-link")
    if not nav_buttons:
        return result

    # 遍历每个导航按钮，提取对应的数据
    for button in nav_buttons:
        # 获取导航按钮的文本作为键（去除首尾空格）
        nav_key = button.get_text(strip=True)

        # 获取按钮对应的标签页ID（data-bs-target属性值）
        target_id = button.get("data-bs-target", "").lstrip("#")  # 去除可能的#前缀
        if not target_id:
            continue

        # 查找对应的标签页元素
        tab_content = first_tab_pane.find("div", id=target_id)
        if not tab_content:
            continue

        # 查找pre标签和hidden input
        pre_tag = tab_content.find("pre")
        # 修复这里的参数冲突问题，使用attrs字典指定属性筛选条件
        hidden_input = tab_content.find(
            "input", attrs={"type": "hidden", "name": "Key"}
        )

        # 构建值列表
        value_list = []
        if pre_tag:
            # 有pre标签时，第一项为pre内容，第二项为hidden input值
            pre_content = pre_tag.get_text(strip=True)
            value_list.append(pre_content)
            if hidden_input:
                value_list.append(hidden_input.get("value", ""))
        else:
            # 没有pre标签时，查找p标签，值列表仅包含hidden input值
            p_tag = tab_content.find("p")
            if p_tag and hidden_input:
                value_list.append(hidden_input.get("value", ""))

        # 只有当值列表有内容时才添加到结果
        if value_list:
            result[nav_key] = value_list

    return result


# 使用示例
if __name__ == "__main__":
    # 示例HTML内容（可替换为实际内容）
    sample_html = """<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Configuration Files</title><link rel="stylesheet" href="/css/bootstrap.min.css"><link rel="stylesheet" href="/css/site.css"></head><body data-bs-theme="dark"><header><div class="btn-group"><div class="btn-group dropdown"><button class="btn btn-dark dropdown-toggle mx-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">File</button><ul class="dropdown-menu" style=""><li><form action="/LoadFile" method="post"><input type="submit" class="dropdown-item" value="Open File"></form></li><li><form action="/LoadFolder" method="post"><input type="submit" class="dropdown-item" value="Open Folder"></form></li><li><form action="/Reset" method="post"><input type="submit" class="dropdown-item" value="Reset"></form></li><li><hr class="dropdown-divider"></li><li><a class="dropdown-item" href="/Settings/Edit">Settings</a></li></ul></div><div class="btn-group dropdown"><button class="btn btn-dark dropdown-toggle mx-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">View</button><ul class="dropdown-menu"><li><a class="dropdown-item" href="/">Home</a></li><li><a class="dropdown-item" href="/Settings/Edit">Settings</a></li><li><a class="dropdown-item" href="/ConfigurationFiles">Configuration Files</a></li><li><a class="dropdown-item" href="/Commands">Commands</a></li><li><a class="dropdown-item" href="/Privacy">Privacy</a></li><li><a class="dropdown-item" href="/Licenses">Licenses</a></li><li><a class="dropdown-item" href="/openapi.json">OpenAPI JSON</a></li><li><a class="dropdown-item" href="/swagger">Swagger Documentation</a></li></ul></div><div class="btn-group dropdown"><button class="btn btn-dark dropdown-toggle mx-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">Export</button><ul class="dropdown-menu"><li><a class="dropdown-item disabled" aria-diabled="true">Export All Files</a></li></ul></div><div class="btn-group dropdown"><button class="btn btn-dark dropdown-toggle mx-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">Language</button><ul class="dropdown-menu"><li><form action="/Localization?code=ar" method="post"><input type="submit" class="dropdown-item" value="العربية"></form></li><li><form action="/Localization?code=de" method="post"><input type="submit" class="dropdown-item" value="Deutsch"></form></li><li><form action="/Localization?code=el" method="post"><input type="submit" class="dropdown-item" value="Ελληνικά"></form></li><li><form action="/Localization?code=en-US" method="post"><input type="submit" class="dropdown-item" value="English (United States)"></form></li><li><form action="/Localization?code=es" method="post"><input type="submit" class="dropdown-item" value="español"></form></li><li><form action="/Localization?code=fa" method="post"><input type="submit" class="dropdown-item" value="فارسی"></form></li><li><form action="/Localization?code=fr" method="post"><input type="submit" class="dropdown-item" value="français"></form></li><li><form action="/Localization?code=id" method="post"><input type="submit" class="dropdown-item" value="Indonesia"></form></li><li><form action="/Localization?code=it" method="post"><input type="submit" class="dropdown-item" value="italiano"></form></li><li><form action="/Localization?code=ja" method="post"><input type="submit" class="dropdown-item" value="日本語"></form></li><li><form action="/Localization?code=ko" method="post"><input type="submit" class="dropdown-item" value="한국어"></form></li><li><form action="/Localization?code=nl" method="post"><input type="submit" class="dropdown-item" value="Nederlands"></form></li><li><form action="/Localization?code=pl" method="post"><input type="submit" class="dropdown-item" value="polski"></form></li><li><form action="/Localization?code=pt-BR" method="post"><input type="submit" class="dropdown-item" value="português (Brasil)"></form></li><li><form action="/Localization?code=ro" method="post"><input type="submit" class="dropdown-item" value="română"></form></li><li><form action="/Localization?code=ru" method="post"><input type="submit" class="dropdown-item" value="русский"></form></li><li><form action="/Localization?code=th" method="post"><input type="submit" class="dropdown-item" value="ไทย"></form></li><li><form action="/Localization?code=tr" method="post"><input type="submit" class="dropdown-item" value="Türkçe"></form></li><li><form action="/Localization?code=uk" method="post"><input type="submit" class="dropdown-item" value="українська"></form></li><li><form action="/Localization?code=zh-Hans" method="post"><input type="submit" class="dropdown-item" value="中文（简体）"></form></li><li><form action="/Localization?code=zh-Hant" method="post"><input type="submit" class="dropdown-item" value="中文（繁體）"></form></li></ul></div></div></header><div class="container"><main role="main" id="app" class="pb-3"><h1>Configuration Files</h1><nav class="nav nav-tabs" id="nav-tab" role="tablist"><button class="nav-link active" id="nav-8440fe13-fe23-419d-9d11-eec6ab99bb6d-tab" data-bs-toggle="tab" data-bs-target="#nav-8440fe13-fe23-419d-9d11-eec6ab99bb6d" type="button" role="tab" aria-controls="nav-8440fe13-fe23-419d-9d11-eec6ab99bb6d" aria-selected="true">Singletons</button><button class="nav-link" id="nav-9b0c286b-1a06-4ead-833e-d06167af7891-tab" data-bs-toggle="tab" data-bs-target="#nav-9b0c286b-1a06-4ead-833e-d06167af7891" type="button" role="tab" aria-controls="nav-9b0c286b-1a06-4ead-833e-d06167af7891" aria-selected="false" tabindex="-1">Lists</button></nav><div class="tab-content"><div class="tab-pane fade show active" id="nav-8440fe13-fe23-419d-9d11-eec6ab99bb6d" role="tabpanel" aria-labelledby="nav-8440fe13-fe23-419d-9d11-eec6ab99bb6d-tab"><div class="container"><div class="row"><div class="col-3 text-center"><nav class="nav nav-pills flex-column" id="nav-tab" role="tablist"><button class="nav-link active" id="nav-13b00187-d84b-4f0b-923c-65f83c58bf23-tab" data-bs-toggle="tab" data-bs-target="#nav-13b00187-d84b-4f0b-923c-65f83c58bf23" type="button" role="tab" aria-controls="nav-13b00187-d84b-4f0b-923c-65f83c58bf23" aria-selected="true">ImportSettings</button><button class="nav-link" id="nav-3882b699-ee4d-4c22-95f0-86da54c19f2f-tab" data-bs-toggle="tab" data-bs-target="#nav-3882b699-ee4d-4c22-95f0-86da54c19f2f" type="button" role="tab" aria-controls="nav-3882b699-ee4d-4c22-95f0-86da54c19f2f" aria-selected="false" tabindex="-1">ProcessingSettings</button><button class="nav-link" id="nav-f14458a1-436b-4b04-a1fd-4745389ae15b-tab" data-bs-toggle="tab" data-bs-target="#nav-f14458a1-436b-4b04-a1fd-4745389ae15b" type="button" role="tab" aria-controls="nav-f14458a1-436b-4b04-a1fd-4745389ae15b" aria-selected="false" tabindex="-1">ExportSettings</button><button class="nav-link" id="nav-7f4455e1-8bea-4907-a7c1-9f59685b7d1d-tab" data-bs-toggle="tab" data-bs-target="#nav-7f4455e1-8bea-4907-a7c1-9f59685b7d1d" type="button" role="tab" aria-controls="nav-7f4455e1-8bea-4907-a7c1-9f59685b7d1d" aria-selected="false" tabindex="-1">EngineResourceData</button></nav></div><div class="col-9"><div class="tab-content"><div class="tab-pane fade show active" id="nav-13b00187-d84b-4f0b-923c-65f83c58bf23" role="tabpanel" aria-labelledby="nav-13b00187-d84b-4f0b-923c-65f83c58bf23-tab"><pre class="bg-dark-subtle rounded-3 p-2">{
  "ScriptContentLevel": 2,
  "StreamingAssetsMode": 1,
  "DefaultVersion": "0.0.0a0",
  "TargetVersion": "0.0.0a0"
}</pre><div class="row text-center"><div class="col"><form action="/ConfigurationFiles/Singleton/Add" method="post"><input type="hidden" name="Key" value="ImportSettings"><input type="submit" class="btn btn-primary mx-1" value="Replace"></form></div><div class="col"><form action="/ConfigurationFiles/Singleton/Remove" method="post"><input type="hidden" name="Key" value="ImportSettings"><input type="submit" class="btn btn-danger mx-1" value="Remove"></form></div></div></div><div class="tab-pane fade" id="nav-3882b699-ee4d-4c22-95f0-86da54c19f2f" role="tabpanel" aria-labelledby="nav-3882b699-ee4d-4c22-95f0-86da54c19f2f-tab"><pre class="bg-dark-subtle rounded-3 p-2">{
  "EnablePrefabOutlining": false,
  "EnableStaticMeshSeparation": true,
  "EnableAssetDeduplication": false,
  "RemoveNullableAttributes": false,
  "PublicizeAssemblies": false,
  "BundledAssetsExportMode": 2
}</pre><div class="row text-center"><div class="col"><form action="/ConfigurationFiles/Singleton/Add" method="post"><input type="hidden" name="Key" value="ProcessingSettings"><input type="submit" class="btn btn-primary mx-1" value="Replace"></form></div><div class="col"><form action="/ConfigurationFiles/Singleton/Remove" method="post"><input type="hidden" name="Key" value="ProcessingSettings"><input type="submit" class="btn btn-danger mx-1" value="Remove"></form></div></div></div><div class="tab-pane fade" id="nav-f14458a1-436b-4b04-a1fd-4745389ae15b" role="tabpanel" aria-labelledby="nav-f14458a1-436b-4b04-a1fd-4745389ae15b-tab"><pre class="bg-dark-subtle rounded-3 p-2">{
  "AudioExportFormat": 2,
  "ImageExportFormat": 4,
  "LightmapTextureExportFormat": 2,
  "ScriptExportMode": 1,
  "ScriptLanguageVersion": -1,
  "ScriptTypesFullyQualified": false,
  "ShaderExportMode": 0,
  "SpriteExportMode": 0,
  "TextExportMode": 2,
  "SaveSettingsToDisk": false,
  "LanguageCode": null
}</pre><div class="row text-center"><div class="col"><form action="/ConfigurationFiles/Singleton/Add" method="post"><input type="hidden" name="Key" value="ExportSettings"><input type="submit" class="btn btn-primary mx-1" value="Replace"></form></div><div class="col"><form action="/ConfigurationFiles/Singleton/Remove" method="post"><input type="hidden" name="Key" value="ExportSettings"><input type="submit" class="btn btn-danger mx-1" value="Remove"></form></div></div></div><div class="tab-pane fade" id="nav-7f4455e1-8bea-4907-a7c1-9f59685b7d1d" role="tabpanel" aria-labelledby="nav-7f4455e1-8bea-4907-a7c1-9f59685b7d1d-tab"><div class="text-center"><p class="p-2">No data has been loaded for this key.</p><form action="/ConfigurationFiles/Singleton/Add" method="post"><input type="""
    import pprint

    pprint.pprint(extract_config_data(sample_html))

# # 使用示例
# if __name__ == "__main__":
#     # 这里替换为实际的HTML内容
#     sample_html = """
#     <form action="/Settings/Update" method="post">
#         <!-- 示例复选框 -->
#         <div class="form-check">
#             <input class="form-check-input" type="checkbox" value="" id="IgnoreStreamingAssets" name="IgnoreStreamingAssets">
#             <label class="form-check-label" for="IgnoreStreamingAssets">Skip StreamingAssets Folder</label>
#         </div>

#         <!-- 示例下拉框 -->
#         <label class="form-label" for="BundledAssetsExportMode">Bundled Assets Export Mode</label>
#         <select class="form-select" name="BundledAssetsExportMode" id="BundledAssetsExportMode">
#             <option value="GroupByAssetType">Group By Asset Type</option>
#             <option value="GroupByBundleName">Group By Bundle Name</option>
#             <option value="DirectExport" selected>Direct Export</option>
#         </select>

#         <!-- 示例文本输入框 -->
#         <label class="form-label" for="DefaultVersion">Default Version</label>
#         <input type="text" class="form-control" id="DefaultVersion" name="DefaultVersion" value="0.0.0a0">
#     </form>
#     """

#     form_data = parse_form_names(sample_html)
#     for key, value in form_data.items():
#         print(f"{key}: {value}")


# # 测试函数
# if __name__ == "__main__":
#     # 传入示例HTML（省略部分重复内容，实际使用完整HTML）
#     html_content = """<html lang="en-US">
#         <!-- 省略头部内容 -->
#         <form action="/Settings/Update" method="post">
#             <!-- 省略其他内容 -->
#             <div class="row">
#                 <div class="col">
#                     <label class="form-label" for="DefaultVersion">Default Version</label>
#                     <input type="text" class="form-control" id="DefaultVersion" name="DefaultVersion" value="0.0.0a0">
#                 </div>
#             </div>
#             <div class="row">
#                 <div class="col">
#                     <label class="form-label" for="BundledAssetsExportMode">Bundled Assets Export Mode</label>
#                     <select class="form-select" name="BundledAssetsExportMode">
#                         <option value="GroupByAssetType">Group By Asset Type</option>
#                         <option value="GroupByBundleName">Group By Bundle Name</option>
#                         <option value="DirectExport" selected>Direct Export</option>
#                     </select>
#                 </div>
#             </div>
#             <div class="form-check">
#                 <input class="form-check-input" type="checkbox" value="" id="IgnoreStreamingAssets" name="IgnoreStreamingAssets">
#                 <label class="form-check-label" for="IgnoreStreamingAssets">Skip StreamingAssets Folder</label>
#             </div>
#             <!-- 省略其他内容 -->
#         </form>
#         <!-- 省略尾部内容 -->
#     </html>"""

#     # 提取表单数据
#     form_data = extract_form_data(html_content)

#     # 打印结果（格式化输出）
#     import pprint

#     pprint.pprint(form_data)

# # 测试函数
# if __name__ == "__main__":
#     # 示例HTML（可替换为实际需要解析的HTML内容）
#     html_content = """<!DOCTYPE html>
# <html lang="en-US">
#     <head>
#         <meta charset="utf-8"/>
#         <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
#         <title>AssetRipper Free</title>
#         <link rel="stylesheet" href="/css/bootstrap.min.css"/>
#         <link rel="stylesheet" href="/css/site.css"/>
#     </head>
#     <body data-bs-theme="dark">
#         <!-- 省略中间部分HTML -->
#         <div class="btn-group dropdown">
#             <button class="btn btn-dark dropdown-toggle mx-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">Export</button>
#             <ul class="dropdown-menu">
#                 <li>
#                     <a class="dropdown-item" href="/Commands">Export All Files</a>
#                 </li>
#                 <li>
#                     <a class="dropdown-item" target="_blank" rel="noopener noreferrer" href="unityhub://2022.3.20f1c1">2022.3.20f1c1</a>
#                 </li>
#             </ul>
#         </div>
#         <!-- 省略剩余HTML -->
#     </body>
# </html>"""

#     # 调用函数提取版本信息
#     version_info = extract_version_info(html_content)
#     print(version_info)  # 输出: {'2022.3.20f1c1': 'unityhub://2022.3.20f1c1'}


# # 测试函数
# if __name__ == "__main__":
#     # 传入示例HTML代码（省略部分重复内容，实际使用完整HTML）
#     html = """<html lang="en-US"><head>...</head><body>...
#         <h1>cab-eb4da0e8c71c10a884a7aef246f1fa57.resource</h1>
#         <h2>Bundle</h2>
#         <a href="/Bundles/View?Path=%7B%22P%22%3A%5B2%5D%7D" class="btn btn-dark p-0 m-0">test.ab</a>
#         <h2>Size</h2>
#         <p>67495748</p>
#         <div class="text-center">
#             <a href="/Resources/Data?Path=%7B%22B%22%3A%7B%22P%22%3A%5B2%5D%7D%2C%22I%22%3A0%7D"
#                download="cab-eb4da0e8c71c10a884a7aef246f1fa57.resource"
#                class="btn btn-primary">Save</a>
#         </div>
#     ...</body></html>"""

#     parsed = parse_resources_html(html)
#     import pprint

#     pprint.pprint(parsed)

# # 测试代码
# if __name__ == "__main__":
#     html = """
#     <html lang="en-US">
#     <body>
#         <nav class="nav nav-tabs">
#             <button id="nav-information-tab" data-bs-target="#nav-information" role="tab">Information</button>
#             <button id="nav-development-tab" data-bs-target="#nav-development" role="tab">Development</button>
#         </nav>

#         <div class="tab-content">
#             <!-- 左侧表头表格 -->
#             <div id="nav-information" role="tabpanel">
#                 <table class="table">
#                     <tbody>
#                         <tr><th>Collection</th><td><a href="#">sharedassets1.assets</a></td></tr>
#                         <tr><th>Path ID</th><td>20</td><td>额外数据</td></tr>  <!-- 演示多列数据 -->
#                         <tr><th>Width</th><td>64</td></tr>
#                     </tbody>
#                 </table>
#             </div>

#             <!-- 单行列表示例 -->
#             <div id="nav-development" role="tabpanel">
#                 <table class="table">
#                     <tbody>
#                         <tr><th>C# Type</th><td>Texture2D_2023_2_0_a19</td></tr>
#                     </tbody>
#                 </table>
#             </div>
#         </div>
#     </body>
#     </html>
#     """

#     parsed_result = parse_tab_tables(html)
#     import pprint

#     pprint.pprint(parsed_result)

# # # 测试代码
# # if __name__ == "__main__":
# #     # 包含无表格的<h2>标签的示例HTML
# #     html = """
# #     <html>
# #         <body>
# #             <h2>Bundle</h2>
# #             <a href="/link">GameBundle</a>  <!-- 无表格 -->

# #             <h2>Assets</h2>
# #             <table>
# #                 <thead><tr><th>Path ID</th><th>Class</th></tr></thead>
# #                 <tbody>
# #                     <tr><td>1</td><td>EditorBuildSettings</td></tr>
# #                 </tbody>
# #             </table>

# #             <h2>EmptyGroup</h2>
# #             <p>这是一个没有表格的分组</p>  <!-- 无表格 -->
# #         </body>
# #     </html>
# #     """

# #     extracted = extract_tables(html)
# #     import pprint

# #     pprint.pprint(extracted)

# # # 打印结果
# # import pprint

# # if __name__ == "__main__":
# #     pprint.pprint(parse())
