from dotenv import load_dotenv
from rich import print

from clients.gemini import generate_gemini_content, generate_gemini_image
from clients.deepseek import generate_deepseek_content

def main():
    load_dotenv()

    print("[green]Running AI main function[/green]")
    # generate_deepseek_content(['./prompts/prompt1.md', './prompts/prompt2.md',])
    generate_gemini_content(
        prompts=['./prompts/prompt6.md',],
        files=['./outputs/gemini_20260419_223751.md',],
    )
    # generate_gemini_image(
    #     prompts=['./prompts/image_prompt1.md',],
    #     files=[], # ['./prompts/prompt1.md', './outputs/gemini_20260419_164413.md'],
    # )
    print("[green]-- All content generation is done. --[/green]")

if __name__ == "__main__":
    main()
