import os

from openai import OpenAI
from datetime import datetime

from .common import create_incremental_file, open_prompt_file

def generate_deepseek_content(prompts=['./prompts/prompt1.md', ]):

    print(f'Deepseek content generation starts now...')

    deepseek_model = 'deepseek-reasoner' # either 'deepseek-reasoner' or 'deepseek-chat'

    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com"
    )

    chat_settings = {
        'model': deepseek_model, # either 'deepseek-reasoner' or 'deepseek-chat',
        'messages': [],
        'stream': True,
        'max_tokens': 8192, # max 65536 for deepseek-reasoner, max 8192 for deepseek-chat
        # 'temperature': 1.0, # the higher the more creative the output, the lower the more focused and deterministic the output. Default is 1.0
    }


    # chat round 1
    # -------------------------------------------------------------------------
    chat_settings['messages'] += [{"role": "user", "content": open_prompt_file('./prompts/prompt1.md'),},]
    response = client.chat.completions.create(
        **chat_settings
    )

    output_file = create_incremental_file(f"./outputs/deepseek_{datetime.now():%Y%m%d_%H%M%S}.md")
    with open(output_file, "w") as f:
        f.write(f'{deepseek_model}\n-----------------------------------------------------------------\n\n')
        for chunk in response:
            if chunk.choices[0].delta.content is None:
                continue
            f.write(chunk.choices[0].delta.content)
            f.flush()
        f.close()


    # chat round 2
    # -------------------------------------------------------------------------
    if len(prompts) < 2:
        print(f'Deepseek content generation is done: {output_file}')
        return

    else:
        chat_settings['messages'] += [
            {"role": "assistant", "content": open_prompt_file(str(output_file)),},
        ]
        for prompt in prompts[1:]:

            chat_settings['messages'] += [
                {"role": "user", "content": open_prompt_file(prompt),},
            ]

            response = client.chat.completions.create(
                **chat_settings,
            )

            message_assistant = ""
            with open(output_file, "a") as f:
                f.write('\n\n=================================================================\n\n')
                f.write(open_prompt_file(prompt))
                f.write('\n\n-----------------------------------------------------------------\n\n')

                for chunk in response:
                    if chunk.choices[0].delta.content is None:
                        continue
                    f.write(chunk.choices[0].delta.content)
                    message_assistant += chunk.choices[0].delta.content
                    f.flush()
                f.close()

            chat_settings['messages'] += [
                {"role": "assistant", "content": message_assistant,},
            ]


    # from pprint import pprint
    # pprint(f'------------chat_settings------------')
    # pprint(chat_settings)

    print(f'Deepseek content generation is done: {output_file}')