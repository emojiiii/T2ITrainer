import gradio as gr

import subprocess
import json
import sys

default_config = {
    "default_script": "train_kolors_lora_ui.py",
    "script_choices": ["train_kolors_lora_ui.py","train_hunyuan_lora_ui.py","train_sd3_lora_ui.py"],
	# "output_dir":"F:/models/sd3",
    # "save_name":"opensd3-b4",
    # "pretrained_model_name_or_path":"stabilityai/stable-diffusion-3-medium-diffusers", 
    # "train_data_dir":"F:/ImageSet/sd3_test", 
	# "output_dir":"F:/models/hy",
    # "save_name":"hy-test",
    # "pretrained_model_name_or_path":"Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers", 
    # "train_data_dir":"F:/ImageSet/sd3_test", 
    "output_dir":"F:/models/kolors",
    "save_name":"kolors-lora",
    "pretrained_model_name_or_path":"Kwai-Kolors/Kolors", # or local folder F:\Kolors
    "train_data_dir":"F:/ImageSet/kolors_test", 
    "vae_path":None, # or local file
    "resume_from_checkpoint":None,
    "model_path":None, 
    "logging_dir":"logs",
    "report_to":"wandb", 
    "rank":32,
    "train_batch_size":1,
    "repeats":10,
    "gradient_accumulation_steps":1,
    "mixed_precision":"fp16",
    "gradient_checkpointing":True,
    "optimizer":"prodigy",
    "lr_scheduler":"cosine", 
    "learning_rate":1,
    "lr_warmup_steps":0,
    "seed":4321,
    "num_train_epochs":20,
    "save_model_epochs":1, 
    "validation_epochs":1, 
    "skip_epoch":0, 
    "break_epoch":0,
    "skip_step":0, 
    "validation_ratio":0.1, 
    "use_dora":False,
    "recreate_cache":False,
    "caption_dropout":0.1
}

def run(
        script,
        seed,
        logging_dir,
        mixed_precision,
        report_to,
        lr_warmup_steps,
        output_dir,
        save_name,
        train_data_dir,
        optimizer,
        lr_scheduler,
        learning_rate,
        train_batch_size,
        repeats,
        gradient_accumulation_steps,
        num_train_epochs,
        save_model_epochs,
        validation_epochs,
        rank,
        skip_epoch,
        break_epoch,
        skip_step,
        gradient_checkpointing,
        validation_ratio,
        pretrained_model_name_or_path,
        model_path,
        resume_from_checkpoint,
        use_dora,
        recreate_cache,
        vae_path
    ):
    inputs = {
        "seed":seed,
        "logging_dir":logging_dir,
        "mixed_precision":mixed_precision,
        "report_to":report_to,
        "lr_warmup_steps":lr_warmup_steps,
        "output_dir":output_dir,
        "save_name":save_name,
        "train_data_dir":train_data_dir,
        "optimizer":optimizer,
        "lr_scheduler":lr_scheduler,
        "learning_rate":learning_rate,
        "train_batch_size":train_batch_size,
        "repeats":repeats,
        "gradient_accumulation_steps":gradient_accumulation_steps,
        "num_train_epochs":num_train_epochs,
        "save_model_epochs":save_model_epochs,
        "validation_epochs":validation_epochs,
        "rank":rank,
        "skip_epoch":skip_epoch,
        "break_epoch":break_epoch,
        "skip_step":skip_step,
        "gradient_checkpointing":gradient_checkpointing,
        "validation_ratio":validation_ratio,
        "pretrained_model_name_or_path":pretrained_model_name_or_path,
        "model_path":model_path,
        "resume_from_checkpoint":resume_from_checkpoint,
        "use_dora":use_dora,
        "recreate_cache":recreate_cache,
        "vae_path":vae_path
    }
    # Convert the inputs dictionary to a list of arguments
    # args = ["python", "train_sd3_lora_ui.py"]  # replace "your_script.py" with the name of your script
    # script = "test_.pyt"
    args = [sys.executable, script]
    for key, value in inputs.items():
        if value is not None:
            if isinstance(value, bool):  # exclude boolean values
                if value == True:
                    args.append(f"--{key}")
            else:
                args.append(f"--{key}")
                args.append(str(value))
                
    # Call the script with the arguments
    # subprocess.run(args)
    subprocess.call(args)
    # print(args)
    return " ".join(args)
    
global_local_storage = f"""
function() {{
    globalThis.setStorage = (key, value) => {{
        localStorage.setItem(key, JSON.stringify(value));
    }};

    globalThis.getStorage = (key) => {{
        return JSON.parse(localStorage.getItem(key));
    }};

    const script = getStorage('script') || '{default_config["default_script"]}';
    const output_dir = getStorage('output_dir') || '{default_config["output_dir"]}';
    const save_name = getStorage('save_name') || '{default_config["save_name"]}';
    const pretrained_model_name_or_path = getStorage('pretrained_model_name_or_path') || '{default_config["pretrained_model_name_or_path"]}';
    const vae_path = getStorage('vae_path') || '{default_config["vae_path"] if default_config["vae_path"] else ""}';
    const model_path = getStorage('model_path') || '{default_config["model_path"] if default_config["model_path"] else ""}';
    const resume_from_checkpoint = getStorage('resume_from_checkpoint') || '{default_config["resume_from_checkpoint"] if default_config["resume_from_checkpoint"] else ""}';
    const train_data_dir = getStorage('train_data_dir') || '{default_config["train_data_dir"]}';
    const logging_dir = getStorage('logging_dir') || '{default_config["logging_dir"]}';
    const report_to = getStorage('report_to') || '{default_config["report_to"]}';

    return [script, output_dir, save_name, pretrained_model_name_or_path, vae_path, model_path, resume_from_checkpoint, train_data_dir, logging_dir, report_to];
}}
"""

with gr.Blocks() as demo:
    script = gr.Dropdown(label="script", value=default_config["default_script"], choices=default_config["script_choices"])
    script.change(lambda x: x, script, None, js="(x) => {setStorage('script', x)}")
    with gr.Accordion("Directory section"):
        # dir section
        with gr.Row():
            output_dir = gr.Textbox(label="output_dir", value=default_config["output_dir"],
                                   placeholder="checkpoint save to")
            output_dir.change(lambda x: x, output_dir, None, js="(x) => {setStorage('output_dir', x)}")

            save_name = gr.Textbox(label="save_name", value=default_config["save_name"],
                                   placeholder="checkpoint save name")
            save_name.change(lambda x: x, save_name, None, js="(x) => {setStorage('save_name', x)}")
        with gr.Row():
            pretrained_model_name_or_path = gr.Textbox(label="pretrained_model_name_or_path", 
                value=default_config["pretrained_model_name_or_path"], 
                placeholder="repo name or dir contains diffusers model structure"
            )
            pretrained_model_name_or_path.change(lambda x: x, pretrained_model_name_or_path, None, js="(x) => {setStorage('pretrained_model_name_or_path', x)}")
            vae_path = gr.Textbox(label="vae_path", value=default_config["vae_path"], placeholder="separate vae single file path")
            vae_path.change(lambda x: x, vae_path, None, js="(x) => {setStorage('vae_path', x)}")
        with gr.Row():
            model_path = gr.Textbox(label="model_path", value=default_config["model_path"], placeholder="single weight files if not trained from official weight")
            model_path.change(lambda x: x, model_path, None, js="(x) => {setStorage('model_path', x)}")
            resume_from_checkpoint = gr.Textbox(label="resume_from_checkpoint", value=default_config["resume_from_checkpoint"], placeholder="resume the lora weight from seleted dir")
            resume_from_checkpoint.change(lambda x: x, resume_from_checkpoint, None, js="(x) => {setStorage('resume_from_checkpoint', x)}")
        with gr.Row():
            train_data_dir = gr.Textbox(label="train_data_dir", value=default_config["train_data_dir"], placeholder="dir contains dataset")
            train_data_dir.change(lambda x: x, train_data_dir, None, js="(x) => {setStorage('train_data_dir', x)}")
            logging_dir = gr.Textbox(label="logging_dir", value=default_config["logging_dir"], placeholder="logs folder")
            logging_dir.change(lambda x: x, logging_dir, None, js="(x) => {setStorage('logging_dir', x)}")
        with gr.Row():
            report_to = gr.Dropdown(label="report_to", value=default_config["report_to"], choices=["wandb"])
            report_to.change(lambda x: x, report_to, None, js="(x) => {setStorage('report_to', x)}")

    with gr.Accordion("Lora Config"):
        # train related section
        with gr.Row():
            rank = gr.Number(label="rank", value=default_config["rank"])
            train_batch_size = gr.Number(label="train_batch_size", value=default_config["train_batch_size"])
        with gr.Row():
            repeats = gr.Number(label="repeats", value=default_config["repeats"])
            gradient_accumulation_steps = gr.Number(label="gradient_accumulation_steps", value=default_config["gradient_accumulation_steps"])
            mixed_precision = gr.Radio(label="mixed_precision", value=default_config["mixed_precision"], choices=["fp16", "bf16"])
            gradient_checkpointing = gr.Checkbox(label="gradient_checkpointing", value=default_config["gradient_checkpointing"])
            use_dora = gr.Checkbox(label="use_dora", value=default_config["use_dora"])
        with gr.Row():
            optimizer = gr.Dropdown(label="optimizer", value=default_config["optimizer"], choices=["adamw","prodigy"])
            lr_scheduler = gr.Dropdown(label="lr_scheduler", value=default_config["lr_scheduler"], 
                        choices=["linear", "cosine", "cosine_with_restarts", "polynomial","constant", "constant_with_warmup"])
        with gr.Row():
            learning_rate = gr.Number(label="learning_rate", value=default_config["learning_rate"], info="Recommended: 1e-4 or 1 for prodigy")
            lr_warmup_steps = gr.Number(label="lr_warmup_steps", value=default_config["lr_warmup_steps"])
            seed = gr.Number(label="seed", value=default_config["seed"])

    with gr.Accordion("Misc"):
        with gr.Row():
            num_train_epochs = gr.Number(label="num_train_epochs", value=default_config["num_train_epochs"], info="Total epoches of the training")
            save_model_epochs = gr.Number(label="save_model_epochs", value=default_config["save_model_epochs"], info="Save checkpoint when x epoches")
            validation_epochs = gr.Number(label="validation_epochs", value=default_config["validation_epochs"], info="perform validation when x epoches")
        with gr.Row():
            skip_epoch = gr.Number(label="skip_epoch", value=default_config["skip_epoch"], info="Skip x epoches for validation and save checkpoint")
            break_epoch = gr.Number(label="break_epoch", value=default_config["break_epoch"], info="Stop train after x epoches")
            skip_step = gr.Number(label="skip_step", value=default_config["skip_step"], info="Skip x steps for validation and save checkpoint")
            validation_ratio = gr.Number(label="validation_ratio", value=default_config["validation_ratio"], info="Split dataset with this ratio for validation")
            recreate_cache = gr.Checkbox(label="recreate_cache", value=default_config["recreate_cache"])
    inputs = [
        script,
        seed,
        logging_dir,
        mixed_precision,
        report_to,
        lr_warmup_steps,
        output_dir,
        save_name,
        train_data_dir,
        optimizer,
        lr_scheduler,
        learning_rate,
        train_batch_size,
        repeats,
        gradient_accumulation_steps,
        num_train_epochs,
        save_model_epochs,
        validation_epochs,
        rank,
        skip_epoch,
        break_epoch,
        skip_step,
        gradient_checkpointing,
        validation_ratio,
        pretrained_model_name_or_path,
        model_path,
        resume_from_checkpoint,
        use_dora,
        recreate_cache,
        vae_path
        ]
    output = gr.Textbox(label="Output Box")
    run_btn = gr.Button("Run")
    run_btn.click(fn=run, inputs=inputs, outputs=output, api_name="run")
    
    demo.load(None, inputs=None, outputs=[script, output_dir, save_name, pretrained_model_name_or_path, vae_path, model_path, resume_from_checkpoint, train_data_dir, logging_dir, report_to], js=global_local_storage)
demo.launch()