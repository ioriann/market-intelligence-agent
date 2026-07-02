def fetch_stock_data(client, code):

    from_date = "20260315"
    to_date = "20260329"

    df = client.get_eq_bars_daily(
        code=code,
        from_yyyymmdd=from_date,
        to_yyyymmdd=to_date,
    )

    return df.tail(10)


def fetch_company_info(client, code):

    company_info = client.get_eq_master(code=code)
    # client.get_eq_master の返り値は環境によって
    # - pandas.DataFrame (行/列) だったり
    # - dict / pandas.Series だったりします。
    # 固定のカラム名に依存すると KeyError になるため、
    # いくつかの可能性を試して安全に取得します。

    def _val(obj, *keys):
        # dict-like
        if isinstance(obj, dict):
            for k in keys:
                if k in obj and obj[k] is not None:
                    return obj[k]
            return None

        # pandas DataFrame/Series-like
        if hasattr(obj, "columns"):
            # DataFrame: 先頭行を使う
            try:
                row = obj.iloc[0]
            except Exception:
                row = None
            if row is not None:
                for k in keys:
                    # 列名そのまま
                    if k in obj.columns:
                        return obj[k].iloc[0]
                # 小文字比較で類推
                lowered = {c.lower(): c for c in obj.columns}
                for k in keys:
                    if k.lower() in lowered:
                        col = lowered[k.lower()]
                        return obj[col].iloc[0]
            return None

        # Series-like
        if hasattr(obj, "get"):
            for k in keys:
                try:
                    v = obj.get(k)
                    if v is not None:
                        return v
                except Exception:
                    pass

        # 最終フォールバック
        return None

    name = _val(company_info, "CoName", "CompanyName", "companyName", "company_name", "Name", "name")
    market = _val(company_info, "MktNm", "MarketCodeName", "marketCodeName", "market", "Market")
    sector = _val(company_info, "S33Nm", "Sector33CodeName", "sector33CodeName", "sector", "Sector")

    return {
        "code": code,
        "name": name or "(不明)",
        "market": market or "(不明)",
        "sector": sector or "(不明)"
    }

def display_result(stock_data, company_info):
    print(f"=== 株価情報({company_info['code']}) ===")
    print(f"銘柄コード: {company_info['code']}")
    print(f"銘柄名: {company_info['name']}")
    print(f"市場: {company_info['market']}")
    print(f"業種: {company_info['sector']}")

    for _, row in stock_data.iterrows():

        print(f"""
日付: {row["Date"].date()}
始値: {row["O"]} 円
高値: {row["H"]} 円
安値: {row["L"]} 円
終値: {row["C"]} 円
------------------------
""")