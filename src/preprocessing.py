import pandas as pd
import re
import os
import numpy as np

def clean_text(text):
    """Hàm làm sạch văn bản bằng Regex"""
    if not isinstance(text, str):
        return ""
    # Chuyển về chữ thường
    text = text.lower()
    # Loại bỏ ký tự đặc biệt (dấu chấm, phẩy, than, hỏi...), chỉ giữ lại chữ cái và khoảng trắng
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Xóa khoảng trắng kép/thừa
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_deepfashion_multimodal(file_path, output_dir):
    print(f"Đang đọc dữ liệu từ: {file_path}...")
    # 1. Đọc file CSV của DeepFashion
    df = pd.read_csv(file_path)
    
    # 2. Xử lý làm sạch câu mô tả (caption)
    print("Đang làm sạch văn bản...")
    df['clean_caption'] = df['caption'].apply(clean_text)
    
    # 3. Tạo Category chung (ghép từ Gender và Product Type)
    # Ví dụ: MEN + Denim -> MEN_Denim
    df['category'] = df['gender'] + "_" + df['product_type']
    
    # 4. Đánh dấu nguồn dữ liệu
    df['dataset_source'] = 'DeepFashion-MultiModal'
    
    # 5. Lọc và chuẩn hóa theo Schema chung của dự án VisFit
    # Chữ lại cột 'product_id' vì nó rất quan trọng để map với tập In-shop Benchmark
    schema_cols = ['image_id', 'product_id', 'dataset_source', 'category', 'clean_caption', 'path']
    df_final = df[schema_cols]
    
    # 6. Xuất ra thư mục processed
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "df_multimodal_visfit_schema.csv")
    df_final.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Hoàn tất! File đã chuẩn hóa được lưu tại: {output_path}")
    print("\n--- Mẫu dữ liệu sau khi chuẩn hóa ---")
    print(df_final[['image_id', 'product_id', 'category', 'clean_caption']].head())

def create_query_gallery_split(input_csv, output_csv, num_queries=1000, random_seed=42):
    """
    Phân chia tập dữ liệu thành Query và Gallery dựa trên product_id.
    """
    print(f"Đang đọc dữ liệu từ: {input_csv}")
    df = pd.read_csv(input_csv)

    # Đếm số lượng ảnh của mỗi sản phẩm
    product_counts = df['product_id'].value_counts()
    
    # Khởi tạo toàn bộ là gallery
    df['partition'] = 'gallery'

    # Lọc các sản phẩm hợp lệ (có >= 2 ảnh)
    valid_products = product_counts[product_counts >= 2].index
    print(f"Số lượng sản phẩm hợp lệ (>= 2 ảnh): {len(valid_products)}")

    # Chọn ngẫu nhiên sản phẩm làm Query
    np.random.seed(random_seed)
    actual_query_size = min(num_queries, len(valid_products))
    query_products = np.random.choice(valid_products, size=actual_query_size, replace=False)

    # Gắn nhãn query
    query_indices = []
    for pid in query_products:
        product_rows = df[df['product_id'] == pid]
        chosen_idx = np.random.choice(product_rows.index)
        query_indices.append(chosen_idx)

    df.loc[query_indices, 'partition'] = 'query'

    print("\n--- Phân bố tập dữ liệu ---")
    print(df['partition'].value_counts())

    # Lưu file với tên chuẩn hóa theo công việc
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"\n✅ Đã xuất file phân chia Query/Gallery: {output_csv}")

if __name__ == "__main__":
    # Đường dẫn file đầu vào (kết quả sau khi clean text)
    INPUT_FILE = "data/processed/metadata/df_multimodal_visfit_schema.csv"
    
    # Đường dẫn file đầu ra (đặt tên theo công việc: tạo tập Query/Gallery)
    OUTPUT_FILE = "data/processed/metadata/df_multimodal_query_gallery.csv"
    
    create_query_gallery_split(INPUT_FILE, OUTPUT_FILE)

if __name__ == "__main__":
    # Thay đổi đường dẫn tương ứng với máy local của Tuấn
    INPUT_FILE = "data/raw/DeepFashion-MultiModal/DeepFashion Labels Front_cleaned.csv"
    OUTPUT_DIR = "data/processed/metadata/"
    
    process_deepfashion_multimodal(INPUT_FILE, OUTPUT_DIR)