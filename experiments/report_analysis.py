import os

import re


def parse_similarity_data(html_content):
    pattern = re.compile(
        r"<p>(?:\(\w+\)\s+)?"  # Необязательный префикс (nn)
        r'Similarity of <span class="grey">([^<]+)</span> to <span class="grey">([^<]+)</span> is <span class="[^"]+">([\d.]+)%</span>',
        re.MULTILINE,
    )

    similarity_dict = {}
    matches = pattern.findall(html_content)

    for a, b, percent in matches:
        key = (a, b)
        value = float(percent)
        similarity_dict.setdefault(key, []).append(value)

    return similarity_dict


def analyze_similarity_stats(data, stats1=None):
    stats = {
        "original_plagiarized": {
            "class1": {"<=50": 0, "<=80": 0, "80<": 0, "total": 0},
            "class2": {"<=50": 0, "<=80": 0, "80<": 0, "total": 0},
        },
        "original_nonplagiarized": {
            "class1": {"<=50": 0, "<=80": 0, "80<": 0, "total": 0},
            "class2": {"<=50": 0, "<=80": 0, "80<": 0, "total": 0},
        },
    }

    if stats1:
        stats = stats1

    if not data:
        return stats

    total_classes = len(next(iter(data.values())))

    for class_idx in range(total_classes):
        for key in data:
            val = data[key][class_idx]

            if {"original", "plagiarized"} == set(key):
                stats["original_plagiarized"][f"class{class_idx + 1}"]["total"] += 1
                if val <= 50:
                    stats["original_plagiarized"][f"class{class_idx + 1}"]["<=50"] += 1
                if 50 < val <= 80:
                    stats["original_plagiarized"][f"class{class_idx + 1}"]["<=80"] += 1
                if 80 < val:
                    stats["original_plagiarized"][f"class{class_idx + 1}"]["80<"] += 1

            elif "original" in key and any("non-plagiarized" in k for k in key):
                stats["original_nonplagiarized"][f"class{class_idx + 1}"]["total"] += 1
                if val <= 50:
                    stats["original_nonplagiarized"][f"class{class_idx + 1}"][
                        "<=50"
                    ] += 1
                if 50 < val <= 80:
                    stats["original_nonplagiarized"][f"class{class_idx + 1}"][
                        "<=80"
                    ] += 1
                if 80 < val:
                    stats["original_nonplagiarized"][f"class{class_idx + 1}"][
                        "80<"
                    ] += 1

    return stats


def generate_html(stats, filename, info, formula):
    html_template = """
    <html>
    <head>
        <title>Статистика схожести</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            table {{ border-collapse: collapse; margin: 20px 0; width: 600px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
            th {{ background-color: #f8f9fa; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .class1 {{ background-color: #e6f7ff; }}
            .class2 {{ background-color: #fff2e6; }}
            .metric {{ font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Анализ схожести текстов</h1>

        <h1>Description</h1>
        <p>{info}</p>

        <h2>Formula</h2>
        <pre style="background-color: #f4f4f4; border: 1px solid #ccc; padding: 10px; border-radius: 5px;"><code>{code}</code>
        </pre>

        <h2>Original vs Plagiarized</h2>
        {op_tables}

        <h2>Original vs Non-Plagiarized</h2>
        {on_tables}
    </body>
    </html>
    """

    op_tables = []
    for i in range(2):
        class_data = stats["original_plagiarized"][f"class{i + 1}"]
        total = class_data["total"]
        op_tables.append(
            f"""
        <div class="class{i + 1}">
            <h3>Класс {i + 1}</h3>
            <table>
                <tr>
                    <th>Метрика</th>
                    <th>Количество</th>
                    <th>Процент</th>
                </tr>
                <tr>
                    <td class="metric">0 - 50 (inclusive)</td>
                    <td>{class_data['<=50']}/{total}</td>
                    <td>{(class_data['<=50'] / total * 100 if total else 0):.2f}%</td>
                </tr>
                <tr>
                    <td class="metric">50 - 80 (inclusive)</td>
                    <td>{class_data['<=80']}/{total}</td>
                    <td>{(class_data['<=80'] / total * 100 if total else 0):.2f}%</td>
                </tr>
                <tr>
                    <td class="metric">80 - 100</td>
                    <td>{class_data['80<']}/{total}</td>
                    <td>{(class_data['80<'] / total * 100 if total else 0):.2f}%</td>
                </tr>
            </table>
        </div>
        """
        )

    on_tables = []
    for i in range(2):
        class_data = stats["original_nonplagiarized"][f"class{i + 1}"]
        total = class_data["total"]
        on_tables.append(
            f"""
        <div class="class{i + 1}">
            <h3>Класс {i + 1}</h3>
            <table>
                <tr>
                    <th>Метрика</th>
                    <th>Количество</th>
                    <th>Процент</th>
                </tr>
                <tr>
                    <td class="metric">0 - 50 (inclusive)</td>
                    <td>{class_data['<=50']}/{total}</td>
                    <td>{(class_data['<=50'] / total * 100 if total else 0):.2f}%</td>
                </tr>
                <tr>
                    <td class="metric">50 - 80 (inclusive)</td>
                    <td>{class_data['<=80']}/{total}</td>
                    <td>{(class_data['<=80'] / total * 100 if total else 0):.2f}%</td>
                </tr>
                <tr>
                    <td class="metric">80 - 100</td>
                    <td>{class_data['80<']}/{total}</td>
                    <td>{(class_data['80<'] / total * 100 if total else 0):.2f}%</td>
                </tr>
            </table>
        </div>
        """
        )

    html_content = html_template.format(
        op_tables="\n".join(op_tables),
        on_tables="\n".join(on_tables),
        info=info,
        code=formula,
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)


def get_analysis(dirpath, analysis_name, info, formula):
    inputs = {}
    for report_name in os.listdir(dirpath):
        full_path = dirpath + "/" + report_name
        data = open(full_path, "r").read()
        if inputs:
            inputs = analyze_similarity_stats(parse_similarity_data(data), inputs)
        else:
            inputs = analyze_similarity_stats(parse_similarity_data(data))

    generate_html(inputs, analysis_name + ".html", info, formula)


path = "./FORANALYZES"
inputs_info = "Euclidian * cosine."
formula = """cosine_between_tensors(emb1, emb2) * euclidean_similarity(emb1, emb2)"""
get_analysis(path, "report1", inputs_info, formula)
