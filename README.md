# VisFit

## Multimodal Fashion Retrieval and Outfit Recommendation System

**VisFit** là hệ thống **truy hồi và gợi ý thời trang đa tác vụ dựa trên mô hình đa phương thức (Multimodal AI)**.

Đồ án tập trung xây dựng một hệ thống có khả năng hiểu và kết hợp thông tin từ **hình ảnh và văn bản**, phục vụ ba tác vụ chính:

* **Basic Fashion Retrieval** – truy hồi sản phẩm thời trang cơ bản.
* **Image-Text Composed Retrieval** – truy hồi sản phẩm dựa trên ảnh tham chiếu kết hợp yêu cầu chỉnh sửa bằng văn bản.
* **Outfit Recommendation** – gợi ý các sản phẩm có khả năng phối hợp với sản phẩm đầu vào.

Đồ án được thực hiện trong thời gian **24/08/2026 – 12/12/2026**.

---

## 1. Mục tiêu

VisFit hướng tới xây dựng một pipeline hoàn chỉnh từ:

```text
Dataset
   ↓
Data Preprocessing
   ↓
Feature Extraction
   ↓
Benchmarking
   ↓
Shared Backbone
   ↓
Task-specific Models
   ↓
FAISS Retrieval
   ↓
Web Demo
```

Các mục tiêu chính:

1. Benchmark các mô hình **Text-only, Image-only và Multimodal**.
2. So sánh hiệu năng bằng các metric:

   * Recall@K
   * Precision@K
   * NDCG@K
3. Đánh giá và lựa chọn **Fashion-CLIP** làm Shared Backbone.
4. Xây dựng hệ thống gồm ba nhánh:

   * **Task A:** Basic Retrieval
   * **Task B:** Composed Retrieval
   * **Task C:** Outfit Recommendation
5. Xây dựng Web Demo bằng Streamlit.
6. Tích hợp FAISS để thực hiện similarity search.
7. Đánh giá hệ thống bằng các metric phù hợp cho từng task.

Đề cương xác định ba nhánh này là thành phần cốt lõi của hệ thống VisFit.

---

# 2. System Architecture

Kiến trúc tổng quát:

```text
                        ┌─────────────────┐
                        │      Input      │
                        │                 │
                        │ Image / Text /  │
                        │ Image + Text    │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Intent Router  │
                        └────────┬────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │   Task A     │ │   Task B     │ │   Task C     │
        │    Basic     │ │   Composed   │ │    Outfit    │
        │   Retrieval  │ │   Retrieval  │ │ Recommendation│
        └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
               │                │                │
               ▼                ▼                ▼
        Fashion-CLIP      Fusion Module        CSA-Net
               │                │                │
               │                ▼                ▼
               │          Target Embedding   Compatibility
               │                │              Space
               │                │                │
               └────────────────┼────────────────┘
                                │
                                ▼
                              FAISS
                                │
                                ▼
                           Top-K Results
                                │
                                ▼
                          Streamlit Web
```

Hệ thống sử dụng **Fashion-CLIP làm Shared Backbone**, sau đó phân luồng sang ba Task Heads chuyên biệt.

---

# 3. Datasets

VisFit sử dụng ba bộ dữ liệu thời trang:

## 3.1 DeepFashion-MultiModal

DeepFashion-MultiModal cung cấp:

* Hình ảnh người mặc trang phục.
* Natural language descriptions.
* Fashion attributes.
* Human parsing mask.
* Keypoints.

Do ảnh là ảnh người mặc thay vì ảnh sản phẩm đơn lẻ, VisFit sử dụng **human parsing mask** để crop vùng trang phục nhằm giảm nhiễu từ:

* Khuôn mặt.
* Tư thế.
* Background.

Ảnh sau preprocessing được resize về kích thước phù hợp với các Image Encoder.

> **License:** DeepFashion-MultiModal được sử dụng trong phạm vi nghiên cứu phi thương mại theo yêu cầu của đề cương. Không phân phối lại dataset hoặc các thành phần dữ liệu bị hạn chế.

---

## 3.2 FashionIQ

FashionIQ được sử dụng cho bài toán:

**Image-Text Composed Retrieval**

Input gồm:

```text
Reference Image
        +
Modification Text
        ↓
Target Product
```

Ví dụ:

```text
Reference:
White shirt

Text:
"Keep the style but change it to blue with short sleeves."
```

Mô hình cần giữ lại những đặc điểm phù hợp từ ảnh tham chiếu đồng thời áp dụng thay đổi được mô tả bằng text.

---

## 3.3 Polyvore Outfits

Polyvore Outfits được sử dụng cho bài toán:

**Outfit Compatibility / Recommendation**

Ví dụ:

```text
Shirt
  +
Pants
  +
Shoes
  ↓
Compatible Outfit
```

Mục tiêu không phải tìm sản phẩm giống nhau mà là tìm sản phẩm **phù hợp để phối cùng nhau**.

---

# 4. Benchmarking

Trước khi xây dựng hệ thống chính, VisFit thực hiện Benchmarking giữa ba nhóm mô hình.

## Image-only

| Model        |
| ------------ |
| ResNet50     |
| EfficientNet |


## Text-only

| Model    |
| -------- |
| TF-IDF   |
| FastText |
| SBERT    |

## Multimodal

| Model        |
| ------------ |
| Fashion-CLIP |

Các mô hình được đánh giá trên cùng một thiết lập dữ liệu với:

* Recall@K
* Precision@K
* NDCG@K

Kết quả Benchmarking được sử dụng làm cơ sở thực nghiệm để lựa chọn Shared Backbone cho hệ thống.

---

# 5. Task A – Basic Fashion Retrieval

Task A thực hiện truy hồi sản phẩm thời trang cơ bản bằng Fashion-CLIP và FAISS.

### Pipeline

```text
Input Image / Text
       ↓
Fashion-CLIP
       ↓
Embedding
       ↓
L2 Normalization
       ↓
FAISS
       ↓
Similarity Search
       ↓
Top-K Products
```

Task A sử dụng không gian embedding chung của Fashion-CLIP để hỗ trợ truy hồi giữa hình ảnh và văn bản.

Các kỹ thuật chính:

* Shared Latent Space
* L2 Normalization
* Cosine Similarity
* Maximum Inner Product Search (MIPS)

Task A không yêu cầu huấn luyện thêm một prediction head mới.

---

# 6. Task B – Image-Text Composed Retrieval

Task B giải quyết bài toán **Image-Text Composed Retrieval**.

Người dùng cung cấp:

```text
Reference Image
       +
Modification Text
       ↓
Desired Product
```

### Pipeline

```text
Reference Image
       ↓
Image Encoder
       ↓
Image Feature
                    ┐
                    ├──→ Fusion Module
                    │
Text Query          │
       ↓            │
Text Encoder ───────┘
                    ↓
              Target Embedding
                    ↓
                  FAISS
                    ↓
               Top-K Results
```

Fusion Module được xây dựng bằng PyTorch, sử dụng:

* Linear Projection
* Cross-Attention
* DVR
* TME
* Contrastive Loss

Một vấn đề quan trọng của Task B là **Reference Dominance**, khi đặc trưng của ảnh tham chiếu có thể lấn át thông tin chỉnh sửa trong text. Cross-Attention được sử dụng để học quan hệ giữa image feature và text feature.

---

# 7. Task C – Outfit Recommendation

Task C chuyển bài toán từ:

> "Find a similar product"

sang:

> "Find a compatible product"

Mô hình sử dụng:

**Category-Specific Attribute Network (CSA-Net)**

để ánh xạ sản phẩm vào một **Compatibility Space**.

### Pipeline

```text
Product Image
      ↓
Fashion-CLIP
      ↓
Image Feature
      ↓
CSA-Net
      ↓
Compatibility Space
      ↓
Compatibility Score
      ↓
Compatible Products
```

CSA-Net học quan hệ tương hợp giữa các sản phẩm thuộc các danh mục khác nhau, ví dụ:

```text
Shirt → Pants
Shirt → Shoes
Pants → Shoes
Dress → Shoes
```

Các khái niệm chính:

* Category-Specific Attribute Network
* Compatibility Space
* Compatibility Score
* FITB (Fill-in-the-Blank)

---

# 8. Offline Feature Extraction

Để giảm yêu cầu GPU trong quá trình training Task B và Task C, VisFit sử dụng chiến lược **Offline Feature Extraction**.

```text
Dataset
   ↓
Preprocessing
   ↓
Fashion-CLIP
   ↓
Feature Extraction
   ↓
.npy Files
   ↓
Model Training
```

Thay vì chạy Fashion-CLIP nhiều lần trong quá trình training, embedding được trích xuất trước và lưu thành `.npy`.

### Lợi ích

* Giảm training time.
* Giảm GPU usage.
* Giảm memory requirement.
* Tách Feature Extraction khỏi Model Training.
* Dễ dàng thực hiện nhiều experiment.

---

# 9. Evaluation Metrics

## Retrieval

### Recall@K

Sử dụng:

```text
Recall@1
Recall@5
Recall@10
Recall@50
```

Recall@K đo tỷ lệ trường hợp Ground Truth xuất hiện trong K kết quả đầu tiên.

---

### Precision@K

Đo tỷ lệ kết quả liên quan trong Top-K kết quả được truy hồi.

---

### NDCG@K

Đánh giá chất lượng ranking của kết quả.

Kết quả đúng xuất hiện càng gần vị trí đầu tiên thì NDCG càng cao.

---

## Outfit Recommendation

### FITB Accuracy

FITB (Fill-in-the-Blank) đánh giá khả năng chọn đúng sản phẩm còn thiếu trong outfit.

Ví dụ:

```text
Shirt + Pants + [?]
                ↓
              Shoes
```

---

### Compatibility Score

Đánh giá mức độ tương hợp giữa các sản phẩm.

### AUC

Đánh giá khả năng phân biệt:

```text
Compatible Outfit
        vs
Incompatible Outfit
```

---

# 10. Project Structure

```text
VisFit/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   ├── DeepFashion-MultiModal/
│   │   ├── FashionIQ/
│   │   └── Polyvore/
│   │
│   └── processed/
│       ├── images/
│       ├── metadata/
│       └── embeddings/
│
├── models/
│   └── .gitkeep
│
├── notebooks/
│   └── Colab_Extract_Embeddings.ipynb
│
├── src/
│   ├── dataloader/
│   │   └── fashion_dataset.py
│   │
│   ├── models/
│   │   ├── fusion_module.py
│   │   └── csa_net.py
│   │
│   ├── preprocessing.py
│   ├── data_profiling.py
│   │
│   └── utils/
│       ├── metrics.py
│       └── visualization.py
│
├── docs/
│   └── visfit_weekly_log.md
│
└── app.py
```

---

# 11. Installation

## 11.1 Clone repository

```bash
git clone https://github.com/tn4u/VisFit.git
cd VisFit
```

---

## 11.2 Create virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 11.3 Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# 12. GPU Environment

VisFit sử dụng PyTorch để thực hiện Deep Learning và Feature Extraction.

Kiểm tra GPU:

```python
import torch

print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
```

Expected:

```text
CUDA available: True
GPU: NVIDIA ...
```

Nếu CUDA không được nhận diện, cần kiểm tra:

* NVIDIA Driver
* PyTorch CUDA build
* Python version
* CUDA compatibility

---

# 13. Data Preparation

Dataset được lưu local và **không được commit lên GitHub**.

Ví dụ:

```text
data/
├── raw/
│   ├── DeepFashion-MultiModal/
│   ├── FashionIQ/
│   └── Polyvore/
│
└── processed/
    ├── images/
    ├── metadata/
    └── embeddings/
```

Chạy preprocessing:

```bash
python src/preprocessing.py
```

Quá trình preprocessing bao gồm:

1. Đọc metadata.
2. Làm sạch text.
3. Chuẩn hóa thông tin sản phẩm.
4. Đọc human parsing mask.
5. Crop vùng trang phục.
6. Resize ảnh.
7. Lưu dữ liệu processed.

---

# 14. Feature Extraction

Feature Extraction được thực hiện offline.

Ví dụ:

```bash
python notebooks/Colab_Extract_Embeddings.ipynb
```

Các embedding được lưu dưới dạng:

```text
.npy
```

và phải duy trì mapping:

```text
product_id → embedding
```

để đảm bảo vector ảnh và vector text được đồng bộ.

---

# 15. FAISS

FAISS được sử dụng làm vector database cho similarity search.

Pipeline:

```text
Product Embeddings
       ↓
L2 Normalization
       ↓
FAISS Index
       ↓
Query Embedding
       ↓
Similarity Search
       ↓
Top-K Products
```

FAISS được sử dụng đặc biệt cho Task A và Task B. Đề cương xác định Task A sử dụng Fashion-CLIP embedding kết hợp FAISS để thực hiện tìm kiếm sản phẩm tương đồng.

---

# 16. Training

## Task B

Training data:

```text
Reference Image
+
Modification Text
+
Target Image
```

Loss:

```text
Contrastive Loss
```

Các hyperparameter cần thử nghiệm:

* Learning rate
* Batch size
* Number of Cross-Attention layers
* Number of attention heads

Mục tiêu là lựa chọn checkpoint tốt nhất trên validation set FashionIQ.

---

## Task C

Training dataset:

```text
Polyvore Outfits
```

Dữ liệu được chia theo **Disjoint Set** để hạn chế data leakage giữa train/validation/test.

CSA-Net được train để học Compatibility Space.

Các metric:

* FITB Accuracy
* Compatibility Score
* AUC

---

# 17. Run Web Demo

VisFit sử dụng Streamlit cho Web Demo.

Chạy:

```bash
streamlit run app.py
```

Web Demo dự kiến hỗ trợ:

### Basic Retrieval

```text
Image
   ↓
Fashion-CLIP
   ↓
FAISS
   ↓
Top-K Products
```

### Composed Retrieval

```text
Image + Text
      ↓
Fusion Module
      ↓
FAISS
      ↓
Top-K Products
```

### Outfit Recommendation

```text
Product
   ↓
CSA-Net
   ↓
Compatibility Space
   ↓
Recommended Products
```

---

# 18. Git Workflow

## Branches

Khuyến nghị sử dụng:

```text
main
develop
feature/<feature-name>
```

Ví dụ:

```bash
git checkout -b feature/preprocessing
git checkout -b feature/faiss
git checkout -b feature/fusion-module
git checkout -b feature/csa-net
git checkout -b feature/streamlit
```

---

## Commit convention

Sử dụng các prefix:

```text
feat:
fix:
refactor:
docs:
test:
chore:
```

Ví dụ:

```bash
git add .
git commit -m "feat: add fashion image preprocessing pipeline"
```

```bash
git commit -m "feat: implement FAISS similarity search"
```

```bash
git commit -m "fix: resolve image preprocessing issue"
```

---

# 19. Team Responsibilities

## Tuấn – SV1

Các nhiệm vụ chính:

* Thu thập và kiểm tra dataset.
* Data profiling.
* Làm sạch text.
* Chuẩn hóa metadata.
* Mapping ground truth.
* Sinh attribute prompt.
* Text Feature Extraction.
* Benchmark Text-only.
* Benchmark Image-only.
* FashionIQ DataLoader.
* Đánh giá Recall@K / Precision@K / NDCG@K.
* Polyvore Disjoint preprocessing.
* FITB Accuracy.
* AUC.
* Intent Router.
* User Testing.
* Viết các chương liên quan đến nghiên cứu và thực nghiệm.

Phân công này được lấy từ kế hoạch triển khai VisFit.

---

## Khanh – SV2

Các nhiệm vụ chính:

* Khởi tạo GitHub repository.
* Thiết lập môi trường PyTorch/CUDA.
* Quản lý `README.md` và `requirements.txt`.
* Image preprocessing.
* Crop ảnh bằng human parsing mask.
* Image Feature Extraction.
* FAISS.
* Fashion-CLIP Shared Backbone.
* Cross-Attention Adapter.
* Fusion Module.
* CSA-Net.
* Training và Hyperparameter Tuning.
* t-SNE visualization.
* Checkpoint management.
* Streamlit Web Demo.
* Tích hợp FAISS vào Web Demo.
* Tối ưu inference.
* Viết Chương 3 và Chương 6.

## Các nhiệm vụ trên được xác định trong kế hoạch triển khai của SV2.

# 20. Expected Outputs

## Source Code

* Preprocessing
* Feature Extraction
* Benchmarking
* FAISS Retrieval
* Fusion Module
* Task B Training
* CSA-Net
* Task C Training
* Streamlit Web Demo

## Data / Features

* Processed metadata
* CSV files
* Image embeddings
* Text embeddings
* `.npy` files
* FAISS Index

## Models

```text
models/
├── fashion_clip/
├── task_b/
└── csa_net/
```

Model checkpoints:

* Fashion-CLIP Backbone
* Task B checkpoint
* CSA-Net checkpoint

## Evaluation

Expected evaluation results:

```text
Recall@1
Recall@5
Recall@10
Recall@50

Precision@K

NDCG@K

FITB Accuracy

Compatibility AUC
```

Các sản phẩm đầu ra này tương ứng với danh sách sản phẩm dự kiến trong đề cương đồ án.

---

# 21. Research Scope and Limitations

VisFit tập trung vào:

* Multimodal Fashion Retrieval.
* Image-Text Composed Retrieval.
* Outfit Compatibility.
* Vector Similarity Search.
* Multimodal Representation Learning.

Phạm vi dữ liệu dự kiến khoảng **10.000–20.000 sản phẩm**, tùy khả năng xử lý và tài nguyên phần cứng.

Đồ án **không tập trung** vào:

* Giá sản phẩm thay đổi theo thời gian.
* Inventory.
* Promotion.
* Lịch sử mua hàng cá nhân.
* Real-time user behavior.

---

# 22. Project Roadmap

```text
[1] Dataset Preparation
        ↓
[2] Data Profiling
        ↓
[3] Image/Text Preprocessing
        ↓
[4] Offline Feature Extraction
        ↓
[5] Benchmarking
        ↓
[6] Fashion-CLIP Selection
        ↓
[7] FAISS Retrieval
        ↓
[8] Task A
        ↓
[9] Fusion Module / XAA
        ↓
[10] Task B
        ↓
[11] CSA-Net
        ↓
[12] Task C
        ↓
[13] Intent Router
        ↓
[14] Streamlit Web Demo
        ↓
[15] Evaluation
        ↓
[16] Final Report
```

---

# 23. Citation / References

Các phương pháp và kiến trúc được sử dụng trong VisFit được nghiên cứu dựa trên các hướng tiếp cận liên quan đến:

* Fashion-CLIP
* FAME-ViL
* FashionERN
* CSA-Net
* FAISS
* Cross-Attention
* Contrastive Learning
* Multimodal Representation Learning

Chi tiết tài liệu tham khảo sẽ được bổ sung trong quá trình nghiên cứu và hoàn thiện báo cáo.

---

# 24. License and Dataset Notice

Source code của project được phát triển phục vụ mục đích học tập và nghiên cứu.

Các dataset bên thứ ba phải được sử dụng theo license/terms của từng dataset.

Đặc biệt, **DeepFashion-MultiModal chỉ được sử dụng cho mục đích nghiên cứu phi thương mại** theo phạm vi của đồ án. Không commit hoặc phân phối dataset lên repository GitHub.


