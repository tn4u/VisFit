## TUẦN 1: 24/08/2026 – 30/08/2026

### 1. Mục tiêu trọng tâm của tuần
- Khởi động dự án, thiết lập môi trường Git/Colab chung cho nhóm.
- Thu thập và kiểm tra tính toàn vẹn của 3 bộ dữ liệu: DeepFashion-MultiModal, FashionIQ, Polyvore Outfits.
- Viết pipeline tiền xử lý ảnh cơ bản (crop theo parsing mask).

### 2. Tiến độ thực hiện chi tiết

#### 👤 Sinh viên 1: Tuấn (SV1) - Phụ trách Data & Analytics
- **Công việc đã thực hiện**:
  - Đã tải thành công 3 bộ dữ liệu lớn về thư mục lưu trữ đám mây [2].
  - Viết script kiểm tra tính toàn vẹn: Đối chiếu số lượng ảnh thực tế với metadata để phát hiện tệp lỗi [2].
  - Chạy thống kê mô tả dữ liệu (số sản phẩm theo danh mục, độ dài mô tả text) [2].
  - Kiểm tra điều khoản giấy phép (License) của DeepFashion-MultiModal để đảm bảo hợp lệ nghiên cứu phi thương mại [2].
- **Kết quả đạt được (Deliverables)**:
  - Báo cáo thống kê mô tả dữ liệu (data profiling) hoàn chỉnh.

#### 👤 Sinh viên 2: Khanh (SV2) - Phụ trách Preprocessing & Vision Pipeline
- **Công việc đã thực hiện**:
  - Khởi tạo Git Repository chung, cấu trúc các thư mục dự án và viết tài liệu hướng dẫn nhóm.
  - Thiết lập môi trường PyTorch hỗ trợ GPU CUDA, file `requirements.txt` chứa thư viện lõi.
  - Viết và kiểm thử thành công lớp `VisFitImagePreprocessor` để crop trang phục theo parsing mask và resize ảnh về 224x224.
- **Kết quả đạt được (Deliverables)**:
  - Repository VisFit có cấu trúc chuẩn, môi trường hoạt động tốt trên GPU Colab.


### 3. Kế hoạch cho tuần tiếp theo (31/08 – 06/09)
- **Tuấn (SV1)**: Làm sạch nhãn text từ DeepFashion-MultiModal và FashionIQ; Ánh xạ ảnh về ID gốc để thiết lập ground truth query/gallery.
- **Khanh (SV2)**: Chạy batch xử lý crop và resize ảnh trên toàn bộ 3 bộ dữ liệu lớn; 

## TUẦN 2: 31/08/2026 – 06/09/2026

#### 👤 Sinh viên 2: Khanh (SV2) - Phụ trách Preprocessing & Vision Pipeline
### 1. Mục tiêu trọng tâm của tuần
- Image preprocessing cho Branch A trên dataset DeepFashion-MultiModal.
- Xây dựng clothing crop dựa trên human parsing mask.
- Bắt đầu feature extraction bằng Fashion-CLIP.

### 2. Dataset Inspection

| Hạng mục | Kết quả |
|---|---|
| Dataset | DeepFashion-MultiModal |
| Total images | 44,097 |
| Images with parsing | 12,701 |
| Image format | JPEG |
| Parsing format | PNG |
| Image size | (750, 1101) |
| Parsing size | (750, 1101) |
| Parsing representation | Grayscale / Class-ID |
| Sample unique values | [0, 1, 5, 11, 13, 14, 15] |
| Image ↔ Parsing matching | 100% |

12,701 ảnh có human parsing tương ứng được sử dụng làm subset chính cho các experiment tiếp theo trong tuần.

### 3. Human Parsing & Clothing Crop

Sử dụng human parsing mask để xác định vùng quần áo, sau đó tạo bounding box và crop ảnh gốc nhằm tạo một preprocessing variant tập trung vào clothing region.

- Clothing classes: `[1, 2, 3, 4, 5, 6, 21]` (top, outer, skirt, dress, pants, leggings, rompers). Chưa bao gồm footwear/accessories.
- Mask: `clothing_mask = np.isin(parsing_array, CLOTHING_CLASSES)`
- Bounding box được tạo từ clothing mask, cộng thêm padding `PADDING_RATIO = 0.05`.
- Không resize ảnh trong bước crop.

**Crop validation:**

| | 10 samples | 100 samples |
|---|---|---|
| Successful crops | 10 | 100 |
| Empty masks | 0 | 0 |
| Invalid bbox | 0 | 0 |
| Mean clothing area | 12.92% | 13.04% |
| Min clothing area | 5.54% | 4.63% |
| Max clothing area | 20.61% | 38.71% |

Clothing crop pipeline hoạt động ổn định trên các sample test, không phát sinh empty mask hoặc invalid bounding box. Chưa có retrieval benchmark nên chưa thể kết luận crop có cải thiện performance so với original image hay không.

### 4. Fashion-CLIP Embedding

- Model: `patrickjohncyh/fashion-clip`
- Mỗi ảnh tạo 2 embedding: Original và Cropped, dimension 512.
- Thiết lập: CUDA, `model.eval()`, inference/no_grad, L2 normalization.

**Test 10 samples:**

| Metric | Original | Cropped |
|---|---|---|
| Shape | (10, 512) | (10, 512) |
| dtype | float32 | float32 |
| NaN / Inf | False / False | False / False |
| Norm trước normalize | 10.568197 | 10.837465 |
| Norm sau normalize | 1.0 | 1.0 |

Cosine similarity (Original vs Cropped): Mean = 0.802541, Min = 0.715287, Max = 0.907463. Successful: 10/10, Failed: 0.

**Test 100 samples:**

| Metric | Original | Cropped |
|---|---|---|
| Shape | (100, 512) | (100, 512) |
| dtype | float32 | float32 |
| NaN / Inf | False / False | False / False |
| Norm trước normalize | 10.481819 | 10.905988 |
| Norm sau normalize | 1.0 | 1.0 |

Cosine similarity (Original vs Cropped): Mean = 0.810535, Min = 0.665790, Max = 0.956463. Successful: 100/100, Failed: 0.

### 5. Full Dataset Embedding (12,701 ảnh có parsing)

**Môi trường:**

| | |
|---|---|
| Device | CUDA |
| GPU | Tesla T4 |
| Model | patrickjohncyh/fashion-clip |
| Batch size | 16 |

**Kết quả:**

| Metric | Original | Cropped |
|---|---|---|
| Shape | (12701, 512) | (12701, 512) |
| dtype | float32 | float32 |
| NaN / Inf | False / False | False / False |
| Norm (Mean / Min / Max) | 1.0 / 0.9999999 / 1.0000001 | 1.0 / 0.9999998 / 1.0000001 |

**Processing:**

| Metric | Giá trị |
|---|---|
| Successful | 12,701 |
| Failed | 0 |
| Total processing time | 517.69 giây |
| Images/sec | 24.53 |

**Cosine similarity (Original vs Cropped, toàn bộ 12,701 ảnh):**

| Mean | Median | Min | Max | Std |
|---|---|---|---|---|
| 0.79894245 | 0.8048926 | 0.44638282 | 0.9846754 | 0.059038535 |

Original và Cropped embeddings có mức tương đồng tương đối cao nhưng vẫn có sự khác biệt. Chưa có retrieval benchmark nên **chưa kết luận** Cropped tốt hơn Original hay việc cropping cải thiện retrieval performance.

### 6. Output

Các artifact được tạo từ experiment trên Colab và được lưu trên drive:

- `data/processed/deepfashion/embeddings/original_embeddings.npy`
- `data/processed/deepfashion/embeddings/cropped_embeddings.npy`
- `data/processed/deepfashion/embeddings/metadata.csv`
- `data/processed/deepfashion/embeddings/failed_samples.csv`

### 7. Kết luận Tuần 2

- Đã kiểm tra DeepFashion-MultiModal human parsing subset.
- Đã xây dựng clothing crop dựa trên human parsing.
- Crop pipeline đã được validation trên 10 và 100 samples.
- Đã triển khai Fashion-CLIP embedding pipeline.
- Đã tạo embedding cho toàn bộ 12,701 ảnh có parsing.
- Original và Cropped embeddings đều có dimension 512, được L2 normalize.
- Không có NaN/Inf; 12,701/12,701 samples thành công.
- Embedding artifacts đã sẵn sàng để sử dụng ở các bước retrieval tiếp theo.

### 8. Kế hoạch cho tuần tiếp theo

- FAISS indexing (Original Index và Cropped Index).
- Baseline retrieval.
- So sánh Original vs Cropped.
- Retrieval evaluation.

