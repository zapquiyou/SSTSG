accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_100.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_100/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_250.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_250/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_500.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_500/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_1000.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_1000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_2500.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_2500/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_5000.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_5000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_10000.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_10000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_25000.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_25000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_50000.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_50000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "verify_data/train/verify_train_100000.jsonl" \
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
        --output_dir "finetune_starcoder2_verify_100000/"