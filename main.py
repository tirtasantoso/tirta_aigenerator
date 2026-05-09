from dotenv import load_dotenv
from rich import print

from clients.gemini import generate_gemini_content, generate_gemini_image
from clients.deepseek import generate_deepseek_content

def main():
    load_dotenv()

    print("[green]Running AI main function[/green]")

    generate_deepseek_content(
        prompts=[
            './prompts/prompt1.md',
            './prompts/prompt11_rogr_trauma.md',
            './prompts/prompt12_sentient_aura.md',
            './prompts/prompt13_immune_system.md',
            './prompts/prompt14_godric_intelligence.md',
            './prompts/prompt15_godric_magic.md',
        ],
        files=['./prompts/references/_reference_thronegate.md',],
    )

    generate_gemini_content(
        prompts=[
            './prompts/prompt1.md',
            './prompts/prompt11_rogr_trauma.md',
            './prompts/prompt12_sentient_aura.md',
            './prompts/prompt13_immune_system.md',
            './prompts/prompt14_godric_intelligence.md',
            './prompts/prompt15_godric_magic.md',
        ],
        files=['./prompts/references/_reference_thronegate.md',],
    )

    # generate_gemini_image(
    #     prompts=['./prompts/image_prompt2.md',],
    #     files=['./outputs/gemini_20260420_030607.md', './prompts/references/godric.png',],
    # )

    print("[green]-- All content generation is done. --[/green]")

if __name__ == "__main__":
    main()
