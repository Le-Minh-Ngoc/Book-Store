# BOOKSTORE MANAGEMENT SYSTEM

Hệ thống quản lý nhà sách trực tuyến được xây dựng bằng Django theo mô hình Domain Package MVC.

## Công nghệ sử dụng

- Python 3.8+
- Django 4.2.9
- MySQL
- PyMySQL
- HTML, CSS, Bootstrap

## Yêu cầu hệ thống

- Python 3.8 trở lên
- MySQL Server

## Hướng dẫn cài đặt và chạy

### Bước 1: Cài đặt MySQL

Tải và cài đặt MySQL từ: https://dev.mysql.com/downloads/mysql/

Ghi nhớ mật khẩu root của MySQL.

### Bước 2: Tạo virtual environment

```bash
cd bookstore
python -m venv .venv
.venv\Scripts\activate
```

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Tạo database MySQL

Mở MySQL command line hoặc MySQL Workbench và chạy:

```sql
CREATE DATABASE bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Bước 5: Cấu hình database

Mở file `bookstore/settings.py` và cập nhật mật khẩu MySQL:

```python
DATABASES = {
    'default': {
        'PASSWORD': 'your_mysql_password',  # Thay bằng mật khẩu MySQL của bạn
    }
}
```

### Bước 6: Chạy migrations

```bash
python manage.py migrate
```

### Bước 7: Tạo superuser

```bash
python manage.py createsuperuser
```

### Bước 8: Chạy server

```bash
python manage.py runserver
```

Server chạy tại: http://127.0.0.1:8000/

## Truy cập hệ thống

- Trang chủ: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Đăng ký: http://127.0.0.1:8000/customer/register/
- Đăng nhập: http://127.0.0.1:8000/customer/login/

## Chức năng

### Khách hàng

- Đăng ký, đăng nhập
- Xem, tìm kiếm sách
- Thêm vào giỏ hàng
- Đặt hàng, thanh toán
- Xem lịch sử đơn hàng
- Đánh giá sách
- Xem gợi ý sách

### Nhân viên

- Thêm sách vào kho
- Quản lý kho hàng
- Xem phiếu nhập kho

### Admin

- Quản lý toàn bộ hệ thống
