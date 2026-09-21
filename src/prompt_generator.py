import os
import re
import pandas as pd

# ===== CHINH DUONG DAN O DAY =====
GT_DIR = "data/processed/ground_truth_text"                       # thu muc output cua notebook Ground_Truth
DF_INPUT = os.path.join(GT_DIR, "mapping_full.csv")               # 12.694 anh, co cot caption
DF_OUTPUT = "data/processed/metadata/df_multimodal_prompts.csv"   # file moi, khong ghi de file cu
CLIP_TEMPLATE = "a photo of a {cat}, {cap}"                       # doi template o day neu can
# =================================

REQUIRED_COLS = ["image_id", "item_id", "gender", "category", "view", "split",
                 "row_in_captions", "caption"]


def clean_text(text):
    """Giu nguyen ham lam sach cua pipeline truoc (chu thuong, chi giu chu cai)."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def generate_dual_prompts(input_path, output_path):
    print("--- SINH PROMPT CHO TEXT-ONLY VA FASHION-CLIP ---")
    df = pd.read_csv(input_path)

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    assert not missing, f"Thieu cot trong {input_path}: {missing}"
    assert df["image_id"].is_unique, "image_id bi trung"

    # Thu tu dong cua file nay quyet dinh thu tu dong cua vector (.npy): sap theo row_in_captions
    df = df.sort_values("row_in_captions").reset_index(drop=True)
    df["vec_row"] = range(len(df))

    # Lam sach caption (cung ham clean_text nhu truoc)
    df["clean_caption"] = df["caption"].apply(clean_text)
    assert (df["clean_caption"] != "").all(), "Co caption rong sau khi lam sach"

    # Giu dinh nghia category cu (gender_producttype, vi du MEN_Denim); giu them product_type goc
    df["product_type"] = df["category"]
    df["category"] = df["gender"] + "_" + df["product_type"]

    # 1. Dành cho nhóm Text-only (SBERT, TF-IDF, FastText): giữ nguyên bản chất mô tả văn bản
    df["text_only_input"] = df["clean_caption"]

    # 2. Dành cho nhóm Fashion-CLIP: thêm template câu ngữ cảnh hình ảnh
    def make_clip_prompt(row):
        cat = str(row["category"]).replace("_", " ").lower()
        cap = str(row["clean_caption"])
        return CLIP_TEMPLATE.format(cat=cat, cap=cap)

    df["fashion_clip_prompt"] = df.apply(make_clip_prompt, axis=1)

    cols = ["vec_row", "image_id", "item_id", "split", "view", "gender", "product_type",
            "category", "row_in_captions", "caption", "clean_caption",
            "text_only_input", "fashion_clip_prompt"]
    df = df[cols]

    # Kiem tra do dai prompt: CLIP text encoder chi nhan toi da 77 token
    n_words = df["fashion_clip_prompt"].str.split().str.len()
    print(f"So dong: {len(df)}")
    print(f"Do dai fashion_clip_prompt (so tu): trung binh {n_words.mean():.1f}, toi da {n_words.max()}")
    print(f"Prompt > 60 tu: {(n_words > 60).sum()} ({(n_words > 60).mean():.1%}) | > 70 tu: {(n_words > 70).sum()} ({(n_words > 70).mean():.1%})")

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Da xuat file chua day du prompt cho ca 2 nhom mo hinh: {output_path}")
    print("Luu y: vector (.npy) phai duoc trich theo dung thu tu dong cua file nay (cot vec_row).")


if __name__ == "__main__":
    generate_dual_prompts(DF_INPUT, DF_OUTPUT)