import jsonlines
import random
import os

num_case_list = [100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]

for num_case in num_case_list:
    fix_data = [item for item in jsonlines.open("fix_data/train/fix_train_" + str(num_case)+ ".jsonl", 'r')]
    generate_data = [item for item in jsonlines.open("generate_data/train/generate_train_" + str(num_case)+ ".jsonl", 'r')]
    verify_data = [item for item in jsonlines.open("verify_data/train/verify_train_" + str(num_case)+ ".jsonl", 'r')]

    combined_data = fix_data + generate_data + verify_data

    random.shuffle(combined_data)

    with jsonlines.open("mix_data/train/mix_train_" + str(num_case * 3)+ ".jsonl", 'w') as writer:
        for item in combined_data:
            writer.write(item)
