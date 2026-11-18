# Trạng thái sau bản export học viên

Đã dùng batch_reviewed_NguyenTruongGiang.json (24 ảnh, 550 đối tượng), tính lại thống kê, tạo release candidate, kiểm 8 ảnh QC, viết 5 quyết định calibration và báo cáo 8 phần. Thời gian theo học viên cung cấp: gold 30 phút/4 ảnh; review 10 phút/24 ảnh.

## Trước khi nộp
1. Điền lớp, mục sử dụng công cụ và nhận xét cá nhân ở STUDENT.md/REPORT.md.
2. Kiểm tra lại các số thời gian đã cung cấp: gold 30 phút/4 ảnh; review 10 phút/24 ảnh. So sánh thời gian chưa bao gồm tạo pre-label, QC và sửa lỗi.
3. Giữ quyết định HOLD/cần REWORK theo dữ liệu. Đề cho phép kết luận Rework trung thực; không đổi thành Release khi chưa có bằng chứng đạt.
4. Nếu sửa tiếp: chốt xe hàng img_008, sửa 3 lỗi trong qc_review.csv, rà 4 ảnh lọt bẫy và 8 cảnh báo box nhỏ; lưu qc_fixed.json hoặc export vòng mới, giữ baseline vòng hiện tại.
5. Chạy validate_labels.py --all và check_submission.py sau mọi thay đổi.
6. Chốt commit, tên repo/public theo SUBMISSION.md, tự nộp link LMS. Chưa push hoặc gửi bài tự động.

## Nguồn chính
labels/batch_reviewed.json giống nguyên byte với export học viên. qc/review_provenance.json ghi SHA256. release/final_det.coco.json là candidate 550 đối tượng, chưa được phê duyệt Release. Không chạy finish_after_review.py để ghi lại thời gian hoặc thay baseline hiện tại.
