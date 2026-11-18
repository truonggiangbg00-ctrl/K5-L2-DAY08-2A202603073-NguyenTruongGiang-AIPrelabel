# Thông tin học viên
- Họ và tên: Nguyễn Trường Giang
- MSHV: 2A202603073
- Lớp: chưa xác nhận
- GitHub: GlennQuagmiree
- Repo hiện tại: https://github.com/GlennQuagmiree/K5-L23-Day08-AI-Assisted-Labeling
- Tên repo theo đề: K5-L23-DAY08-2A202603073-NguyenTruongGiang-AIPrelabel (chưa đổi remote)
- Commit chốt bài: chưa chốt
- Máy: Windows + Ubuntu WSL, inference CPU
- CVAT Docker: 2.74.1

## Kết quả tóm tắt
- Bản review học viên: 24 ảnh, 550 đối tượng gồm 8 ignore_region.
- Accepted 465/501=92.8%; edited 5/501=1.0%; deleted 29/501=5.8%; added 63/533=11.8%. Hai box máy trong ignore không tính deleted.
- Gold máy: precision 40/69=58.0%; recall 40/69=58.0% trên 4 ảnh.
- Bắt bẫy: 8/12=66.7%, chưa đạt 80%.
- Thời gian theo học viên cung cấp: gold 30 phút/4 ảnh = 7.5 phút/ảnh; review 10 phút/24 ảnh = 0.417 phút/ảnh. Tỉ số mô tả 18 lần; chưa tính chi phí tạo nhãn máy, QC và sửa lỗi, hai tập ảnh khác nhau và chất lượng chưa tương đương.
- QC: 3/8=37.5% ảnh lỗi; 3/211=1.4% đối tượng lỗi. Cận trên Wilson 95% cho ảnh lỗi: 69%.
- **HOLD — cần REWORK:** còn một ca guideline chưa chốt, tỉ lệ ảnh lỗi và bắt bẫy chưa đạt.
- Phần khai báo sử dụng công cụ và nhận xét cá nhân: học viên tự viết trước nộp.
