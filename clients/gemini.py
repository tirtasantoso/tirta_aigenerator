import os
from urllib import response

from google import genai
from google.genai import types
from pathlib import Path
from datetime import datetime
from PIL import Image

from .common import create_incremental_file, open_prompt_file

def generate_gemini_content(
        prompts: list[dict] = [{'message': './prompts/prompt1.md', 'files': []}],
        system_persona: str = './prompts/references/_system_role.md',
    ):

    print(f'Gemini content generation starts now...')

    gemini_model = "gemini-3.5-flash" # either "gemini-3.1-pro-preview", "gemini-3.5-flash"

    client = genai.Client(
        api_key=os.environ.get('GEMINI_API_KEY')
    )

    chat = client.chats.create(
        model=gemini_model,
        config={
             'system_instruction': open_prompt_file(system_persona),
        }
    )

    # chat round 1
    # -------------------------------------------------------------------------
    message1 = open_prompt_file(prompts[0]['message'])
    files1 = [client.files.upload(file=Path(file_location)) for file_location in prompts[0]['files'] if 'files' in prompts[0] and prompts[0]['files']]
    response = chat.send_message_stream(
        # message=message1,
        message=[message1] + files1,
    )

    output_file_name = f"gemini_{datetime.now():%Y%m%d_%H%M%S}"
    output_file = create_incremental_file(f"./outputs/{output_file_name}.md")
    output_reasoning_file = create_incremental_file(f"./outputs/{output_file_name}_reasoning.md")

    with open(output_file, "w") as f, open(output_reasoning_file, "w") as f_reasoning:
        f_reasoning.write(
            f'{gemini_model}\n'
            f'==================================\n'
            f'*{output_reasoning_file}*\n\n'
            f'{open_prompt_file(prompts[0]["message"])}\n'
        )

        f.write(
            f'{gemini_model}\n'
            f'==================================\n'
            f'*{output_file}*\n\n'
        )

        for chunk in response:
            f.write(chunk.text)
            f.flush()

        f_reasoning.write(
            f'\n\n----------------------------------\n\n'
        )
        f.write(
            f'\n\n----------------------------------\n\n'
        )

        f_reasoning.close()
        f.close()


    # chat round 2
    # -------------------------------------------------------------------------
    if len(prompts) < 2:
        print(f'Gemini content generation is done: {output_file}, {output_reasoning_file}')
        return

    else:
        for prompt in prompts[1:]:
            message2 = open_prompt_file(prompt['message'])
            files2 = [client.files.upload(file=Path(file_location)) for file_location in prompt['files'] if 'files' in prompt and prompt['files']]
            response = chat.send_message_stream(
                message=[message2] + files2,
            )
            with open(output_file, "a") as f, open(output_reasoning_file, "a") as f_reasoning:
                f_reasoning.write(
                    f'## {prompt["message"]}\n'
                    f'{message2}\n'
                    f'\n\n----------------------------------\n\n'
                )

                f.write(
                    f'## {prompt["message"]}\n'
                    f'*{output_file}*\n\n'
                )

                for chunk in response:
                    f.write(chunk.text)
                    f.flush()

                f.write(
                    f'\n\n----------------------------------\n\n'
                )

                f_reasoning.close()
                f.close()

    print(f'Gemini content generation is done: {output_file}, {output_reasoning_file}')



def generate_gemini_image(prompts=['./prompts/image_prompt1.md', ], files=['./files/file1.pdf', ]):

    print(f'Gemini image generation starts now...')

    gemini_model = "gemini-3.1-flash-image-preview" # either "gemini-3.1-flash-image-preview", "gemini-3-pro-image-preview'

    client = genai.Client(
        api_key=os.environ.get('GEMINI_API_KEY')
    )

    if files and len(files) > 0:
        myfiles = [client.files.upload(file=Path(file_location)) for file_location in files]
    else:
        myfiles = []

    message1 = open_prompt_file(prompts[0])

    response = client.models.generate_content(
        model=gemini_model,
        contents=myfiles + [message1],
    )

    output_file = create_incremental_file(f"./outputs/gemini_{datetime.now():%Y%m%d_%H%M%S}.md")
    with open(output_file, "w") as f:
        f.write(f'#gemini_model:\n{gemini_model}\n\n')
        f.write(f'#files:\n{files}\n\n')
        f.write(f'#message:\n {message1}\n')
        f.write(f'================')
    for part in response.parts:
        if part.text is not None:
            with open(output_file, "a") as f:
                f.write(part.text)
                f.flush()
                f.close()
        elif part.inline_data is not None:
            image = part.as_image()
            image.save(output_file.with_suffix('.png'))

    print(f'Gemini image generation is done: {output_file}')