import pandas as pd
import re
import os

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

if __name__ == "__main__":
    # Thay đổi đường dẫn tương ứng với máy local của Tuấn
    INPUT_FILE = "data/raw/DeepFashion-MultiModal/DeepFashion Labels Front_cleaned.csv"
    OUTPUT_DIR = "data/processed/metadata/"
    
    process_deepfashion_multimodal(INPUT_FILE, OUTPUT_DIR)