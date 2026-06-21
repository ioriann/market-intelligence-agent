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

print(df.tail(10))