def create_stock_report(company_info, stock_data, news=None):

    sorted_data = stock_data.sort_values("Date")

    earliest_date = sorted_data["Date"].min()
    latest_date = sorted_data["Date"].max()

    first_close = sorted_data.iloc[0]["C"]
    last_close = sorted_data.iloc[-1]["C"]
    change_rate = (last_close - first_close) / first_close * 100

    highest = sorted_data["H"].max()
    lowest = sorted_data["L"].min()

    report = f"# {company_info['name']} ({company_info['code']})\n\n"

    report += f"作成日: {latest_date.date()}\n\n"

    report += f"- 銘柄コード: {company_info['code']}\n"
    report += f"- 銘柄名: {company_info['name']}\n"
    report += f"- 市場: {company_info['market']}\n"
    report += f"- 業種: {company_info['sector']}\n\n"

    report += "## 期間サマリー\n\n"
    report += f"- 期間: {earliest_date.date()} 〜 {latest_date.date()}\n"
    report += f"- 期間最高値: {highest:,}円\n"
    report += f"- 期間最安値: {lowest:,}円\n"
    report += f"- 騰落率: {change_rate:+.2f}%\n\n"

    if news:
        report += "## 関連ニュース\n\n"
        for item in news:
            report += f"- [{item['title']}]({item['link']}) （{item['published']}）\n"
        report += "\n"

    report += "## 株価データ\n\n"

    report += "| 日付 | 始値 | 高値 | 安値 | 終値 |\n"
    report += "| --- | --- | --- | --- | --- |\n"

    for _, row in sorted_data.iterrows():
        report += (
            f"| {row['Date'].date()} "
            f"| {row['O']:,}円 "
            f"| {row['H']:,}円 "
            f"| {row['L']:,}円 "
            f"| {row['C']:,}円 |\n"
        )

    return report

def save_stock_report(report, code, stock_data):

    latest_date = stock_data["Date"].max()
    date = latest_date.strftime("%Y%m%d")

    filename = f"reports/{code}_{date}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"株価レポートを保存しました: {filename}")