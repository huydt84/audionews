# Hệ thống đọc tin tức giọng ba miền

## Kiến trúc tổng quan

![image](https://github.com/huydt84/audionews/assets/77562200/3cfa0ce7-3d57-4312-a0de-1a3940dd9e31)


## Yêu cầu hệ thống:
Đã cài đặt Docker

## Cài đặt và chạy hệ thống:
- Nếu trong thư mục **tts_service/app** đã có thư mục **models** thì chuyển sang bước tiếp theo. Nếu không có thì cần tải thư mục folder ở [đường dẫn này](https://husteduvn-my.sharepoint.com/:f:/g/personal/huy_dt200269_sis_hust_edu_vn/EgEG95hprytPj7olSvDXdP4BYxyah7rxPkN4CxiDojfGeg?e=WDVozk)

- Vào thư mục của dự án (**/audionews**), chạy: ```docker-compose up --build```

- Mở trình duyệt, vào http://localhost:3500/ để sử dụng hệ thống
