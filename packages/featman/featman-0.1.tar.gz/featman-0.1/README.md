# Featman
Features and sh*t. Use as an abstraction to `Spaceman`. It can be used with the storage layers spaceman provides.

```python
from featman import Features

features = (
    Features(host="localhost", db="global")
        .set_storage("...")
        .set_type("...")
        .set_time(now=False, back=True, month=0, day=0, hour=0, minute=30)
        .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
        .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
        .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
        .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
        .push()
)
```