
![PA封面图](https://github.com/ZHO-ZHO-ZHO/ComfyUI-PixArt-alpha-Diffusers/assets/140084057/cd5f98a2-baa4-4825-8dd9-132559f7dc04)


# ComfyUI-PixArt-alpha-Diffusers

Unofficial implementation of [PixArt-alpha-Diffusers](https://github.com/PixArt-alpha/PixArt-alpha) for ComfyUI


![Dingtalk_20240308214927](https://github.com/ZHO-ZHO-ZHO/ComfyUI-PixArt-alpha-Diffusers/assets/140084057/af92fd3e-88ab-4d25-872a-bafdabd8f164)


## 项目介绍 | Info

- 来自对[PixArt-alpha-Diffusers](https://github.com/PixArt-alpha/PixArt-alpha)的非官方实现，由于原本支持 PixArt-α 的 [ComfyUI_ExtraModels](https://github.com/city96/ComfyUI_ExtraModels) 插件年久失修暂时无法与新版 ComfyUI 兼容，所以特意做了这版供大家使用
  
- 版本：V1.0 支持自动下载模型（模型很大，C盘空间警告！），支持通用styler


## 节点说明 | Features

- 基础模型加载 | 🖼️PixArtAlpha ModelLoader
    - 支持从 huggingface hub 自动下载模型，输入模型名称（如：PixArt-alpha/PixArt-XL-2-1024-MS）即可

 - 提示词 + 风格 | 🖼️PixArtAlpha Styler
    - 与各种提示词（文本）输入（如肖像大师等）、styler、 Photomaker Prompt_Styler 兼容
    - prompt、negative：正负提示词
    - style_name：支持官方提供的10种风格
        - (No style)
        - Cinematic
        - Photographic
        - Anime
        - Manga
        - Digital Art
        - Pixel art
        - Fantasy art
        - Neonpunk
        - 3D Model

- InstantID 生成 | 🖼️PixArtAlpha Generation
    - pipe：接入模型
    - positivet、negative：正负提示词
    - width、height：宽度、高度
    - step：步数，官方默认20-25步
    - guidance_scale：提示词相关度，DPM-Solver默认为4.5，SA-Solver默认为3
    - schedule：2种调度器，DPM-Solver 和 SA-Solver
    - seed：种子


## 安装 | Install


- 推荐使用管理器 ComfyUI Manager 安装（On the Way）


- 手动安装：
    1. `cd custom_nodes`
    2. `git clone https://github.com/ZHO-ZHO-ZHO/ComfyUI-PixArt-alpha-Diffusers.git`
    3. `cd custom_nodes/ComfyUI-PixArt-alpha-Diffusers`
    4. `pip install -r requirements.txt`
    5. 重启 ComfyUI

  
## 工作流 | Workflows

V1.0

- [V1.0 PixArtAlpha Standard](https://github.com/ZHO-ZHO-ZHO/ComfyUI-PixArt-alpha-Diffusers/blob/main/PixArtAlpha%20Workflows/PixArtAlpha%20Standard%E3%80%90Zho%E3%80%91.json)

  ![Dingtalk_20240308211946](https://github.com/ZHO-ZHO-ZHO/ComfyUI-PixArt-alpha-Diffusers/assets/140084057/d372554e-bb5b-4f34-9480-47d4629c8a96)


## 更新日志

- 20240308

  V1.0 上线：支持自动下载模型（模型很大，C盘空间警告！），支持通用styler，支持10种风格

  创建项目



## Stars 

[![Star History Chart](https://api.star-history.com/svg?repos=ZHO-ZHO-ZHO/ComfyUI-PixArt-alpha-Diffusers&type=Date)](https://star-history.com/#ZHO-ZHO-ZHO/ComfyUI-PixArt-alpha-Diffusers&Date)


## 关于我 | About me

📬 **联系我**：
- 邮箱：zhozho3965@gmail.com
- QQ 群：839821928

🔗 **社交媒体**：
- 个人页：[-Zho-](https://jike.city/zho)
- Bilibili：[我的B站主页](https://space.bilibili.com/484366804)
- X（Twitter）：[我的Twitter](https://twitter.com/ZHOZHO672070)
- 小红书：[我的小红书主页](https://www.xiaohongshu.com/user/profile/63f11530000000001001e0c8?xhsshare=CopyLink&appuid=63f11530000000001001e0c8&apptime=1690528872)

💡 **支持我**：
- B站：[B站充电](https://space.bilibili.com/484366804)
- 爱发电：[为我充电](https://afdian.net/a/ZHOZHO)


## Credits

[PixArt-alpha-Diffusers](https://github.com/PixArt-alpha/PixArt-alpha)
