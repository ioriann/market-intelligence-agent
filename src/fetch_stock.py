from dotenv import load_dotenv
from jquantsapi import ClientV2


load_dotenv()


def fetch_stock_data(code):

    client = ClientV2()

    from_date = "20260315"
    to_date = "20260329"

    df = client.get_eq_bars_daily(
        code=code,
        from_yyyymmdd=from_date,
        to_yyyymmdd=to_date,
    )

    return df.tail(10)


def display_stock_data(df, code):

    print(f"=== 株価情報({code}) ===")

    for _, row in df.iterrows():

        print(f"""
日付: {row["Date"].date()}
始値: {row["O"]} 円
高値: {row["H"]} 円
安値: {row["L"]} 円
終値: {row["C"]} 円
------------------------
""")


def main():

    stock_code = [code.strip() for code in input().split(',')]

    for code in stock_code:
        df = fetch_stock_data(code)
        display_stock_data(df, code)


if __name__ == "__main__":
    main()