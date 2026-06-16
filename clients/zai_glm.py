import os
import json

from openai import OpenAI
from datetime import datetime
from pathlib import Path

from .common import create_incremental_file, open_prompt_file

def generate_glm_content(
        system_persona: str = './prompts/references/_system_role.md',
        prompts: list[dict] = [{'message': './prompts/prompt1.md', 'files': []}],
        reasoning_effort: str|bool = 'max',
        with_json_output = False,
    ):

    print(f'GLM content generation starts now...')

    glm_model = 'glm-5.2' # either 'glm-5.1' or 'glm-4.7'

    client = OpenAI(
        api_key=os.environ.get('ZAI_GLM_API_KEY'),
        base_url="https://api.z.ai/api/paas/v4/"
    )

    chat_settings = {
        'model': glm_model,
        'messages': [
            {
                "role": "system",
                "content": open_prompt_file(system_persona)
            }
        ],
        'stream': True,
        'max_tokens': 131072, # max 131072, min 1, default 4096
        'temperature': 1.0, # the higher the more creative the output, the lower the more focused and deterministic the output. Default is 1.0
    }
    if reasoning_effort:
        chat_settings.update({
            'reasoning_effort': reasoning_effort, # either "low", "medium", or "high". The higher the reasoning effort, the more time the model will spend on thinking and reasoning before giving an answer. Default is "medium".'
            'extra_body': {"thinking": {
                "type": "enabled",
                "clear_thinking": False  # False for Preserved Thinking
            }},
        })
    else:
        chat_settings.update({
            'extra_body': {"thinking": {"type": "disabled"}},
        })


    # chat round 1
    # -------------------------------------------------------------------------
    # content_files = []
    # if files and len(files) > 0:
    #     # for file_location in files:
    #     #     file_obj = client.files.create(
    #     #         file=open(Path(file_location), "rb"),
    #     #         purpose="user_data"
    #     #     )
    #     #     content_files += [
    #     #         {
    #     #             "type": "input_file",
    #     #             "file_id": file_obj.id,
    #     #         },
    #     #     ]
    #     for file_location in files:
    #         content_files += [
    #             {"type": "text", "text": open_prompt_file(file_location),}
    #         ]
    content_files = [
        {"type": "text", "text": f'<file name="{Path(file).name}">{open_prompt_file(file)}</file>'} for file in prompts[0]['files'] if 'files' in prompts[0] and prompts[0]['files']
    ]
    if 'json_premessages' in prompts[0] and prompts[0]['json_premessages']:
        chat_settings['messages'] += open_prompt_file(prompts[0]['json_premessages'])
    chat_settings['messages'] += [
        {"role": "user", "content": content_files + [{"type": "text", "text": open_prompt_file(prompts[0]['message'])},],}
    ]
    response = client.chat.completions.create(
        **chat_settings
    )

    output_file_name = f"glm_{datetime.now():%Y%m%d_%H%M%S}"
    output_file = create_incremental_file(f"./outputs/{output_file_name}.md")
    output_reasoning_file = create_incremental_file(f"./outputs/{output_file_name}_reasoning.md")

    reasoning_assistant = ""
    content_assistant = ""

    with open(output_reasoning_file, "w") as f_reasoning, open(output_file, "w") as f:

        f_reasoning.write(
            f'{glm_model}\n'
            f'==================================\n'
            f'*{output_reasoning_file}*\n\n'
            f'{open_prompt_file(prompts[0]["message"])}\n'
            f'\n----------------------------------\n'
            f'<blockquote>\n'
        )

        f.write(
            f'{glm_model}\n'
            f'==================================\n'
            f'*{output_file}*\n\n'
        )

        for chunk in response:
            if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                reasoning_assistant += chunk.choices[0].delta.reasoning_content
                f_reasoning.write(chunk.choices[0].delta.reasoning_content)
                f_reasoning.flush()
            elif chunk.choices[0].delta.content:
                content_assistant += chunk.choices[0].delta.content
                f.write(chunk.choices[0].delta.content)
                f.flush()

        f_reasoning.write(
            f'\n</blockquote>\n'
            f'\n\n----------------------------------\n\n'
        )
        f.write(
            f'\n\n----------------------------------\n\n'
        )
        f_reasoning.close()
        f.close()

    chat_settings['messages'] += [
        {"role": "assistant", "reasoning_content": reasoning_assistant, "content": content_assistant},
    ]


    # chat round 2
    # -------------------------------------------------------------------------
    if len(prompts) < 2:
        print(f'GLM content generation is done: {output_file}, {output_reasoning_file}')
        return

    else:
        for prompt in prompts[1:]:
            content_files = [
                {"type": "text", "text": f'<file name="{Path(file).name}">{open_prompt_file(file)}</file>'} for file in prompt['files'] if 'files' in prompt and prompt['files']
            ]
            if 'json_premessages' in prompt and prompt['json_premessages']:
                chat_settings['messages'] += open_prompt_file(prompt['json_premessages'])
            chat_settings['messages'] += [
                {"role": "user", "content": content_files + [{"type": "text", "text": open_prompt_file(prompt["message"])},],},
            ]

            response = client.chat.completions.create(
                **chat_settings,
            )

            reasoning_assistant = ""
            content_assistant = ""

            with open(output_reasoning_file, "a") as f_reasoning, open(output_file, "a") as f:

                f_reasoning.write(
                    f'## {prompt["message"]}\n'
                    f'*{output_reasoning_file}*\n\n'
                    f'{open_prompt_file(prompt["message"])}\n'
                    f'<blockquote>\n'
                )

                f.write(
                    f'## {prompt["message"]}\n'
                    f'*{output_file}*\n\n'
                )

                for chunk in response:
                    if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                        reasoning_assistant += chunk.choices[0].delta.reasoning_content
                        f_reasoning.write(chunk.choices[0].delta.reasoning_content)
                        f_reasoning.flush()
                    elif chunk.choices[0].delta.content:
                        content_assistant += chunk.choices[0].delta.content
                        f.write(chunk.choices[0].delta.content)
                        f.flush()

                f_reasoning.write(
                    f'\n</blockquote>\n'
                    f'\n\n----------------------------------\n\n'
                )
                f.write(
                    f'\n\n----------------------------------\n\n'
                )
                f_reasoning.close()
                f.close()

            chat_settings['messages'] += [
                {"role": "assistant", "reasoning_content": reasoning_assistant, "content": content_assistant},
            ]


    if with_json_output:
        output_json_file = create_incremental_file(f"./outputs/{output_file_name}_reasoning.json")
        with open(output_json_file, "a") as f:
            f.write(json.dumps(chat_settings['messages'], indent=4))
            f.close()

    print(f'GLM content generation is done: {output_file}, {output_reasoning_file}')


def generate_glm_file_list(
        prompt: dict = {'message': './prompts/prompt1.md', 'files': []},
        create_doc = False,
    ):
        output_file = create_incremental_file(f"./outputs/{Path(prompt['message']).stem}_filelist.md")
        file_content = 'Treat the following list of files as additional contexts for ALL future prompts in this chat. These contexts are supplementary and should be used to enhance the responses. The file "00_MASTER_LORE.md" is to be treated as the master reference lore, and the other files as examples of stories that you can use as additional references.\n\n'
        for file in prompt['files']:
            # file_content.append({"file": Path(file).name, "content": open_prompt_file(file)})
            file_content += f'<file name="{Path(file).name}">\n{open_prompt_file(file)}\n</file>\n'
        with open(output_file, "a") as f:
            # f.write(json.dumps(file_content, indent=4))
            f.write(file_content)
            f.close()