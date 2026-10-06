from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import CLIPModel, CLIPProcessor


MODEL_NAME = "patrickjohncyh/fashion-clip"


class BranchAModel:
    def __init__(self, checkpoint_path: str | Path, device=None):
        self.checkpoint_path = Path(checkpoint_path)

        if not self.checkpoint_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy checkpoint: {self.checkpoint_path}"
            )

        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.processor = CLIPProcessor.from_pretrained(
            MODEL_NAME
        )

        self.model = CLIPModel.from_pretrained(
            MODEL_NAME
        )

        checkpoint = torch.load(
            self.checkpoint_path,
            map_location=self.device,
            weights_only=False
        )

        if "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
        else:
            state_dict = checkpoint

        self.model.load_state_dict(
            state_dict
        )

        self.model.to(
            self.device
        )

        self.model.eval()

    @torch.inference_mode()
    def encode_image(self, image):
        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        pixel_values = inputs[
            "pixel_values"
        ].to(
            self.device
        )

        raw_output = self.model.get_image_features(
            pixel_values=pixel_values
        )

        if isinstance(
            raw_output,
            torch.Tensor
        ):
            embedding = raw_output

        elif (
            hasattr(raw_output, "image_embeds")
            and raw_output.image_embeds is not None
        ):
            embedding = raw_output.image_embeds

        elif (
            hasattr(raw_output, "pooler_output")
            and raw_output.pooler_output is not None
        ):
            embedding = raw_output.pooler_output

        elif (
            hasattr(raw_output, "last_hidden_state")
            and raw_output.last_hidden_state is not None
        ):
            embedding = (
                raw_output.last_hidden_state[:, 0, :]
            )

        else:
            raise TypeError(
                f"Không hỗ trợ output type: {type(raw_output)}"
            )

        expected_dim = (
            self.model.config.projection_dim
        )

        if (
            embedding.shape[-1]
            != expected_dim
        ):
            embedding = (
                self.model.visual_projection(
                    embedding
                )
            )

        embedding = F.normalize(
            embedding,
            p=2,
            dim=-1
        )

        embedding = (
            embedding
            .cpu()
            .numpy()
            .astype("float32")
        )

        return embedding