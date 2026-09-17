accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_300.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_300/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_750.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_750/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_1500.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_1500/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_3000.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_3000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_7500.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_7500/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_15000.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_15000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_30000.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_30000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_75000.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_75000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_150000.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_150000/"

accelerate launch finetune_modify.py \
        --model_id "finetune_starcoder2/final_checkpoint" \
        --dataset_name "json" \
        --data_files "mix_data/train/mix_train_300000.jsonl" \
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
        --output_dir "finetune_starcoder2_mix_300000/"