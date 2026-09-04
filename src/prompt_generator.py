import pandas as pd
import os

def generate_dual_prompts(input_path, output_path):
    print("--- SINH PROMPT CHO TEXT-ONLY VÀ FASHION-CLIP ---")
    df = pd.read_csv(input_path)
    
    # 1. Dành cho nhóm Text-only (SBERT, TF-IDF, FastText): Giữ nguyên bản chất mô tả văn bản
    df['text_only_input'] = df['clean_caption']
    
    # 2. Dành cho nhóm Fashion-CLIP: Thêm template câu ngữ cảnh hình ảnh
    def make_clip_prompt(row):
        cat = str(row['category']).replace('_', ' ').lower()
        cap = str(row['clean_caption'])
        return f"a photo of a {cat}, {cap}"
    
    df['fashion_clip_prompt'] = df.apply(make_clip_prompt, axis=1)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Da xuat file chua day du prompt cho ca 2 nhom mo hinh: {output_path}")

if __name__ == "__main__":
    DF_INPUT = "data/processed/metadata/df_multimodal_query_gallery.csv"
    DF_OUTPUT = "data/processed/metadata/df_multimodal_prompts.csv"
    
    generate_dual_prompts(DF_INPUT, DF_OUTPUT)