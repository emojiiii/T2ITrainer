# T2ITrainer
T2ITrainer is still under development stage and not stable yet. \
It updates very frequently, please check the change logs for details.

## Prerequisites
- PyTorch version >= 2.3.0 with CUDA 12.1 support (`torch>=2.3.0+cu121`).

## Supported Training Configurations
- For Lora training: Supports kolors, sd3, and hunyuandit 1.1.
  - **Hardware requirements:**
    - CUDA GPU with >13GB memory for hunyuandit lora training.
    - CUDA GPU with 11GB memory for kolors training.

## Installation
### 0. Microsoft Visual C++ Redistributable latest supported downloads
Please install Microsoft Visual C++ Redistributable if you have the following error: \
0SError:[WinError 126] ... Error loading "...\Lib\site-packages\torch\lib\fbgemm dl1" or one of its dependencies. \
https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170

### 1. Setup environment using setup.bat:
setup.bat include 5 steps: 
- Step 1. Setup venv (optional)
- Step 2. Upgrade pip
- Step 3. Install torch (auto,optional) if setup venv install torch automatically.
- Step 4. Install other dependencies from requirements.txt
- Step 5. Download the Model Files (optional)
```
git clone https://github.com/lrzjason/T2ITrainer.git
cd T2ITrainer
setup.bat
```
Goto point 2 after setup.bat

### 1. Setup environment manually (optional):
Clone repository
```
git clone https://github.com/lrzjason/T2ITrainer.git
cd T2ITrainer
```
Create virtual environment if you want:
```
python -m venv venv
call venv\Scripts\activate
```
If created virtual environment, install pytorch from https://pytorch.org/get-started/locally/
(Recommanded Torch version >= 2.3.0+cu121)
Example:
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
Install dependencies:
```
pip install -r requirements.txt
```

### 2. Run the script:
- PS: Kolors' original vae in fp16 would cause training error and produce black image when inference.
- Please download the fp16 fix vae from https://huggingface.co/madebyollin/sdxl-vae-fp16-fix
- sdxl.vae.safetensors or sdxl_vae.safetensors and use one of them in vae_path option
```
python ui.py
```

### 3. Testing:
- For kolors:
  Install plugins from:
  - [ComfyUI-KwaiKolorsWrapper](https://github.com/kijai/ComfyUI-KwaiKolorsWrapper)
  - [ComfyUI-Kolors-MZ](https://github.com/MinusZoneAI/ComfyUI-Kolors-MZ)
  
  Then use the normal lora loader in ComfyUI.
<!-- 
- For hunyuandit 1.1:
  Modify `test.py` with `output_dir`, `lora_dir_name`, and prompt to generate images with lora.
  ```
  python test.py
  ``` -->

## Kolors Merging SDXL Checkpoint

### **!!! Important !!!**
After merging, note that it may not effectively transfer knowledge from SDXL checkpoint to Kolors. It might just add random noise and reverse some overfitting.

- **Hardware requirements:**
  Requires 20GB+ RAM for model merging.

Please activate your virtual environment if needed.

### 1. Install dependencies:
```
git clone https://github.com/lrzjason/T2ITrainer.git
cd T2ITrainer
pip install -r requirements.txt
```

### 2. Run the script:
```
python ui_for_merge.py
```

### 3. Testing:
As of 2024-07-08, Kolors inference is limited. Refer to [ComfyUI-KwaiKolorsWrapper](https://github.com/kijai/ComfyUI-KwaiKolorsWrapper) for testing.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=lrzjason/T2ITrainer&type=Date)](https://star-history.com/#lrzjason/T2ITrainer&Date)

## Change Logs:
- **2024-06-17:** Initial UI release.
- **2024-06-25:** Updated hunyuandit lora training script and UI for multiple training scripts.
- **2024-06-27:** Fixed incorrect bucketing in hunyuandit lora training and added cache recreation option in UI.
- **2024-07-06:** Fixed RGB to BGR channel issue in sd3 latent.
- **2024-07-08:** Added `merge_state_dict.py` for merging Kolors and SDXL state dicts, saving as Kolors unet.
- **2024-07-11:** Added Kolors training script to UI.
- **2024-07-11:(2)** Added resume from checkpoint
- **2024-07-13:** Remove some unused dependencies
- **2024-07-13:(2)** Fix bugs on saved lora, added prefix to keys
- **2024-07-14:** Avoid loading text encoder unnecessarily after cached latent
- **2024-07-15:** Added setup.bat for windows users
- **2024-07-16:** Added save and load config.json
- **2024-07-19:** Fix model_path couldn't load the weight
- **2024-07-20:** Adjust cache logic and fix caching bug. Please recreate cache after this update.
- **2024-07-20:(2)** Add 2048 resolution, it could choose 1024, 2048 training based resolution now. It only recommanded to train 2048 resolution when you have >= 24GB vram.
- **2024-07-21:** Update debiased estimation loss and change cache resize from default to area
- **2024-07-22:** Fix when batch_size > 1, debiased estimation loss would cause error.
- **2024-07-22:(2)**  Thanks emojiiii for linux setup.sh script and related updates.
- **2024-07-28:**  Update caching logic, automatically update cache when added or deleted files.
- **2024-08-04:**  Add kolors slider training code and image generation code


## Acknowledgements:
- Thanks to minienglish1 and Freon in EveryDream Discord for the assistance.
- Special thanks to kohya ss for references from the training codebase.
- Thanks to Kblueleaf for coding reference on hunyuandit gradient checkpoint implementation.
- Thanks to Kolors for the open-source checkpoint.
- Thanks to comfyui for the wonderful codebase.
- Thanks to emojiiii for the setup.bat script and other updates.
- Thanks to Rohit Gandikota and related authors of Concept Sliders https://github.com/rohitgandikota/sliders
