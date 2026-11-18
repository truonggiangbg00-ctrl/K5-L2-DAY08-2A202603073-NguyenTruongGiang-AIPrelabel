# Báo cáo Day 08 — 2A202603073 - Nguyễn Trường Giang

Ngày cập nhật: 2026-11-18. Nguồn nhãn: `labels/batch_reviewed_NguyenTruongGiang.json`, được sao chép nguyên byte sang `batch_reviewed.json`. Tổng 24 ảnh, 550 đối tượng gồm 8 ignore_region. Bản export gốc được giữ nguyên; không âm thầm sửa nhãn sau khi đo.

## 1. Model và recipe (Part 2–3)

| Lớp | Model | Ngưỡng | Căn cứ |
|---|---|---|---|
| person, bicycle, motorbike, car, bus, truck | YOLO26m CPU | 0.3 | r06 và qc/threshold_sweep.md |
| three_wheeler | YOLOE-26s CPU; prompt tuk tuk three wheeler | 0.3 | r07 và qc/threshold_sweep.md |

Lệnh đã dùng:
```bash
python scripts/merge_prelabels.py work/prelabel/yoloe_all/pre.coco.json work/prelabel/y26_all/pre.coco.json --conf 0.3 --iou 0.6 --split "batch,gold" --out work/prelabel/merged_review/pre.coco.json
```

Trước khi thêm bẫy: 582 box/28 ảnh (24 batch + 4 gold): person 311, motorbike 154, car 69, three_wheeler 16, bicycle 14, truck 12, bus 6. File import chỉ chứa 24 ảnh batch. Không tái sinh bẫy trong lúc review.

Chọn MobileSAM cho các thử nghiệm mask trên CPU. r05 sinh 16 mask/2 ảnh, 4.41 giây/ảnh theo log; đây là thời gian pipeline, không phải thời gian người duyệt. YOLO26 triển khai CVAT dùng bản n, trong khi recipe offline dùng bản m; không đánh đồng hai kết quả.

Không có ngưỡng đã thử ≤0.5 đạt recall 90%: tối đa person 23/28, bicycle 1/6, motorbike 14/19, car 7/8, three_wheeler 3/7. Bus có 1 vật, truck có 0 vật nên không đủ mẫu chọn ngưỡng theo lớp. Ngưỡng 0.3 là mặc định, không phải ngưỡng đã chứng minh đạt mục tiêu. Chọn và đo trên cùng 4 ảnh gold có nguy cơ lạc quan.

Sai lớp và box không ôm sát không được sửa chỉ bằng đổi ngưỡng. Cần kiểm tra hình ảnh và sửa nhãn. Ví dụ có bằng chứng: `img_013` ở r05, tuk-tuk mang lớp `car` điểm 0.42; thêm SAM vẫn giữ lớp sai. `img_002` ở r03 có `three_wheeler` điểm 0.93 cho tuk-tuk xanh, trong khi r08 chưa có box xe riêng. Chưa xác minh được ví dụ điểm thấp nhưng đúng bằng gold pilot nên không tự gán nhãn “đúng” cho mọi box thấp.

### Đối chiếu đầu ra từng model

| So sánh | Bằng chứng | Quyết định từ quan sát |
|---|---|---|
| r03 YOLOE và r08 YOLO26 trên img_002 | [YOLOE](evidence/r03_img002.jpg), [YOLO26](evidence/r08_img002.jpg) | YOLOE bổ sung lớp three_wheeler; YOLO26 vẫn cần cho người và xe máy |
| r08 conf 0.25 và r04 conf 0.5 trên img_011 | [0.25](evidence/r08_img011.jpg), [0.5](evidence/r04_img011.jpg) | Trên 8 pilot, 215 → 139 box, giảm 35.3%; chỉ số này không phân biệt loại đúng hay loại nhầm |
| r05 YOLO26 + MobileSAM trên img_013 | [Box và mask](evidence/r05_img013.jpg) | SAM giải quyết hình dạng; lỗi lớp phải sửa ở detector/mapping hoặc review |

Không có thử nghiệm A/B prompt YOLOE: prompt hiện là cấu hình đã chạy, chưa có bằng chứng là tốt nhất. Giữ metadata thời gian và số box của từng run; các nhận xét được bổ sung sau khi quan sát lại ảnh đầu ra.

### Cách áp dụng ngưỡng theo lớp

Sweep không tìm được ngưỡng đạt recall mục tiêu cho lớp có đủ mẫu; bus/truck không đủ mẫu. Vì thế bảng recipe chọn 0.3 cho từng lớp thay vì tối ưu thêm trên 4 ảnh. Chuỗi tương đương để tái lập là `--thr "person=0.3,bicycle=0.3,motorbike=0.3,car=0.3,bus=0.3,truck=0.3,three_wheeler=0.3"` đã được chạy kiểm chứng ngày 2026-11-18 với cùng nguồn, IoU 0.6 và split batch,gold; đầu ra 582 box có images/annotations giống recipe ban đầu dùng `--conf 0.3`. Kết quả kiểm chứng lưu tại `work/prelabel/threshold_explicit_check/pre.coco.json`, không tái sinh bẫy hoặc thay baseline review. Không tăng recall bằng cách giảm chuẩn gold hoặc thay taxonomy.

## 2. AI error profile

Nguồn: `qc/review_stats.json` và `.md`, so baseline có bẫy với bản export đã review. Thống kê loại vùng quanh bẫy để không đánh giá model bằng lỗi nhân tạo.

| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted | 465 | 92.8% | 501 box máy sau lọc vùng bẫy |
| edited | 5 | 1.0% | 501 box máy |
| deleted | 29 | 5.8% | 501 box máy |
| added | 63 | 11.8% | 533 đối tượng sau lọc vùng bẫy/ignore |

Tổng ba trạng thái phía máy là 499, thấp hơn 501 vì 2 box nằm trong ignore_region không tính deleted theo script. Không tự chuẩn hóa lại phần trăm. Có 2 trường hợp đổi lớp; số added trừ đổi lớp là 61, chỉ là ước lượng bỏ sót theo phép ghép box.

Máy trên gold: TP=40, FP=29, FN=29; precision=40/69=58.0%, recall=40/69=58.0%. Mẫu số recall là 69 vật không phải ignore trong 4 ảnh gold; KTC 95% khoảng 46–69%. Bicycle yếu trên gold (recall tốt nhất trong sweep chỉ 1/6), nhưng 6 vật không đủ đại diện mọi bối cảnh. Có 63 đối tượng được thêm trong thống kê review, nên không thể coi accepted cao là bằng chứng không bỏ sót.

## 3. Thiên kiến tự động hóa và ảnh bẫy

Bắt được **8/12=66.7%**, dưới ngưỡng 80% (cần ít nhất 10/12). Theo loại: wrong_class 1/3, loose 2/3, missing 2/3, extra 3/3. Bẫy còn lọt: img_027 và img_013 (wrong_class), img_005 (loose), img_008 (missing). Đây là kết quả từ bản export trước sửa QC; không chỉnh nhãn theo đáp án rồi báo lại như kết quả review mù.

Accepted 465/501=92.8% đi kèm bắt bẫy 8/12 là tín hiệu cần siết review. Có thể giữ lại nhiều box vì hình thức hợp lý mà chưa kiểm lớp, biên và vùng không có box. Không khẳng định trạng thái tâm lý của người duyệt chỉ từ hai tỉ lệ này. KTC bẫy 95% khoảng 39–86%, mẫu rất nhỏ.


### Phân tích từng bẫy lọt sau khi chốt export

| Ảnh / loại | Vùng cần kiểm (xywh ảnh gốc) | Vì sao dễ lọt — giả thuyết từ ảnh | Bước checklist cần bổ sung |
|---|---|---|---|
| img_027 / wrong_class | (803,355,12,33), person bị đổi bicycle | Vật nhỏ phía xa, hình mảnh dễ bị bỏ qua khi chỉ nhìn xe lớn | Phóng to vùng nền, xác định người hay xe bằng hình dáng; không nhận lớp chỉ từ màu box |
| img_013 / wrong_class | (930,86,63,82), key thiết kế truck → car | Vùng xe nền ít nổi bật so với tuk-tuk lớn | Kiểm từng xe nền theo taxonomy. Đáp án bẫy là nhãn gốc của máy, cần kiểm thực tế trước khi dùng làm nhãn chuẩn |
| img_005 / loose | (475,251,76,156) | Cảnh đông, nhiều người chồng box; cạnh trên lấy dư vùng quanh đầu | Ẩn các box khác rồi so bốn cạnh với đúng cá thể, không suy ra biên đúng từ conf |
| img_008 / missing | (36,234,16,29), person bị bỏ | Người rất nhỏ ở mép trái nền, không có box để thu hút chú ý | Quét lưới 3×3 khi ẩn nhãn; kiểm mép ảnh trước khi chốt |

Đây là giả thuyết về cơ chế bỏ sót, không phải lời xác nhận học viên đã bỏ một bước cụ thể. Chưa có nhật ký thao tác để chứng minh nguyên nhân tâm lý. Kết quả bẫy đã được hiển thị trong chat trước lượt review lại của học viên; do đó lượt hiện tại không hoàn toàn mù. Giữ 8/12 như số đo mô tả của export, không dùng làm thí nghiệm độc lập về thiên kiến hay đổi thành 12/12 sau khi xem đáp án.

Kiểm việc làm ở vòng sau: lưu một bản export trước khi xem key; ghi checklist đủ 24/24 ảnh, số ca chưa chắc còn treo và thời gian từng phiên. Ba nhóm lỗi khác nhau cần ba lượt kiểm: lớp → biên → vùng không có nhãn.

## 4. Máy có đáng dùng không?

Học viên báo thời gian lượt review 24 ảnh là **10 phút**, tương đương **10/24=0.417 phút/ảnh**, khoảng **25 giây/ảnh**. Không bao gồm xử lý kỹ thuật và QC sau đó. Học viên bổ sung thời gian gán tay 4 ảnh gold là **30 phút**, tương đương **7.5 phút/ảnh**. Tỉ số thời gian theo ảnh là **7.5 / (10/24) = 18 lần**, tức thời gian review/ảnh thấp hơn khoảng **94.4%** trong hai lượt đã báo. Đây chỉ là so sánh mô tả: hai tập ảnh khác nhau, người duyệt đã quen cảnh sau gold, chưa cộng thời gian tạo pre-label, QC và sửa lỗi. Chất lượng hiện chưa đạt nên chưa thể xem đây là mức tăng năng suất ở chất lượng tương đương.

Recipe có thể hỗ trợ tạo điểm bắt đầu, nhưng chất lượng lượt hiện tại chưa đủ Release: recall gold 40/69 và bắt bẫy 8/12. Lượt 25 giây/ảnh cần được xem cùng cảnh đông và ca chưa rõ; không dùng tốc độ nhanh làm tiêu chí hoàn thành.

Ba quy tắc cho vòng tiếp theo:
1. Mỗi ảnh: ẩn nhãn, quét toàn cảnh trước rồi mới hiện box; checklist đủ 24/24.
2. Mỗi box: kiểm cá thể, lớp và bốn cạnh; không tự chấp nhận theo conf. Ghi ca chưa chắc vào calibration.
3. Quét lại vùng trống, vật nhỏ và che khuất trước Save; chỉ đọc đáp án bẫy sau khi chốt export của vòng đo.

## 5. Mask SAM cho 3 vật

Đã giữ 3 thử nghiệm MobileSAM và chạy thêm SAM 2.1-b trên cùng 3 vật. Tất cả là ảnh đầu ra thực; số click dưới đây dành cho SAM 2.1-b, kèm một box prompt mỗi vật.

| Ảnh | Điểm dương/âm | Diện tích mask | Quan sát | File |
|---|---|---|---|---|
| img_009 | 3/1 | 40,104 px; 5.7% ảnh | Lấy thêm tay lái, giỏ, động cơ so với MobileSAM chỉ lấy bánh; còn lẫn một phần hàng/giá đỡ | masks/motorbike_img009_sam21.jpg |
| img_013 | 3/2 | 305,411 px; 43.7% ảnh | Bao phủ thân/mái/bánh, nhưng lẫn người lái và xe máy phía sau; không chọn làm mask cuối | masks/tuktuk_img013_sam21.jpg |
| img_031 | 3/2 | 108,040 px; 15.5% ảnh | Lấy khung/giỏ/bánh rộng hơn, còn lấp nền trong bánh và dính một phần hàng | masks/bicycle_img031_sam21.jpg |

Không khẳng định SAM 2.1 tốt hơn trên mọi vật: img_013 tăng vùng mask nhưng tăng cả phần không thuộc xe. Guideline 4.2 yêu cầu loại lỗ lớn hơn khoảng 5%, không lấy bóng đổ hoặc vật khác; các mask hiện chưa bảo đảm yêu cầu đó. Cần prompt bổ sung hoặc chỉnh tay trước dùng làm nhãn huấn luyện. MobileSAM vẫn hữu ích cho CPU và thử tương tác nhanh. Cấu hình prompt được lưu ở masks/mask_runs.json; không suy diễn thời gian người gán từ thời gian inference.

## 6. Calibration

Có 5 quyết định CAL-01–05 trong `qc/calibration_decisions.csv`, đồng bộ với `guidelines/guideline_v1.1_calibrated.md`.
- CAL-01: lỗi áp dụng taxonomy xích lô/người, không đổi taxonomy gốc.
- CAL-02: phân biệt giỏ/giá đỡ cố định với hàng rời nhô xa (img_009, img_031).
- CAL-03: box trùng theo cùng cá thể, không gộp người khác nhau chỉ vì box chồng nhau (img_029, img_035).
- CAL-04: mũ trưng bày không phải người (img_031).
- CAL-05: không dùng ngưỡng conf làm điều kiện tự chấp nhận (img_005, img_029).

Còn một ca chưa chốt về xe hàng img_008: cần xác nhận cấu trúc hai/ba bánh để phân biệt xe đẩy với three_wheeler. Không ép một nhãn để đạt số liệu. Các câu hỏi khác không có đủ ví dụ được ghi rõ trong guideline.

### Đối chiếu calibration với bản nhãn hiện tại

CAL-01 và CAL-04 có thay đổi đã thể hiện ở bản review (xích lô/người, bỏ mũ giả). CAL-02 và CAL-03 chưa được áp dụng nhất quán: mask còn lẫn hàng/nền và QC vẫn thấy box trùng. CAL-05 là quy tắc của vòng sửa tiếp theo, không bằng chứng toàn bộ box hiện tại đã được kiểm đủ. Vì vậy guideline v1.1 là chuẩn để sửa candidate, không tuyên bố candidate đã tuân thủ hoàn toàn. Chính các chênh lệch này dẫn tới HOLD/cần REWORK.

## 7. QC và quyết định

Nguồn: `qc/qc_sample.csv`, `qc/qc_review.csv`, `qc/qc_report_auto.md`. Mẫu seed 42: **8/24 ảnh**, gồm 3 ca khó + 5 ngẫu nhiên, **211 đối tượng**. Người kiểm trong phiếu: Codex; đây không phải một lượt kiểm độc lập do học viên tự thực hiện.

Phát hiện **3/211=1.4% đối tượng lỗi**, thuộc **3/8=37.5% ảnh lỗi**. Ngưỡng Release áp dụng cho ảnh lỗi ≤2%, không lấy tỉ lệ đối tượng 1.4% thay thế. Hai lỗi thừa: img_029 box467 chỉ đầu trùng box người, img_035 box522 trùng person537; một lỗi hình học: img_005 box48 chưa bao đủ phần người áo đỏ nhìn thấy. ID thuộc release candidate hiện tại. `khong` nghĩa là chưa phát hiện lỗi trong lượt kiểm, không chứng minh ảnh không còn lỗi.

Cận trên Wilson 95% của tỉ lệ ảnh lỗi: **69%**. Mẫu nhỏ và người kiểm không độc lập hoàn toàn với quá trình chuẩn bị nhãn nên kết luận chất lượng cần thận trọng. Script kiểm cấu trúc/ghép box/đếm lỗi, không tự biết lớp đúng, box ôm sát hay vật cả người và máy cùng bỏ sót.

**Quyết định: HOLD — cần REWORK**, ngày 2026-11-18. Theo thứ tự quyết định: Hold vì còn ca taxonomy img_008; sau khi chốt vẫn phải Rework vì 3/8 ảnh lỗi và bắt bẫy 8/12. Thư mục release là **release candidate**, chưa phải dữ liệu được phê duyệt dùng huấn luyện.

Kế hoạch: chốt img_008, sửa các lỗi QC, rà lại bốn ảnh lọt bẫy, xem 8 cảnh báo vật dưới 20 px và sửa mask. Giữ số đo vòng này làm baseline; vòng sửa sau phải có export và thống kê riêng, không ghi đè lịch sử đo.

## 8. Ghi chú cá nhân

- Mục “Dùng AI để làm bài”: học viên tự bổ sung theo yêu cầu riêng trước khi nộp.
- Theo xác nhận học viên, 4 ảnh gold đã gán tay trước khi xem AI. Thời gian được học viên bổ sung: 30 phút/4 ảnh; review 10 phút/24 ảnh. Chưa đo toàn bộ chi phí QC và sửa lỗi nên chưa đủ dữ liệu kết luận hiệu quả ở chất lượng tương đương.
- Máy Windows + Ubuntu WSL, CVAT 2.74.1; các lần chạy trong log dùng CPU. YOLOE chạy qua Nuclio local do môi trường Windows gặp chặn DLL. Không dùng cache dự đoán thay các lần chạy trong log.
- Ba function Day08 đã triển khai. Detector có conf/can_review, YOLOE xuất rectangle để tương thích task box; task skeleton không dùng mapping box.
- Nhận xét cá nhân và điều sẽ làm khác lần sau: học viên tự bổ sung. Gợi ý từ số liệu là tăng thời gian kiểm vật nhỏ/che khuất và ghi thời gian ngay từ đầu; đây chưa phải lời tự nhận của học viên.
