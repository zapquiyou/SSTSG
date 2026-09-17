# Table of Contents
1. [Introduce](#introduce)
2. [File directory structure](#file-directory-structure)
3. [Installation](#installation)
3. [Experimental step](#experimental-step)

# Introduction

This is the repository for SSTSG, an approach that automatically generates test scripts from formal test cases using LLMs.

# File directory structure

```
root_directory/
├── finetune_lua_fix.sh         # finetune Starcoder2 using script fix samples
├── finetune_lua_generate.sh    # finetune Starcoder2 using script generation samples 
├── finetune_lua_mix.sh         # finetune Starcoder2 using mix samples
├── finetune_lua_verify.sh      # finetune Starcoder2 using script verification samples 
├── generate_test_data.sh       # generate test dataset 
├── generate_train_data.sh      # generate train dataset 
└── *.py                        # the functionality of the *.py files is described in the experimental step section.
```

# Installation
It is recommended to use conda to configure the environment in which the program runs. You can use the following command to create a python environment and activate it.

```bash
conda create -n script_generate python=3.11
conda activate script_generate
```

Then install the libraries need in the experiment.

```bash
pip install jsonlines
pip install nltk
pip install transformers
pip install accelerate
pip install datasets
pip install bitsandbytes
pip install peft
pip install trl
pip install wandb
pip install huggingface_hub
conda install pytorch torchvision torchaudio pytorch-cuda -c pytorch -c nvidia
```
Execute the following script using python to ensure that the words corpus of nltk is downloaded.

```python
import nltk
nltk.download('words')
```
Before you run any of the scripts make sure you are logged in `wandb` and HuggingFace Hub to push the checkpoints:
```bash
wandb login
huggingface-cli login
``` 

In addition, you need to install the lua interpreter and the luacheck tool, and make sure that the luacheck tool is located in the Path directory of the system environment variable. You can use the instructions below to check if the luacheck tool is installed and configured correctly.

```bash
luacheck -v
```

**Note:**  This experiment was run on the Ubuntu system. If you need to run on Windows, you need to make sure that the luacheck.bat is in the Path directory of the system environment variable and replace all the luacheck commands in the code with luacheck.bat.

# Experimental step
The experimental steps are as follows: 
1. Run finetune_lua.sh to fine-tune StarCoder2 on the Lua subset of the Stack-Dedup dataset.
2. Generate the training dataset using generate_train_data.sh; 
3. Generate the testing dataset using generate_test_data.sh; 
4. Fine-tune the model using finetune_lua_mix.sh, finetune_lua_generate.sh, finetune_lua_fix.sh, and finetune_lua_verify.sh, resulting in a Hybrid Model and Separate Models (including Script Generation, Script Fix, and Script Verification Models);
5. Run run_mix_model_total.py to get RQ1 original output (mix_data/test/test_mix_total_300000_result.jsonl) using Hybrid Model. Run mix_model_total_check.py to get RQ1 experimental result (mix_data/test/test_mix_total_300000_check.json);
6. Run run_mix_model_generate.py, run_mix_model_fix.py, and run_mix_model_verify.py to get RQ2 original output (mix_data/test/mix_test_\<functionality\>\_\<train dataset size\>\_result.jsonl) using Hybrid Model. Run mix_model_generate_check.py, run_mix_model_fix_check.py, and run_mix_model_verify_check.py to get RQ2 experimental result (mix_data/test/mix_\<functionality\>_\<train dataset size\>_check.json).
7. RQ3's partial experimental results have already been obtained in Step 5. Run run_model_generate.py, run_model_fix.py, and run_model_verify.py to get RQ3 remaining original output (\<functionality\>\_data/test/\<functionality\>\_test\_\<train dataset size\>\_result.jsonl) using Separate Model. Run generate_model_check.py, fix_model_check.py, and verify_model_check.py to get RQ3 remaining experimental result (\<functionality\>\_data/test/\<functionality\>\_check\_\<train dataset size\>\_result.json).
8. Run run_mix_model_generate_sampling.py, run_mix_model_fix_sampling.py, and run_mix_model_verify_sampling.py to get RQ4 original output (mix_data/test/test_mix_\<functionality\>\_15000\_temperature_\<temperature\>\_\<run index>\_result.jsonl) using Hybrid Model. Run mix_model_generate_sampling_check.py, run_mix_model_fix_sampling_check.py, and run_mix_model_verify_sampling_check.py to get RQ4 experimental result (mix_data/test/test_\<functionality\>\_sampling_\<temperature\>\_check.json).
