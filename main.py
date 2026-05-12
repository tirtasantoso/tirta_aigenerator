from dotenv import load_dotenv
from rich import print

from clients.gemini import generate_gemini_content, generate_gemini_image
from clients.deepseek import generate_deepseek_content

def main():
    load_dotenv()

    print("[green]Running AI main function[/green]")

    generate_deepseek_content(
        prompts=[
            {
                'message': './prompts/prompt16_statjournals.md',
                'files': [
                    './prompts/references/thronegate/00_MASTER_LORE.md',
                    './prompts/references/thronegate/01_godric_origin.md',
                    './prompts/references/thronegate/11_rogr_trauma.md',
                    './prompts/references/thronegate/12_sentient_aura.md',
                    './prompts/references/thronegate/13_immune_system.md',
                    './prompts/references/thronegate/14_godric_intelligence.md',
                    './prompts/references/thronegate/15_godric_magic.md',
                ]
            },
            {
                'message': './prompts/prompt16b.md',
                'files': [
                    './prompts/references/thronegate/16_statjournals.md',
                ]
            },
            {
                'message': './prompts/prompt17_superpowers.md',
                'files': []
            },
            # './prompts/prompt17.md',
            # './prompts/prompt18.md',
            # './prompts/prompt1.md',
            # './prompts/prompt11_rogr_trauma.md',
            # './prompts/prompt12_sentient_aura.md',
            # './prompts/prompt13_immune_system.md',
            # './prompts/prompt14_godric_intelligence.md',
            # './prompts/prompt15_godric_magic.md',
            # './prompts/prompt16_statjournals.md',
        ],
    )

    generate_gemini_content(
        prompts=[
            {
                'message': './prompts/prompt16_statjournals.md',
                'files': [
                    './prompts/references/thronegate/00_MASTER_LORE.md',
                    './prompts/references/thronegate/01_godric_origin.md',
                    './prompts/references/thronegate/11_rogr_trauma.md',
                    './prompts/references/thronegate/12_sentient_aura.md',
                    './prompts/references/thronegate/13_immune_system.md',
                    './prompts/references/thronegate/14_godric_intelligence.md',
                    './prompts/references/thronegate/15_godric_magic.md',
                ]
            },
            {
                'message': './prompts/prompt16b.md',
                'files': [
                    './prompts/references/thronegate/16_statjournals.md',
                ]
            },
            {
                'message': './prompts/prompt17_superpowers.md',
                'files': []
            },
            # './prompts/prompt17.md',
            # './prompts/prompt18.md',
            # './prompts/prompt1.md',
            # './prompts/prompt11_rogr_trauma.md',
            # './prompts/prompt12_sentient_aura.md',
            # './prompts/prompt13_immune_system.md',
            # './prompts/prompt14_godric_intelligence.md',
            # './prompts/prompt15_godric_magic.md',
            # './prompts/prompt16_statjournals.md',
        ],
    )

    # generate_gemini_image(
    #     prompts=['./prompts/image_prompt2.md',],
    #     files=['./outputs/gemini_20260420_030607.md', './prompts/references/godric.png',],
    # )

    print("[green]-- All content generation is done. --[/green]")

if __name__ == "__main__":
    main()
