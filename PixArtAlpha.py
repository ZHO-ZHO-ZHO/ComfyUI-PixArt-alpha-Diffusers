import torch
import os
import folder_paths
from diffusers import PixArtAlphaPipeline, DPMSolverMultistepScheduler
from huggingface_hub import hf_hub_download
import numpy as np
from .sa_solver_diffusers import SASolverScheduler
from .style_template import style_list


device = "cuda" if torch.cuda.is_available() else "cpu"


# Create a dictionary from style_list for easier access
styles = {style['name']: (style['prompt'], style['negative_prompt']) for style in style_list}

STYLE_NAMES = [style['name'] for style in style_list]
DEFAULT_STYLE_NAME = "(No style)"

def apply_style(style_name: str, positive: str, negative: str = "") -> tuple[str, str]:
    # Get the prompts for the given style_name, or defaults to the first style if not found
    p, n = styles.get(style_name, styles[DEFAULT_STYLE_NAME])
    return p.replace("{prompt}", positive), n + ' ' + negative


class PA_Styler_Zho:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "A alpaca made of colorful building blocks, cyberpunk", "multiline": True}),
                "negative_prompt": ("STRING", {"default": "asymmetry, worst quality, low quality", "multiline": True}),
                "style_name": (STYLE_NAMES, {"default": DEFAULT_STYLE_NAME})
            }
        }

    RETURN_TYPES = ('STRING', 'STRING',)
    RETURN_NAMES = ('positive_prompt', 'negative_prompt',)
    FUNCTION = "prompt_style"
    CATEGORY = "🖼️PixArtAlpha"

    def prompt_style(self, style_name, prompt, negative_prompt):
        prompt, negative_prompt = apply_style(style_name, prompt, negative_prompt)
        
        return prompt, negative_prompt


class PA_BaseModelLoader_fromhub_Zho:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_model_path": ("STRING", {"default": "PixArt-alpha/PixArt-XL-2-1024-MS"})
            }
        }

    RETURN_TYPES = ("PAMODEL",)
    RETURN_NAMES = ("pipe",)
    FUNCTION = "load_model"
    CATEGORY = "🖼️PixArtAlpha"
  
    def load_model(self, base_model_path):
        pipe = PixArtAlphaPipeline.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16,
        ).to(device)
        return [pipe]


class PA_Generation_Zho:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("PAMODEL",),
                "positive": ("STRING", {"multiline": True, "forceInput": True}),
                "negative": ("STRING", {"multiline": True, "forceInput": True}),
                "width": ("INT", {"default": 1024, "min": 512, "max": 2048, "step": 32}),
                "height": ("INT", {"default": 1024, "min": 512, "max": 2048, "step": 32}), 
                "steps": ("INT", {"default": 20, "min": 1, "max": 100, "step": 1}),
                "guidance_scale": ("FLOAT", {"default": 4.5, "min": 0, "max": 20}),
                "schedule": (["DPM-Solver", "SA-Solver"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "🖼️PixArtAlpha"
                       
    def generate_image(self, positive, negative, pipe, steps, guidance_scale, seed, width, height, schedule):

        if schedule == 'DPM-Solver':
            if not isinstance(pipe.scheduler, DPMSolverMultistepScheduler):
                pipe.scheduler = DPMSolverMultistepScheduler()
        elif schedule == "SA-Solver":
            if not isinstance(pipe.scheduler, SASolverScheduler):
                pipe.scheduler = SASolverScheduler.from_config(pipe.scheduler.config, algorithm_type='data_prediction', tau_func=lambda t: 1 if 200 <= t <= 800 else 0, predictor_order=2, corrector_order=2)
        else:
            raise ValueError(f"Unknown schedule: {schedule}")
        
        generator = torch.Generator(device=device).manual_seed(seed)

        output = pipe(
            prompt=positive,
            negative_prompt=negative,
            num_inference_steps=steps,
            generator=generator,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            )
      
        # 检查输出类型并相应处理
        if isinstance(output, tuple):
            # 当返回的是元组时，第一个元素是图像列表
            images_list = output[0]
        else:
            # 如果返回的是 StableDiffusionXLPipelineOutput，需要从中提取图像
            images_list = output.images

        # 转换图像为 torch.Tensor，并调整维度顺序为 NHWC
        images_tensors = []
        for img in images_list:
            # 将 PIL.Image 转换为 numpy.ndarray
            img_array = np.array(img)
            # 转换 numpy.ndarray 为 torch.Tensor
            img_tensor = torch.from_numpy(img_array).float() / 255.
            # 转换图像格式为 CHW (如果需要)
            if img_tensor.ndim == 3 and img_tensor.shape[-1] == 3:
                img_tensor = img_tensor.permute(2, 0, 1)
            # 添加批次维度并转换为 NHWC
            img_tensor = img_tensor.unsqueeze(0).permute(0, 2, 3, 1)
            images_tensors.append(img_tensor)

        if len(images_tensors) > 1:
            output_image = torch.cat(images_tensors, dim=0)
        else:
            output_image = images_tensors[0]

        return (output_image,)


NODE_CLASS_MAPPINGS = {
    "PA_Styler_Zho": PA_Styler_Zho,
    "PA_BaseModelLoader_fromhub_Zho": PA_BaseModelLoader_fromhub_Zho,
    "PA_Generation_Zho": PA_Generation_Zho
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PA_Styler_Zho": "🖼️PixArtAlpha Styler",
    "PA_BaseModelLoader_fromhub_Zho": "🖼️PixArtAlpha ModelLoader",
    "PA_Generation_Zho": "🖼️PixArtAlpha Generation"
}
