from dotenv import load_dotenv
from jquantsapi import ClientV2

from fetch_stock import fetch_stock_data, fetch_company_info, display_result
from report import create_stock_report, save_stock_report
from news import fetch_stock_news
from ai_analysis import analyze_market_data

load_dotenv()


def main():

    client = ClientV2()
    stock_code = [code.strip() for code in input().split(',')]

    for code in stock_code:
        stock_data = fetch_stock_data(client, code)
        company_info = fetch_company_info(client, code)
        news = fetch_stock_news(company_info["name"])
        display_result(stock_data, company_info)
        report = create_stock_report(company_info, stock_data, news)
        save_stock_report(report, code, stock_data)
        analysis_result = analyze_market_data(report)
        if analysis_result is None:
            print("AI分析中にエラーが発生しました。")
        else:
            print("=== AI分析結果 ===")
            print(analysis_result)

if __name__ == "__main__":
    main()
