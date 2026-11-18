# Bằng chứng quan sát model

Ảnh sao chép từ đầu ra các lượt chạy đã có, không phải ảnh dựng. r03_img002: YOLOE; r08_img002 và r08_img011: YOLO26 conf 0.25; r04_img011: YOLO26 conf 0.5; r05_img013: YOLO26 + MobileSAM.

Nhận xét bổ sung sau khi xem lại ảnh; không đổi số box, thời gian hoặc thông số inference. work/runs.csv và run.json đã đồng bộ các cột nhận xét. Không đưa work hoặc trọng số vào bộ bài.

Kiểm chứng ngưỡng theo lớp ngày 2026-11-18: bảy lớp đều 0.3, IoU 0.6, split batch,gold. Images và annotations giống kết quả merge gốc; 582 box. Bẫy và nhãn export giữ nguyên.
