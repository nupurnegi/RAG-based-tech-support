from generator.generator_llm import generator_llm

def judge_with_llm(prompt):
    response = generator_llm().generate_text(prompt)
    # print(response)
    # score_str = response.splitlines()[0].strip()
    return response
    # try:
    #     return float(score_str)
    # except ValueError:
    #     print("Invalid judge output:", response)
    #     return 0.0
