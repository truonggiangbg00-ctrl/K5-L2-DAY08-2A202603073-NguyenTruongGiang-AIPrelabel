# Bổ sung guideline v1.1 — 2A202603073 - Nguyễn Trường Giang

## 1. Quy tắc bổ sung sau calibration
- CAL-02, img_009 và img_031: giỏ, giá đỡ gắn cố định thuộc xe; hàng rời nhô hơn khoảng 20% chiều dài xe không thuộc box/mask xe. Vẽ phần xe nhìn thấy, không suy đoán phần bị che.
- CAL-03, img_029 và img_035: một người chỉ có một box. Box đầu nằm trong box thân của cùng người là trùng; hai người đứng sát nhau vẫn là hai box. Không gộp theo độ chồng lấp đơn thuần.
- CAL-05, img_005 và img_029: không đặt ngưỡng conf để chấp nhận mà không kiểm. Điểm cao không thay thế kiểm lớp, biên và vật bị bỏ sót.

## 2. Quy tắc v1.0 được làm rõ bằng ví dụ
- CAL-01: xích lô ở img_010, img_017 là three_wheeler, gồm khung và mui; người trên/ngoài xe có box person riêng. Đây là sửa lỗi áp dụng taxonomy, không phải đổi lớp của đề.
- CAL-04: mũ trưng bày trong img_031 không phải person; xóa box giả quanh mũ.
- Vật cao dưới 20 px không gán riêng; chỉ gom ignore_region nếu là cụm ít nhất 5 vật sát nhau khó tách. Không dùng ignore để bỏ qua vật lớn rõ ràng.

## 3. Câu hỏi còn mở và giới hạn
Xe điện chưa có ca đủ rõ để chốt. Xe hàng img_008 còn cần xác nhận cấu trúc hai/ba bánh. Các ca can_review cần đối chiếu khi sửa vòng tiếp theo. Không coi bản này là bằng chứng đã giải quyết mọi trường hợp.

## 4. Lịch sử
v1.0: giữ nguyên bản đề. v1.1 ngày 2026-11-18: thêm quy tắc hàng hóa và phụ kiện, box trùng theo cá thể, không tự chấp nhận theo conf; có 5 dòng CAL-01–05 trong calibration_decisions.csv. Các quyết định hiện phục vụ đánh giá và kế hoạch Rework, không thay bản export của học viên một cách âm thầm.
