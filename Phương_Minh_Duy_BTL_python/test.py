import asyncio
from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime, timedelta, timezone

app = FastAPI()

API_KEY = '1af198eb76-8362cbab0b-sdx021'  # Thay bằng key API của bạn
BASE_URL = 'https://api.fastforex.io/'  # URL cơ bản của API fastFOREX

# Định nghĩa múi giờ UTC và múi giờ Việt Nam
UTC_timezone = timezone.utc
VN_timezone = timezone(timedelta(hours=7))  # UTC+7

async def fetch_forex_data():
    while True:
        from_currency = 'GBP'  # Tiền tệ mặc định là JPY

        url = f"{BASE_URL}fetch-one?from={from_currency}&to=GBP&api_key={API_KEY}"  # Chỉnh sửa đây
        response = requests.get(url)

        if response.status_code == 200:
            forex_data = response.json()
            # Chuyển đổi thời gian từ múi giờ UTC sang múi giờ Việt Nam
            updated_time_utc = datetime.strptime(forex_data['updated'], "%Y-%m-%d %H:%M:%S")
            updated_time_vn = updated_time_utc.replace(tzinfo=UTC_timezone).astimezone(VN_timezone)
            forex_data['updated'] = updated_time_vn.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            print(forex_data)  # In ra dữ liệu JSON cập nhật
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized. Check your API key.")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Currency pair not found.")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        await asyncio.sleep(30)  # Chờ 30 giây trước khi gửi yêu cầu kế tiếp

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch_forex_data())  # Bắt đầu lặp vô hạn để cập nhật dữ liệu

@app.get("/forex/{to_currency}")
def get_forex_rate(to_currency: str):
    from_currency = 'GBP'  # Tiền tệ mặc định là JPY

    # Kiểm tra định dạng mã tiền tệ
    if len(to_currency) != 3 or not to_currency.isalpha():
        raise HTTPException(status_code=400, detail="Invalid currency code format. Use a 3-letter currency code.")

    url = f"{BASE_URL}fetch-one?from={from_currency}&to={to_currency}&api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        forex_data = response.json()
        # Chuyển đổi thời gian từ múi giờ UTC sang múi giờ Việt Nam
        updated_time_utc = datetime.strptime(forex_data['updated'], "%Y-%m-%d %H:%M:%S")
        updated_time_vn = updated_time_utc.replace(tzinfo=UTC_timezone).astimezone(VN_timezone)
        forex_data['updated'] = updated_time_vn.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        return forex_data  # Trả về dữ liệu JSON trực tiếp
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized. Check your API key.")
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Currency pair not found.")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
