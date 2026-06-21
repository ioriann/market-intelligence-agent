from dotenv import load_dotenv

from jquantsapi import ClientV2


load_dotenv()

client = ClientV2()


from_date = "20260315"
to_date = "20260329"


df = client.get_eq_bars_daily(
    code="7203",
    from_yyyymmdd=from_date,
    to_yyyymmdd=to_date,
)

latest_10 = df.tail(10)

print("=== トヨタ自動車（7203）の株価 ===")

for _, row in latest_10.iterrows():
    print(f"""
日付: {row["Date"].date()}
始値: {row["O"]} 円
高値: {row["H"]} 円
安値: {row["L"]} 円
終値: {row["C"]} 円
------------------------
""")