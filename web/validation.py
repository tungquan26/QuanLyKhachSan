SERVICE_STATUSES = ("Đang cung cấp", "Ngừng cung cấp")


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
