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