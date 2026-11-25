# Task B — FashionIQ development, official-val và demo

Bộ gồm **7 notebook cho quy trình chính** và **3 nguồn lịch sử** để truy vết seed42. Notebook tự chứa lớp/hàm; không import notebook khác. Dữ liệu, feature, checkpoint, cache và log đầy đủ nằm trên Drive, không đưa vào Git.

| Notebook | Nguồn | Chức năng / thứ tự |
|---|---|---|
| [taskb_prepare](taskb_prepare.ipynb) | FashionIQ_Benchmark_Preparation | 1. Kaggle dataset, annotation/mapping/image audit, protocol, split và frozen features |
| [taskb_xaa_dev](taskb_xaa_dev.ipynb) | 01_Development_XAA | 2. Baseline development ba seed; campaign gốc |
| [taskb_dvr_dev](taskb_dvr_dev.ipynb) | 02_Development_DVR_optimized | 3. MR/SR/Full DVR; import baseline hoàn tất có kiểm chứng |
| [taskb_final](taskb_final.ipynb) | 03_Final_Training_OfficialVal_optimized | 4. Khóa E* từ development, fresh heads trên official-train, 12 lượt official-val |
| [taskb_adapter_full](taskb_adapter_full.ipynb) | TME_Adapter_Full_Experiment | Nhánh riêng: development encoder+adapter từng seed → lock → final fresh → benchmark ghép cặp |
| [taskb_encoder_dev](taskb_encoder_dev.ipynb) | TME_Development | Nguồn duy nhất được giữ của Conventional-only seed42 đã reuse; có ablation TME lịch sử, không phải kết quả chính tuần45 |
| [taskb_adapter_dev](taskb_adapter_dev.ipynb) | Colab checked_v2_storagefix | Nguồn thực thi adapter seed42; giữ vì full experiment xác minh đúng legacy code/config/checkpoint này |
| [taskb_adapter_trial](taskb_adapter_trial.ipynb) | Adapter/Trial | Trial retrieval-only và alignment seed42, nguồn tạo cache và metadata cho adapter development lịch sử |
| [taskb_adapter_mr](taskb_adapter_mr.ipynb) | Adapter_MR/Pilot_va_Final | Sau Adapter full: pilot A/B/C/D → khóa epoch từ development → fresh MR → benchmark official-val ghép cặp |
| [taskb_demo](taskb_demo.ipynb) | Demo FAISS final | Sau khi có artifact final: truy vấn official-val hoặc nhập ảnh + mô tả mới trên Colab GPU |

Mở Colab GPU, mount Drive và chạy từ trên xuống. Preparation phải đạt đầy đủ trước development. XAA → DVR → final dùng nguồn baseline chỉ đọc ở campaign cũ. Adapter full mặc định preflight; chỉ bật `RUN_FULL_PIPELINE=True` ở cell cuối khi chủ động chạy đủ phase. Có thể chạy phase/seed bằng `CFG` và dispatcher; không chạy lại cell cấu hình khi lượt đang hoạt động. Resume giữ campaign/config/runtime và fingerprint, không reset hoặc sửa hash để vượt lỗi.

Ba notebook lịch sử phục vụ truy vết **artifact đã tồn tại**, không phải bước bắt buộc chạy lại mỗi lần. Encoder lịch sử còn cấu hình `conventional/no_alignment/full`; chỉ Conventional-only seed42 được reuse trong nhánh báo cáo. Adapter lịch sử tham chiếu trial cache/metadata trên Drive, không warm-start trọng số trial. Các notebook chính chứa implementation cần dùng; các path `/Users/...` và tên notebook cũ trong `SOURCE_RECORDS`/hash là bằng chứng provenance lịch sử, không phải đường dẫn cần tồn tại trên Colab. Giữ nguyên chúng để không thay hợp đồng thí nghiệm.

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

Hai XAA/DVR nội bộ cũ và output lịch sử có tại [Git history](https://github.com/tn4u/VisFit/tree/ce9727984bc4352174854858148b50846319e246/notebooks), khớp mã và output trong bộ bàn giao. Quy trình official-val dùng các notebook development/final ở bảng trên. Hai encoder week5 đã được thay bằng preparation. Các bản cũ vẫn có trong lịch sử Git.

Output/debug/widget/user metadata đã xóa; code/config khoa học giữ nguyên, riêng adapter full bỏ cell live probe/driver lỗi trùng và thêm opt-in cho driver thành công. Tổng hợp ngắn ở README thay cho output dài. [Nguồn và SHA](taskb_sources.json) lưu dấu vết trước dọn.

Lần rà soát chỉ kiểm tra JSON/nbformat, cú pháp IPython/Python, định nghĩa trước sử dụng ở cell top-level, tính tự chứa, liên kết/tên file, secret, kích thước và diff; tính lại thống kê adapter từ artifact. Không chạy training, benchmark hay nạp lại checkpoint GPU; chưa xác minh lại toàn bộ binary/shard trong lần này. Saved output và JSON completion là bằng chứng lịch sử, không thay kiểm tra runtime bắt buộc khi chạy lại.

## Dependency audit: clone repo có đủ để chạy từ đầu không?

**Đủ bộ code notebook cho hai quy trình báo cáo khi có các artifact đã khóa; chưa đủ để tái hiện độc lập chỉ bằng GitHub.** [Inventory dependency](taskb_artifacts.json) liệt kê path, SHA mong đợi và thư viện lấy trực tiếp từ code; đây không phải xác nhận mọi tài khoản đều truy cập được dữ liệu.

| Thành phần ngoài Git | Nơi lấy / cách tạo và giới hạn |
|---|---|
| FashionIQ ảnh + `cap.*.{train,val}.json`, `split.*.val.json` | Kaggle `binhhuunguyen/fashioniq`, preparation tự tải nếu thiếu. Annotation/ảnh phải khớp snapshot và audit; không thay bằng dataset khác chỉ cùng tên. |
| **`FashionIQ_Task_B_Experiment_Split.csv`** | `embeddings/text_features_taskb/` dưới root Drive chung; SHA `9e9680556bd26348f29f5f529e765dfebb78d1c1d85f404c95bb6db6bac8da13`. Đây là đầu vào bắt buộc của `development_views()`, không chỉ file đối chiếu. Kaggle không cung cấp nhãn split nội bộ này; cần xin đúng bản từ chủ artifact. Không tự tạo split khác rồi sửa SHA. |
| Preparation package | `taskb_prepare` tạo protocol/config/audit, development/official manifests, feature views, mapping/index và shards. XAA/DVR/adapter kiểm SHA cụ thể của package. Tạo lại với runtime/preprocessing khác có thể đổi contract/SHA và bị từ chối; một lượt mới không mặc nhiên tương đương snapshot báo cáo. |
| XAA baseline development | `taskb_xaa_dev` tạo ba seed trong campaign gốc. `taskb_dvr_dev` import kết quả này chỉ đọc; `taskb_final` cần đủ baseline và DVR curves trước khi khóa E*=8. |
| Legacy Conventional-only seed42 | `tme_development/FashionIQ/tme_dev_v1_seed42`: `conventional/{config.json,best.pt,last.pt,best.json,last.json,metric_history.json,epoch_*_per_query.csv}` và metadata/manifests của run. `taskb_encoder_dev` là nguồn lịch sử, không bảo đảm chạy mới sẽ sinh lại đúng byte checkpoint/JSON đã khóa. |
| Legacy adapter seed42 | `retrieval_only_dev_v1_base42_adapter42_checked_v2_storagefix`: training config, best/last checkpoint + markers, history, epoch/query/Top-K/verification outputs. **`taskb_adapter_full` luôn import seed42**, kể cả preflight; không có nhánh fallback train lại seed42 khi thiếu snapshot. Cần xin bộ artifact được khóa từ chủ sở hữu. |
| Trial metadata/cache của adapter dev lịch sử | `tme_adapter_trial/FashionIQ/adapter_trial_v1_seed42`; `taskb_adapter_dev` kiểm `TRIAL_ARTIFACT_LOCKS`, gồm trial request/config/provenance/audit, baseline/retrieval results và index cache. Đây là dependency thật dù không warm-start trọng số trial. Notebook trial lưu mã tạo artifact. Để dùng lại snapshot, cần bản đã khóa từ Drive và giữ nguyên checksum. |
| Final checkpoint, lock, summary/query/Top-K | Các campaign Drive ở trên; chạy các phase đúng thứ tự để tạo trong môi trường tương thích. Không dùng số trong README thay artifact. Encoder/feature cache lớn không đưa vào Git. |

Thư viện cài từ các cell bootstrap/stdlib và môi trường Colab; không cần script Python nội bộ bị bỏ sót hay import `.ipynb` khác. Một số runtime được khóa đúng torch/CUDA và SDK; không tự nâng cấp để vượt kiểm tra. `requirements.txt` ở root phục vụ project chung, không thay bootstrap riêng của thí nghiệm.

Artifact Drive là dữ liệu của tài khoản chủ sở hữu, không được coi là công khai chỉ vì có URL. Liên hệ chủ artifact để cấp quyền hoặc cung cấp bản được phép chia sẻ; lần audit này không mở quyền, không đưa CSV annotation/manifest, dataset, credential hoặc checkpoint lên Git. Repo chứa config, schema/hàm sinh manifest và expected SHA; bản payload nhỏ nằm trên Drive vẫn cần quyền truy cập và điều kiện phân phối phù hợp.

Rà soát Git sau sắp xếp: các notebook Task B chỉ còn trên branch encoder cũ là hai week5 đã thay bằng preparation; không có notebook tuần44/45 mới bị bỏ quên ở worktree khác. Các notebook Task A khác trên branch lịch sử không nhập vào đây. Các bản adapter development chưa chạy trong Downloads không thay nguồn storagefix đã xác minh. Không có notebook SOTA riêng cần nhập trong các nguồn được kiểm kê; đối chiếu công bố vẫn thuộc báo cáo, không phải benchmark đã tái lập.

## Adapter + MR và demo FAISS

- **Adapter + MR.** Sau khi có Adapter full, chạy cấu hình, bootstrap và định nghĩa. Kiểm tra nguồn pilot theo seed trước khi bật pilot validation. Pilot dùng development, final khóa 1 epoch từ pilot rồi học MR với encoder và Adapter final đúng seed đóng băng. Final cần lock của Adapter full và đủ ba seed trước benchmark ghép cặp. Khi chỉ truy vết, giữ các cờ training tắt. Artifact nằm trong `adapter_mr_pilot/FashionIQ/` và `adapter_mr_final/FashionIQ/adapter_mr_final_v1` dưới root Drive chung. Mean official-val của Adapter + MR là 37,121802 ± 0,252124%, chênh ghép cặp +0,046982 ± 0,078133 điểm phần trăm so với Adapter qua ba seed.
- **Demo.** Trên Colab GPU, chạy cấu hình → bootstrap/Drive → định nghĩa → setup → giao diện. Mặc định dùng Adapter final seed42, có thêm Conventional-only, XAA, XAA + DVR-MR và Adapter + MR khi đủ artifact. Chế độ benchmark dùng query/gallery official-val và ground truth. Chế độ ảnh + mô tả chạy preprocessing và encoder thật cho đầu vào mới. Setup mặc định bật `run_full_validation` để đối chiếu toàn bộ query. Tắt cờ này khi chỉ cần mở giao diện.
- **Nguồn artifact.** [Index FAISS và biên bản xác minh](https://drive.google.com/drive/folders/1C0fqSko740joXZ5yNoqUvUJ8HPd2Irvo) ở `taskb_demo/faiss_flatip_v1` dưới root Drive chung. Demo cần preparation, FashionIQ, checkpoint và encoder final theo mô hình, cùng IndexFlatIP theo category và mapping/contract/SHA tương ứng. Xem [staging bàn giao](https://drive.google.com/drive/folders/1_qxu1mlktaGwiHa3c9SZ7nMHvjTMd_Zl) và `Mo_hinh/_Dung_chung/manifest.json` trong bộ bàn giao để tra artifact và checksum. Liên hệ chủ sở hữu nếu thiếu quyền. Dataset, ảnh, checkpoint, feature cache, FAISS index và báo cáo Word nằm ngoài Git.
- **Giới hạn kiểm tra.** Đợt đưa lên Git đối chiếu mã, JSON, cấu trúc notebook, cú pháp và liên kết nội bộ. Biên bản Colab T4 trước đây bao phủ 6.016 query official-val cho mỗi mô hình seed42 và kiểm tra cả truy vấn ảnh + mô tả mới. Không chạy lại training, inference hoặc benchmark trong đợt này. Output đã lưu và log đầy đủ ở bộ bàn giao/Drive.
