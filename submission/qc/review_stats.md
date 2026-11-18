# Số đo review (det)

- Ảnh tính: 24 (batch,gold); box máy: 501; đối tượng sau duyệt: 533; ngưỡng accepted: IoU >= 0.9
- Đã **loại 19 đối tượng nằm quanh các bẫy** khỏi bảng này: lỗi nhân tạo không phản ánh chất lượng máy.

## 1. Bốn trạng thái (AI error profile)
| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted (giữ nguyên) | 465 | 465/501 = 92.8% | 501 box máy |
| edited (sửa) | 5 | 5/501 = 1.0% | 501 box máy |
| deleted (xoá) | 29 | 29/501 = 5.8% | 501 box máy |
| added (vẽ thêm) | 63 | 63/533 = 11.8% | 533 đối tượng sau duyệt |

Trong số deleted + added, **2 trường hợp là đổi lớp** (máy gán sai lớp, box đúng chỗ): đó không phải máy bỏ sót. Số vật máy **sót thật** ≈ added − đổi lớp = 61.

### Theo lớp
| Lớp | accepted | edited | deleted | added |
|---|---|---|---|---|
| person | 255 | 3 | 11 | 19 |
| bicycle | 5 | 0 | 4 | 3 |
| motorbike | 134 | 0 | 7 | 13 |
| car | 51 | 1 | 3 | 22 |
| bus | 4 | 0 | 0 | 0 |
| truck | 7 | 0 | 1 | 0 |
| three_wheeler | 9 | 1 | 3 | 6 |

## 2. So với gold (nhãn gán tay từ đầu)
Ảnh gold: 4; đối tượng gold: 69 (mẫu số của recall)
| | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Máy (pre-label) | 40 | 29 | 29 | 58.0% (KTC 95%: 46–69%) | 58.0% (KTC 95%: 46–69%) |

*Lạc quan: ngưỡng được chọn trên chính các ảnh gold này (in-sample), và chỉ có 4 ảnh. Đọc khoảng tin cậy, đừng đọc con số đơn.*


(Ảnh gold không nằm trong nhãn sau duyệt: không tính residual / new error. Đó là chủ ý: duyệt lại ảnh bạn vừa tự gán tay sẽ đo trí nhớ, không đo thiên kiến.)

## 3. Ảnh bẫy
- Bắt được 8/12 = 66.7% (KTC 95%: 39–86%) (ngưỡng đạt: 80%). Chỉ 12 bẫy nên khoảng tin cậy rất rộng: đọc cùng danh sách bẫy lọt, đừng kết luận chỉ từ %.
  - wrong_class: 1/3
  - loose: 2/3
  - missing: 2/3
  - extra: 3/3
  - lọt: img_027.jpg (wrong_class), img_013.jpg (wrong_class), img_005.jpg (loose), img_008.jpg (missing)

## Gợi ý đọc số
- `deleted` cao → ngưỡng thấp hoặc ánh xạ nhãn sai; `added` cao → máy bỏ sót (xem lớp nào);
- `accepted` thấp (< 50%) → sửa mỗi box lâu hơn vẽ mới: đổi model/ngưỡng hoặc vẽ tay;
- bắt bẫy < 80% → duyệt lại lô, siết checklist (quét ảnh TRƯỚC khi nhìn nhãn máy).
