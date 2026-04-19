import os
from urllib import response

from google import genai
from google.genai import types
from pathlib import Path
from datetime import datetime
from PIL import Image

from .common import create_incremental_file, open_prompt_file

def generate_gemini_content(
    prompts: list[Path|str] = ['./prompts/prompt1.md', ],
    files: list[Path|str] = []
    ):

    print(f'Gemini content generation starts now...')

    gemini_model = "gemini-3-flash-preview" # either "gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview", 'gemini-3-flash-preview'

    client = genai.Client(
        api_key=os.environ.get('GEMINI_API_KEY')
    )

    chat = client.chats.create(
        model=gemini_model,
    )

    if files and len(files) > 0:
        myfiles = [client.files.upload(file=Path(file_location)) for file_location in files]
    else:
        myfiles = []

    # chat round 1
    # -------------------------------------------------------------------------
    message1 = open_prompt_file(prompts[0])
    response = chat.send_message_stream(
        # message=message1,
        message=[message1] + myfiles,
    )

    output_file = create_incremental_file(f"./outputs/gemini_{datetime.now():%Y%m%d_%H%M%S}.md")
    with open(output_file, "w") as f:
        f.write(f'{gemini_model}\n-----------------------------------------------------------------\n\n')
        for chunk in response:
            f.write(chunk.text)
            f.flush()
        f.close()


    # chat round 2
    # -------------------------------------------------------------------------
    if len(prompts) < 2:
        print(f'Gemini content generation is done: {output_file}')
        return

    else:
        for prompt in prompts[1:]:
            message2 = open_prompt_file(prompt)
            response = chat.send_message_stream(
                message=message2,
            )
            with open(output_file, "a") as f:
                f.write('\n\n=================================================================\n\n')
                f.write(message2)
                f.write('\n\n-----------------------------------------------------------------\n\n')
                for chunk in response:
                    f.write(chunk.text)
                    f.flush()
                f.close()

    print(f'Gemini content generation is done: {output_file}')


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
    for part in response.parts:
        if part.text is not None:
            with open(output_file, "w") as f:
                f.write(part.text)
                f.flush()
                f.close()
        elif part.inline_data is not None:
            image = part.as_image()
            image.save(output_file.with_suffix('.png'))


    print(f'Gemini image generation is done: {output_file}')