SERVICE_STATUSES = ("Đang cung cấp", "Ngừng cung cấp")

def report_dates(values):
    import re
    from datetime import date

    parsed = []
    for key, label in (("tu_ngay", "Từ ngày"), ("den_ngay", "Đến ngày")):
        value = values[key]
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            raise ValueError(f"{label} phải là ngày hợp lệ theo định dạng năm-tháng-ngày.")
        try:
            parsed.append(date.fromisoformat(value))
        except ValueError:
            raise ValueError(f"{label} không hợp lệ.") from None
    if parsed[0] > parsed[1]:
        raise ValueError("Từ ngày không được lớn hơn Đến ngày.")
    return parsed

def identity(value):
    if len(value) != 12 or not value.isascii() or not value.isdigit():
        raise ValueError("CCCD cần đúng 12 chữ số.")
    return value

def guest(values):
    if not values["name"] or len(values["name"]) > 100:
        raise ValueError("Nhập họ tên từ 1 đến 100 ký tự.")
    identity(values["cccd"])
    if len(values["phone"]) > 20:
        raise ValueError("Số điện thoại dài tối đa 20 ký tự.")

def service(values):
    if not values["name"] or len(values["name"]) > 100:
        raise ValueError("Nhập tên dịch vụ từ 1 đến 100 ký tự.")
    if not values["unit"] or len(values["unit"]) > 30:
        raise ValueError("Nhập đơn vị tính từ 1 đến 30 ký tự.")
    price = values["price"]
    if not price or not price.isascii() or not price.isdigit() or len(price) > 14:
        raise ValueError("Đơn giá phải là số nguyên từ 0 đến 99999999999999 đồng, không dùng dấu phân cách.")
    if values["status"] not in SERVICE_STATUSES:
        raise ValueError("Hãy chọn trạng thái Đang cung cấp hoặc Ngừng cung cấp.")
    return int(price)
