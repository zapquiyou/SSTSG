accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_100.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_100/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_250.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_250/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_500.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_500/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_1000.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_1000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_2500.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_2500/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_5000.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_5000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_10000.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_10000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_25000.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_25000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_50000.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_50000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "generate_data/train/generate_train_100000.jsonl" \
        --subset "data/lua" \
        --dataset_text_field "content" \
        --split "train" \
        --max_seq_length 2000 \
        --max_steps -1 \
        --micro_batch_size 1 \
        --gradient_accumulation_steps 8 \
        --learning_rate 2e-5 \
        --warmup_steps 20 \
        --num_proc "$(nproc)" \
        --save_steps 5000   \
        --output_dir "finetune_starcoder2_generate_100000/"