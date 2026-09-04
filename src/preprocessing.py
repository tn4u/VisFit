import pandas as pd
import re
import os
import numpy as np

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_deepfashion_multimodal(file_path, output_dir):
    print(f"Đang đọc dữ liệu từ: {file_path}...")
    df = pd.read_csv(file_path)
    
    print("Đang làm sạch văn bản...")
    df['clean_caption'] = df['caption'].apply(clean_text)
    
    df['category'] = df['gender'] + "_" + df['product_type']
    
    df['dataset_source'] = 'DeepFashion-MultiModal'
    
    schema_cols = ['image_id', 'product_id', 'dataset_source', 'category', 'clean_caption', 'path']
    df_final = df[schema_cols]
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "df_multimodal_visfit_schema.csv")
    df_final.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Hoàn tất! File đã chuẩn hóa được lưu tại: {output_path}")
    print("\n--- Mẫu dữ liệu sau khi chuẩn hóa ---")
    print(df_final[['image_id', 'product_id', 'category', 'clean_caption']].head())

def create_query_gallery_split(input_csv, output_csv, num_queries=1000, random_seed=42):
    print(f"Đang đọc dữ liệu từ: {input_csv}")
    df = pd.read_csv(input_csv)
    product_counts = df['product_id'].value_counts()
    
    df['partition'] = 'gallery'

    valid_products = product_counts[product_counts >= 2].index
    print(f"Số lượng sản phẩm hợp lệ (>= 2 ảnh): {len(valid_products)}")

    np.random.seed(random_seed)
    actual_query_size = min(num_queries, len(valid_products))
    query_products = np.random.choice(valid_products, size=actual_query_size, replace=False)

    query_indices = []
    for pid in query_products:
        product_rows = df[df['product_id'] == pid]
        chosen_idx = np.random.choice(product_rows.index)
        query_indices.append(chosen_idx)

    df.loc[query_indices, 'partition'] = 'query'

    print("\n--- Phân bố tập dữ liệu ---")
    print(df['partition'].value_counts())

    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"\nĐã xuất file phân chia Query/Gallery: {output_csv}")

def clean_text_fashion_iq(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_fashion_iq(input_csv, output_csv):
    print(f"Đang đọc dữ liệu FashionIQ từ: {input_csv}...")
    df = pd.read_csv(input_csv)
    
    print("Đang làm sạch text...")
    df['clean_caption'] = df['caption'].apply(clean_text_fashion_iq)
    
    df['partition'] = df['source_file'].apply(
        lambda x: 'train' if 'train' in str(x).lower() else ('val' if 'val' in str(x).lower() else 'test')
    )
    
    df['dataset_source'] = 'FashionIQ'
    
    schema_cols = ['candidate', 'target', 'dataset_source', 'category', 'clean_caption', 'partition']
    df_final = df[schema_cols]
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_final.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"\nHoàn tất! File chuẩn hóa đã lưu tại: {output_csv}")
    print("\n--- Mẫu dữ liệu sau khi chuẩn hóa ---")
    print(df_final[['candidate', 'target', 'clean_caption', 'partition']].head(3).to_string())
    print("\n--- Phân bố tập dữ liệu ---")
    print(df_final['partition'].value_counts())

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    INPUT_FILE_FIQ = os.path.join(BASE_DIR, "data/raw/FashionIQ/FashionIQ_cleaned_metadata.csv")
    OUTPUT_FILE_FIQ = os.path.join(BASE_DIR, "data/processed/metadata/df_fashioniq_schema.csv")
    process_fashion_iq(INPUT_FILE_FIQ, OUTPUT_FILE_FIQ)

    INPUT_FILE_DF_RAW = os.path.join(BASE_DIR, "data/raw/DeepFashion-MultiModal/DeepFashion Labels Front_cleaned.csv")
    OUTPUT_DIR_DF = os.path.join(BASE_DIR, "data/processed/metadata")
    process_deepfashion_multimodal(INPUT_FILE_DF_RAW, OUTPUT_DIR_DF)

    INPUT_FILE_DF_SCHEMA = os.path.join(BASE_DIR, "data/processed/metadata/df_multimodal_visfit_schema.csv")
    OUTPUT_FILE_SPLIT = os.path.join(BASE_DIR, "data/processed/metadata/df_multimodal_query_gallery.csv")
    create_query_gallery_split(INPUT_FILE_DF_SCHEMA, OUTPUT_FILE_SPLIT)