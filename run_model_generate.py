from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, AutoConfig
import jsonlines
import re

num_test_case_list = [100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]

for num_test_case in num_test_case_list:

    checkpoint = "finetune_starcoder2_generate_" + str(num_test_case) + "/final_checkpoint"
    model = "bigcode/starcoder2-3b"
    device = "cuda"
    quantization_config = BitsAndBytesConfig(load_in_8bit=True)

    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

    with open("generate_data/test/generate_test_1000.txt", encoding="utf-8") as f:
        formal_test_case = f.read()
    cases = formal_test_case.split("--------Test_Cases--------:\n")

    wf = jsonlines.open("generate_data/test/generate_test_" + str(num_test_case) + "_result.jsonl", mode = "w")

    index = 0
    start_str = "/script\n"
    end_str = "/script_end\n"
    for case in cases:
        if case == "":
            continue
        case_lines = case.split("\n")
        generate_script = []
        formal_case = []
        for line in case_lines:
            exception_flag = False
            if line == "":
                continue
            inputs = tokenizer.encode("/generate\n" + line + "\n/generate_end\n", return_tensors="pt").to(device)
            eos_token_id = tokenizer.eos_token_id
            pad_token_id = tokenizer.pad_token_id
            outputs = model.generate(inputs, max_length=750, eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
            script = tokenizer.decode(outputs[0])
            print(script)
            script_line = script.split("\n")
            if  script_line[3] != "/script":
                exception_flag = True
            else:
                script = re.search(f"{start_str}(.*?){end_str}", script, re.DOTALL)
                if script == None:
                    outputs = model.generate(inputs, max_length=1000, eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
                    script = tokenizer.decode(outputs[0])
                    script = re.search(f"{start_str}(.*?){end_str}", script, re.DOTALL)
                    if script == None:
                        outputs = model.generate(inputs, max_length=1250, eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
                        script = tokenizer.decode(outputs[0])
                        script = re.search(f"{start_str}(.*?){end_str}", script, re.DOTALL)
                        if script == None:
                            print("Error: script is None")
                            exception_flag = True
            if exception_flag == True:
                script = "ERROR!\n"
            else:
                script = script.group(1)
            generate_script.append(script)
            formal_case.append(line)

        wf.write({"input": formal_case, "output": generate_script})
        index += 1
        print(str(index) + " done!")

    wf.close()