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
#### 👤 Sinh viên 1: Tuấn (SV1) - Phụ trách Data & Analytics
### 1. Mục tiêu trọng tâm của tuần
- Text preprocessing cho Branch A (DeepFashion-MultiModal) và Branch B (FashionIQ).
- Làm sạch nhãn text: loại bỏ ký tự nhiễu, chuẩn hóa chính tả bằng Regex.
- Chuẩn hóa định dạng Schema chung cho toàn bộ dự án.
- Ánh xạ ground truth, thiết lập tập Query/Gallery và Train/Val/Test.

### 2. Dataset Inspection (Text Metadata)

| Hạng mục | DeepFashion-MultiModal | FashionIQ |
|---|---|---|
| **Nguồn dữ liệu gốc** | CSV tổng hợp | JSON lồng nhau (đã gộp thành CSV) |
| **Total records** | 12,278 | 24,016 |
| **Missing values (NaN)** | 0 | 0 |
| **Cấu trúc trường dữ liệu** | `image_id`, `caption`, `product_id`, `category` | `candidate`, `target`, `caption`, `source_file` |
| **Độ dài caption (trung bình)** | 234 ký tự | 65 ký tự |
| **Định dạng bài toán** | Basic Retrieval | Composed Retrieval (Triplet) |

### 3. Text Cleaning & Schema Normalization
Áp dụng biểu thức chính quy (Regex) để làm sạch toàn bộ mô tả sản phẩm và câu lệnh chỉnh sửa, chuyển đổi về một Schema chuẩn `visfit_schema`.

- **Pipeline xử lý**: Lowercase $\rightarrow$ Loại bỏ dấu câu $\rightarrow$ Xóa khoảng trắng thừa $\rightarrow$ Trích xuất Category.
- **Cấu trúc Schema lõi**: `dataset_source`, `category`, `clean_caption`, `partition`.

**Validation mẫu sau khi làm sạch:**

| Dataset | Text gốc (Original) | Text đã làm sạch (Cleaned) |
|---|---|---|
| DeepFashion | "It is a grey shirt... and has pawn star on it!!" | "it is a grey shirt and has pawn star on it" |
| FashionIQ | "has no sleeves, and is light pink & pink" | "has no sleeves and is light pink and pink" |

### 4. Ground Truth Partitioning
Xây dựng thuật toán phân chia tập đánh giá dựa trên đặc thù của từng bộ dữ liệu.

**Đối với DeepFashion-MultiModal (Tạo Query/Gallery):**
- Thuật toán đếm số lượng ảnh theo `product_id`. Chỉ các sản phẩm có $\ge 2$ ảnh mới đủ điều kiện làm Query.
- Lấy mẫu ngẫu nhiên (seed=42) 1,000 ID sản phẩm hợp lệ, mỗi ID chọn 1 ảnh làm `query`, các ảnh còn lại đẩy vào `gallery`.

**Đối với FashionIQ (Tạo Train/Val):**
- Trích xuất nhãn phân tập trực tiếp từ tên file gốc (`source_file`).

**Kết quả phân bổ (Data Partitioning Results):**

| Tập dữ liệu | Partition | Số lượng (Records) | Tỷ lệ |
|---|---|---|---|
| **DeepFashion** | Gallery | 11,278 | 91.8% |
| | Query | 1,000 | 8.2% |
| **FashionIQ** | Train | 18,000 | 75.0% |
| | Val | 6,016 | 25.0% |

### 5. Output
Các artifact được tạo từ quá trình xử lý và lưu trữ trên thư mục `data/processed/metadata/`:
- `df_multimodal_query_gallery.csv`
- `df_fashioniq_schema.csv`

### 6. Kết luận Tuần 2 (SV1)
- Đã hoàn thành 100% làm sạch text cho 36,294 mẫu từ cả 2 bộ dữ liệu.
- Schema dự án đã được đồng nhất, đảm bảo tính tương thích cao cho các bước ghép nối.
- Pipeline chia tập Query/Gallery tự động hoạt động chính xác. Dữ liệu đã sẵn sàng để sinh Prompt ở tuần tiếp theo.

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

## TUẦN 3: 07/09/2026 – 13/09/2026

#### 👤 Sinh viên 1: Tuấn (SV1) - Phụ trách Data & Analytics
### 1. Mục tiêu trọng tâm của tuần
- Xây dựng script sinh Prompt thuộc tính (Attribute Prompt) từ metadata.
- Tách biệt định dạng đầu vào tối ưu cho 2 nhánh mô hình: Text-only (SBERT/TF-IDF) và Vision-Language (Fashion-CLIP).
- Lấy mẫu đánh giá chất lượng prompt sinh ra.

### 2. Prompt Engineering Design
Do yêu cầu đặc thù của các kiến trúc mạng khác nhau, pipeline sinh text được thiết kế phân nhánh:

- **Nhánh Text-only (`text_only_input`)**: Dữ liệu được giữ nguyên dưới dạng văn bản mô tả thuần túy (giữ lại `clean_caption`) để tránh làm loãng trọng số từ vựng của TF-IDF/SBERT.
- **Nhánh Vision-Language (`fashion_clip_prompt`)**: Cấu trúc thành câu hoàn chỉnh mang ngữ cảnh hình ảnh để mô hình Fashion-CLIP dễ dàng ánh xạ sang không gian ảnh.
  - *Template áp dụng*: `"a photo of a {category}, {clean_caption}"`.

### 3. Prompt Quality Validation
Thực hiện lấy mẫu ngẫu nhiên (random sampling) để đối chiếu giữa câu lệnh sinh tự động và nội dung thực tế của hình ảnh.

| Ảnh ID (Sample) | Model Target | Output Prompt Sinh Tự Động | Đánh giá |
|---|---|---|---|
| `WOMEN-Blouses_Shirts...` | Text-only | "the shirt this person wears has long sleeves..." | Đạt |
| `WOMEN-Blouses_Shirts...` | Fashion-CLIP | "a photo of a women blouses shirts, the shirt this person wears has long sleeves..." | Đạt |
| `MEN-Tees_Tanks-id...` | Fashion-CLIP | "a photo of a men tees tanks, the person wears a tank tank top with color block patterns..." | Đạt |

*Nhận xét đánh giá:* Các câu lệnh được sinh ra trôi chảy, đúng ngữ pháp tiếng Anh, thông tin category và caption được nối liền mạch. Đã đối chiếu chéo trực tiếp với file ảnh `.jpg` gốc và xác nhận thuộc tính miêu tả hoàn toàn khớp với hình ảnh thị giác.

### 4. Output
Các artifact được tạo từ quá trình sinh Prompt và lưu trữ trên thư mục metadata:
- `data/processed/metadata/df_multimodal_prompts.csv`

### 5. Kết luận Tuần 3 (SV1)
- Hoàn thiện 100% việc chuẩn bị dữ liệu văn bản kép cho Nhánh A.
- Phân tách thành công đầu vào chuyên biệt cho mô hình Text-only và Fashion-CLIP.
- Không phát sinh lỗi logic trong quá trình sinh mẫu. Sẵn sàng tích hợp sang môi trường Colab để chạy Feature Extraction offline ở Tuần 4.

#### 👤 Sinh viên 2: Khanh (SV2) - Phụ trách Vision Pipeline & Retrieval Evaluation

### 1. Mục tiêu trọng tâm của tuần
- Xây dựng các baseline ảnh để chuẩn bị so sánh với Fashion-CLIP trong bài toán Image Retrieval.
- Chuẩn hóa và lưu trữ embedding dưới dạng `.npy` để phục vụ FAISS indexing.
- Nghiên cứu official DeepFashion In-shop Clothes Retrieval partition.
- Xây dựng mapping giữa DeepFashion-MultiModal và In-shop benchmark.
- Thiết lập tập Query/Gallery và Ground Truth hợp lệ cho bước đánh giá retrieval.

---

### 2. Image Embedding với các Pretrained Image Encoder

Sau khi hoàn thành Fashion-CLIP embedding ở tuần trước, trong tuần này tiến hành mở rộng pipeline trích xuất đặc trưng ảnh với 4 kiến trúc pretrained khác nhằm tạo các baseline để so sánh chất lượng retrieval.

Các model được sử dụng:

- ResNet50
- EfficientNet-B0
- VGG16
- ViT-B/16

Toàn bộ model sử dụng pretrained weights, chưa thực hiện fine-tuning.

#### 2.1. Thiết lập thực nghiệm

- Dataset: DeepFashion-Multi-Modal.
- Subset sử dụng: 12,701 ảnh có Human Parsing Mask.
- Input: Cropped clothing image được tạo từ preprocessing pipeline đã xây dựng ở tuần trước.
- Device: CUDA GPU.
- Batch inference.
- Không cập nhật trọng số model.
- Embedding được chuyển về `float32`.
- Áp dụng L2 Normalization trước khi lưu.
- Không ghi nhận lỗi trong quá trình inference.

#### 2.2. Kết quả Image Embedding

| Model | Samples | Embedding Dimension | Failed | Processing Time (s) | Images/sec |
|---|---:|---:|---:|---:|---:|
| ResNet50 | 12,701 | 2,048 | 0 | 185.65 | 68.41 |
| EfficientNet-B0 | 12,701 | 1,280 | 0 | 150.94 | 84.15 |
| VGG16 | 12,701 | 4,096 | 0 | 151.71 | 83.72 |
| ViT-B/16 | 12,701 | 768 | 0 | 166.97 | 76.07 |

Tất cả 4 model đều xử lý thành công toàn bộ 12,701 ảnh, không phát sinh failed sample.

#### 2.3. So sánh với Fashion-CLIP

Fashion-CLIP embedding đã được hoàn thành ở tuần trước và được giữ làm model chính của hệ thống.

| Model | Embedding Dimension | Samples | Images/sec |
|---|---:|---:|---:|
| Fashion-CLIP | 512 | 12,701 | 24.53 |
| ResNet50 | 2,048 | 12,701 | 68.41 |
| EfficientNet-B0 | 1,280 | 12,701 | 84.15 |
| VGG16 | 4,096 | 12,701 | 83.72 |
| ViT-B/16 | 768 | 12,701 | 76.07 |

EfficientNet-B0 đạt tốc độ trích xuất cao nhất trong nhóm benchmark, trong khi Fashion-CLIP có tốc độ thấp hơn do kiến trúc Vision-Language phức tạp hơn.

Tuy nhiên, tốc độ inference **không phản ánh trực tiếp chất lượng retrieval**. Chưa thể kết luận model nào tốt nhất trước khi thực hiện FAISS retrieval và đánh giá bằng Recall@K/mAP.

#### 2.4. Output

Embedding của từng model được lưu độc lập để phục vụ bước xây dựng FAISS Index:

- `data/processed/embeddings/resnet50/cropped_embeddings.npy`
- `data/processed/embeddings/efficientnet_b0/cropped_embeddings.npy`
- `data/processed/embeddings/vgg16/cropped_embeddings.npy`
- `data/processed/embeddings/vit_b16/cropped_embeddings.npy`

Mỗi thư mục đồng thời lưu:
- `metadata.csv`
- `failed_samples.csv`

Các embedding đã được L2 normalize và sẵn sàng cho Cosine Similarity / FAISS Inner Product Search.

---

### 3. Xây dựng Ground Truth cho Image Retrieval

Sau khi hoàn tất các Image Embedding baseline, tiến hành xây dựng Ground Truth để đảm bảo các model có thể được đánh giá trên cùng một tập Query/Gallery.

Do DeepFashion-Multi-Modal subset hiện tại không cung cấp trực tiếp Query/Gallery chuẩn cho bài toán retrieval, tiến hành ánh xạ dữ liệu với official **DeepFashion In-shop Clothes Retrieval** benchmark.

### 3.1. Official In-shop Partition

Sử dụng file official:

`list_eval_partition.txt`

File chứa các trường:

- `image_name`
- `item_id`
- `evaluation_status`

Trong đó `evaluation_status` gồm:

- `train`
- `query`
- `gallery`

`item_id` được sử dụng làm Product Identity để xác định positive gallery image cho mỗi query.

---

### 3.2. DeepFashion-Multi-Modal ↔ In-shop Mapping

Image ID trong DeepFashion-Multi-Modal có dạng:

`MEN-Denim-id_00000089-01_7_additional`

Từ đó trích xuất Product ID:

`id_00000089`

Product ID được đối chiếu với `item_id` trong official In-shop partition.

Mapping chỉ được sử dụng để tạo Ground Truth khi ảnh có thể ánh xạ đủ điều kiện với official partition.

Quá trình mapping tạo ra các artifact:

- `mapping_result.csv`
- `mapping_statistics.csv`

---

### 3.3. Tạo Query, Gallery và Ground Truth

Sau quá trình mapping, tập dữ liệu ban đầu thu được:

| Thành phần | Số lượng |
|---|---:|
| Query images ban đầu | 3,540 |
| Gallery images | 2,944 |
| Query-positive pairs | 4,697 |

Positive Gallery của mỗi Query được xác định là các Gallery image có cùng `item_id`.

Ground Truth được lưu dưới dạng cặp:

`Query Image → Positive Gallery Image`

---

### 3.5. Phân tích Query không có Positive Gallery

Trong quá trình validation phát hiện:

**1,650 / 3,540 Query images không có Positive Gallery tương ứng trong subset hiện tại.**

Tiến hành phân tích nguyên nhân theo `item_id`.

Kết quả:

| Nguyên nhân | Số Item |
|---|---:|
| Official In-shop partition không có Gallery | 0 |
| Gallery tồn tại trong official benchmark nhưng không nằm trong DFM-MM parsing subset | 1,402 |

Kết quả cho thấy toàn bộ lỗi không đến từ official benchmark.

Các item này đều có Gallery image trong official In-shop dataset, tuy nhiên Gallery image tương ứng không xuất hiện trong subset 12,701 ảnh có parsing của DeepFashion-Multi-Modal đang được sử dụng.

Do đó không thể đánh giá retrieval cho các Query này trên embedding hiện tại.

---

### 3.6. Lọc Evaluation Query

Để đảm bảo metric retrieval hợp lệ, chỉ giữ lại Query có ít nhất một Positive Gallery trong tập Gallery hiện tại.

Kết quả sau filtering:

| Thành phần | Số lượng |
|---|---:|
| Query ban đầu | 3,540 |
| Query không có Positive | 1,650 |
| Valid Evaluation Query | 1,890 |
| Gallery | 2,944 |
| Ground Truth Positive Pairs | 4,697 |

Tỷ lệ Query có thể sử dụng để đánh giá:

**1,890 / 3,540 = 53.39%**

1,650 Query bị loại được lưu riêng để phục vụ audit và kiểm tra lại dataset.

Evaluation hiện tại vì vậy được xác định là:

> Evaluation trên tập con DeepFashion-Multi-Modal có thể ánh xạ với official In-shop Clothes Retrieval partition.

Không coi đây là kết quả trên toàn bộ official In-shop benchmark.

---

### 3.7. Ground Truth Output

Các artifact được tạo:

- `ground_truth/query.csv`
- `ground_truth/gallery.csv`
- `ground_truth/ground_truth.csv`
- `ground_truth/query_without_positive.csv`
- `mapping_result.csv`
- `mapping_statistics.csv`

Trong đó:

- `query.csv`: chứa các Query hợp lệ để evaluation.
- `gallery.csv`: chứa Gallery images.
- `ground_truth.csv`: chứa các Query-Positive Gallery pair.
- `query_without_positive.csv`: chứa các Query bị loại do không có positive trong current subset.

---

### 4. Kết luận Tuần 3 (SV2)

Trong tuần đã hoàn thành hai nhóm công việc chính.

**Image Feature Extraction:**
- Hoàn thành embedding cho 4 pretrained Image Encoder:
  - ResNet50
  - EfficientNet-B0
  - VGG16
  - ViT-B/16
- Embedding đã được L2 normalize và lưu dưới dạng `.npy`.
- Cùng với Fashion-CLIP, hiện tại đã có 5 Image Encoder để thực hiện benchmark retrieval.

**Ground Truth Construction:**
- Xây dựng mapping giữa DeepFashion-Multi-Modal và official In-shop dataset.
- Tạo Query/Gallery/Ground Truth cho subset hiện tại.
- Sau filtering còn 1,890 valid Query, 2,944 Gallery images và 4,697 positive pairs.
- Ground Truth đã sẵn sàng để sử dụng cho FAISS Retrieval Evaluation.

---

### 5. Kế hoạch cho tuần tiếp theo


- Xây dựng FAISS Index từ Gallery embeddings.
- Chạy retrieval cho toàn bộ 1,890 valid queries.
- Đánh giá các metric:
  - Recall@1
  - Recall@5
  - Recall@10
  - Recall@20
  - mAP
- So sánh retrieval performance giữa:
  - Fashion-CLIP
  - ResNet50
  - EfficientNet-B0
  - VGG16
  - ViT-B/16
- Đánh giá thêm Original Image vs Cropped Image đối với Fashion-CLIP.
- Phân tích qualitative retrieval bằng cách trực quan hóa Top-K kết quả đúng/sai.

## TUẦN 4: 14/09/2026 – 20/09/2026

### PHẦN BÁO CÁO CỦA TUẤN (SV1) - Phụ trách Data & Analytics

#### 1. Mục tiêu trọng tâm của tuần
- Chuyển dịch môi trường xử lý văn bản lên Google Colab để tận dụng năng lực tính toán GPU.
- Trích xuất đặc trưng (Feature Extraction) cho toàn bộ dữ liệu text của Nhánh A (DeepFashion) nhằm phục vụ bài toán Basic Retrieval.
- Xây dựng các thang đo cơ sở (Text Baselines) đa dạng từ truyền thống đến hiện đại (TF-IDF, FastText, SBERT) để đối chiếu với mô hình đa phương thức (Fashion-CLIP).
- Lưu trữ dữ liệu dưới định dạng vector numpy (`.npy`) offline để tối ưu tốc độ truy xuất.

#### 2. Môi trường triển khai
- **Nền tảng:** Google Colab.
- **Phần cứng:** Tesla T4 GPU.
- **Thư viện lõi:** `sentence-transformers`, `transformers` (Hugging Face), `gensim`, `scikit-learn`.

#### 3. Quá trình Trích xuất Đặc trưng (Text Embedding Pipeline)
Dựa trên 2 trường dữ liệu đầu vào đã phân tách từ Tuần 3 (`text_only_input` và `fashion_clip_prompt`), pipeline trích xuất được thiết kế cho 4 Text Encoder khác nhau:

| Text Encoder | Nguồn cấp | Thiết lập / Model sử dụng | Loại dữ liệu | Mục đích |
|---|---|---|---|---|
| **TF-IDF** | `scikit-learn` | Trích xuất theo tần suất từ vựng (chạy trên CPU) | Rời rạc (Sparse) | Baseline truyền thống dựa trên từ vựng |
| **FastText** | `gensim` | Train trực tiếp trên tập từ vựng thời trang dự án (Vector = 300) | Dày đặc (Dense) | Baseline truyền thống hiểu hình thái từ |
| **SBERT** | Hugging Face | `all-MiniLM-L6-v2` (chạy batch_size=64 trên GPU) | Dày đặc (Dense) | Baseline ngữ nghĩa NLP |
| **Fashion-CLIP** | Hugging Face | `patrickjohncyh/fashion-clip` (Nhánh Text) | Dày đặc (Dense) | Mô hình đích Đa phương thức |

#### 4. Đánh giá chất lượng dữ liệu (Sanity Check)
Sau khi trích xuất, tiến hành kiểm tra ngẫu nhiên (Sample Index = 0, ID: `MEN-Denim-id_00000089-28_1_front`) để xác minh tính toàn vẹn của không gian vector:

*   **Về chiều dữ liệu (Dimension Shape):**
    *   TF-IDF Vector: (101,)
    *   FastText Vector: (300,)
    *   SBERT Vector: (384,)
    *   Fashion-CLIP Vector: (512,) - *Khớp hoàn toàn với không gian 512 chiều của Image Encoder (SV2 thực hiện).*
*   **Về bản chất phân phối:**
    *   **Vector thưa (Sparse):** TF-IDF hoạt động chuẩn xác, mẫu kiểm tra chỉ chứa 23/101 phần tử có giá trị khác 0 (đại diện cho các từ khóa xuất hiện trong câu).
    *   **Vector đặc (Dense):** Cả FastText, SBERT và Fashion-CLIP đều trả về mảng số thực phân phối âm dương đan xen (vd CLIP: `[ 0.827, 1.543, -1.019...]`), chứng tỏ mô hình đã nhúng (embed) thành công ngữ nghĩa tiềm ẩn (latent features) của câu chữ.

#### 5. Output (Artifacts)
Toàn bộ kết quả đã được nén và lưu trữ tĩnh trên Google Drive tại thư mục `data/processed/embeddings/text_features/`, không ghi nhận vector lỗi (NaN/Empty):
- `image_ids.npy` và `product_ids.npy` (Khóa đối chiếu gốc)
- `tfidf_embeddings.npy`
- `fasttext_embeddings.npy`
- `sbert_embeddings.npy`
- `fashionclip_text_embeddings.npy`

#### 6. Kết luận Tuần 4 (SV1)
- Đã hoàn tất 100% việc chuyển đổi không gian văn bản (Text) sang không gian số toán học (Vector) cho 4 kiến trúc Text Encoder.
- Dữ liệu Offline `.npy` đã sẵn sàng, định tuyến hoàn hảo với đặc trưng hình ảnh.
- Bàn giao thành công hệ thống dữ liệu cho SV2 để nạp vào FAISS Index và bắt đầu chạy thử nghiệm truy hồi Cosine Similarity trong tuần tới.