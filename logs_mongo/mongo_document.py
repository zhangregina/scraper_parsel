from datetime import datetime


class VinCodeModel:
    auto_collection = {
        "_id": "",
        "vin_code": "",
        "url": "",
        "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    }
