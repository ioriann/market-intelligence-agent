def create_stock_report(company_info, stock_data):

    latest_date = stock_data["Date"].max()

    report = f"# {company_info['name']} ({company_info['code']})\n\n"

    report += f"作成日: {latest_date.date()}\n\n"

    report += f"- 銘柄コード: {company_info['code']}\n"
    report += f"- 銘柄名: {company_info['name']}\n"
    report += f"- 市場: {company_info['market']}\n"
    report += f"- 業種: {company_info['sector']}\n\n"

    report += "## 株価データ\n\n"

    report += "| 日付 | 始値 | 高値 | 安値 | 終値 |\n"
    report += "| --- | --- | --- | --- | --- |\n"

    for _, row in stock_data.iterrows():
        report += (
            f"| {row['Date'].date()} "
            f"| {row['O']} "
            f"| {row['H']} "
            f"| {row['L']} "
            f"| {row['C']} |\n"
        )

    return report

def save_stock_report(report, code, stock_data):

    latest_date = stock_data["Date"].max()
    date = latest_date.strftime("%Y%m%d")

    filename = f"reports/{code}_{date}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"株価レポートを保存しました: {filename}")