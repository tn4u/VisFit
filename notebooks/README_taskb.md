# Task B — bộ notebook tái hiện tuần44/45

Bộ chính gồm **5 notebook**, cộng **2 nguồn lịch sử** cần để truy vết seed42. Notebook tự chứa lớp/hàm; không import notebook khác. Dữ liệu, feature, checkpoint, cache và log đầy đủ nằm trên Drive, không đưa vào Git.

| Notebook | Nguồn | Chức năng / thứ tự |
|---|---|---|
| [taskb_prepare](taskb_prepare.ipynb) | FashionIQ_Benchmark_Preparation | 1. Kaggle dataset, annotation/mapping/image audit, protocol, split và frozen features |
| [taskb_xaa_dev](taskb_xaa_dev.ipynb) | 01_Development_XAA | 2. Baseline development ba seed; campaign gốc |
| [taskb_dvr_dev](taskb_dvr_dev.ipynb) | 02_Development_DVR_optimized | 3. MR/SR/Full DVR; import baseline hoàn tất có kiểm chứng |
| [taskb_final](taskb_final.ipynb) | 03_Final_Training_OfficialVal_optimized | 4. Khóa E* từ development, fresh heads trên official-train, 12 lượt official-val |
| [taskb_adapter_full](taskb_adapter_full.ipynb) | TME_Adapter_Full_Experiment | Nhánh riêng: development encoder+adapter từng seed → lock → final fresh → benchmark ghép cặp |
| [taskb_encoder_dev](taskb_encoder_dev.ipynb) | TME_Development | Nguồn duy nhất được giữ của Conventional-only seed42 đã reuse; có ablation TME lịch sử, không phải kết quả chính tuần45 |
| [taskb_adapter_dev](taskb_adapter_dev.ipynb) | Colab checked_v2_storagefix | Nguồn thực thi adapter seed42; giữ vì full experiment xác minh đúng legacy code/config/checkpoint này |

Mở Colab GPU, mount Drive và chạy từ trên xuống. Preparation phải đạt đầy đủ trước development. XAA → DVR → final dùng nguồn baseline chỉ đọc ở campaign cũ. Adapter full mặc định preflight; chỉ bật `RUN_FULL_PIPELINE=True` ở cell cuối khi chủ động chạy đủ phase. Có thể chạy phase/seed bằng `CFG` và dispatcher; không chạy lại cell cấu hình khi lượt đang hoạt động. Resume giữ campaign/config/runtime và fingerprint, không reset hoặc sửa hash để vượt lỗi.

Hai notebook lịch sử phục vụ truy vết **artifact đã tồn tại**, không phải bước bắt buộc chạy lại mỗi lần. Encoder lịch sử còn cấu hình `conventional/no_alignment/full`; chỉ Conventional-only seed42 được reuse trong nhánh báo cáo. Adapter lịch sử tham chiếu trial cache/metadata trên Drive, không warm-start trọng số trial. Các notebook chính chứa implementation cần dùng; các path `/Users/...` và tên notebook cũ trong `SOURCE_RECORDS`/hash là bằng chứng provenance lịch sử, không phải đường dẫn cần tồn tại trên Colab. Giữ nguyên chúng để không thay hợp đồng thí nghiệm.

## Protocol và artifact

- Development: 16.204 train / 1.796 internal-val. Final: 18.000 official-train / 6.016 official-val; gallery dress/shirt/toptee: 3.817/6.346/5.373. Điểm gallery nội bộ cũ không so trực tiếp với official-val.
- Exact cosine FP32, reference giữ trong gallery, caption policy đã khóa; truy hồi riêng category. Overall macro, Mean=(R@10+R@50)/2, đơn vị %, sample std `ddof=1` qua đủ seeds42/43/44. Official-val không phải official test.
- Root chung: `MyDrive/ĐATN/data/processed/`. Preparation: `benchmark_preparation/FashionIQ/fashioniq_prep_v1_20261103`.
- XAA baseline: `taskb_training/FashionIQ/heads_v1_20261103/development`; DVR/final: `taskb_training/FashionIQ/heads_v1_20261103_ioopt_v1/{development,final}`.
- Adapter: [campaign artifacts](https://drive.google.com/drive/folders/14cU18AenQZ6KXntGaP40z_ZLKPJ873cU), `tme_adapter_full_experiment/FashionIQ/conventional_retrieval_adapter_full_v1`. Nguồn seed42: `tme_development/FashionIQ/tme_dev_v1_seed42` và `tme_adapter_development/FashionIQ/retrieval_only_dev_v1_base42_adapter42_checked_v2_storagefix`.
- Tài khoản cần quyền Drive/Kaggle. Không lưu credential vào notebook; chỉ upload qua cell xác thực khi cần. Đường dẫn checkpoint/cache thí nghiệm không đổi khi đổi tên file repo.

## Đối chiếu báo cáo

Đã đọc PDF tuần44/45 và `Tuần 45 Adapter.docx`, đối chiếu output đã lưu cùng completion/summary/lock JSON/CSV trên Drive. Các số sau là **kết quả lịch sử**, không phải lượt chạy trong lần rà soát này:

| Official-val | Mean ± sample std (%) |
|---|---:|
| XAA No-FT | 32,532862 ± 0,688069 |
| XAA + MR | 34,255160 ± 0,067996 |
| XAA + SR | 34,150596 ± 0,231587 |
| Full DVR | 34,158901 ± 0,253598 |
| Conventional-only | 34,890330 ± 0,323471 |
| Conventional + retrieval-only residual adapter | 37,074821 ± 0,309345 |

XAA/DVR: E*=8, đủ12 lượt. Adapter: encoder3 epoch (ngân sách đặt trước), adapter9 epoch chọn từ giao các epoch có metric thật của ba seed, earliest tie; đủ6 lượt paired official-val. Chênh Mean adapter +2,184490 điểm, nhưng R@1 giảm trung bình 0,035123 điểm. Nhánh này **lấy cảm hứng TME**, không phải TME nguyên bản, chưa kết hợp DVR và có thêm training text encoder so với XAA/DVR. Không kết luận đạt SOTA hay ý nghĩa thống kê từ ba seed.

Không tìm thấy notebook tổng hợp SOTA riêng trong nguồn được cung cấp; bảng công bố thuộc báo cáo, chưa được chạy tái lập ở đây. Không tạo notebook mới để gán các số công bố thành output thực nghiệm.

## Dọn repo và giới hạn xác minh

Hai XAA/DVR cũ được thay bằng bản development mới; hai encoder week5 được thay bằng preparation nhất quán (historical target gallery chỉ23.742, package mới32.980 target/gallery). Bản gốc còn trong Git history trước commit này. Pilot/trial và checked chưa chạy trong Downloads không nhập hàng loạt. Notebook `FashionIQ_OfficialVal_Benchmark` chưa được tracking được giữ nguyên, không stage: không có output và không phải nguồn final metrics của báo cáo.

Output/debug/widget/user metadata đã xóa; code/config khoa học giữ nguyên, riêng adapter full bỏ cell live probe/driver lỗi trùng và thêm opt-in cho driver thành công. Tổng hợp ngắn ở README thay cho output dài. [Nguồn và SHA](taskb_sources.json) lưu dấu vết trước dọn.

Lần rà soát chỉ kiểm tra JSON/nbformat, cú pháp IPython/Python, định nghĩa trước sử dụng ở cell top-level, tính tự chứa, liên kết/tên file, secret, kích thước và diff; tính lại thống kê adapter từ artifact. Không chạy training, benchmark hay nạp lại checkpoint GPU; chưa xác minh lại toàn bộ binary/shard trong lần này. Saved output và JSON completion là bằng chứng lịch sử, không thay kiểm tra runtime bắt buộc khi chạy lại.
