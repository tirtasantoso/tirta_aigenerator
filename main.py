from dotenv import load_dotenv
from rich import print

from clients.gemini import generate_gemini_content, generate_gemini_image
from clients.zai_glm import generate_glm_content, generate_glm_file_list
from clients.deepseek import generate_deepseek_content, generate_deepseek_file_list

def main():
    load_dotenv()

    print("[green]Running AI main function[/green]")

    system_persona = './prompts/references/thronegate/_SYSTEM_PERSONA.md'

    prompts_list = [
        # {
        #     'json_premessages': './outputs/glm_20260613_102637_reasoning.json',
        #     'message': './prompts/prompt23_godric_infiltration.md',
        #     'files': [],
        # },
        # {
        #     'message': './prompts/prompt22_godric_video_game.md',
        #     'files': [],
        # },
        # {
        #     'message': './prompts/prompt2_rogr_trauma.md',
        #     'files': []
        # },
        # {
        #     'message': './prompts/prompt3_gent_incident.md',
        #     'files': []
        # },
        # {
        #     'message': './prompts/prompt4_immune_system.md',
        #     'files': []
        # },
        # {
        #     'message': './prompts/prompt5_godric_intelligence.md',
        #     'files': []
        # },
        # {
        #     'message': './prompts/prompt6_godric_magic.md',
        #     'files': []
        # },
        {
            'message': './prompts/prompt7_statjournals.md',
            'files': [
                './prompts/references/thronegate/00_MASTER_LORE.md',
                './prompts/references/thronegate/01_godric_origin.md',
                './prompts/references/thronegate/02_rogr_trauma.md',
                './prompts/references/thronegate/03_sentient_aura.md',
                './prompts/references/thronegate/04_immune_system.md',
                './prompts/references/thronegate/05_godric_intelligence.md',
                './prompts/references/thronegate/06_godric_magic.md',
                './prompts/references/thronegate/07_statjournals.md',
            ]
        },
        # {
        #     'message': './prompts/prompt7b_redothis.md',
        #     'files': [
        #         './prompts/references/thronegate/07_statjournals.md',
        #     ]
        # },
        {
            'message': './prompts/prompt8_superpowers.md',
            'files': [
                './prompts/references/thronegate/08_superpowers.md',
            ]
        },
        {
            'message': './prompts/prompt9_pleasurable_stats.md',
            'files': []
        },
        # {
        #     'message': './prompts/prompt10_godric_universe.md',
        #     'files': []
        # },
        {
            'message': './prompts/prompt10_stasis_origin.md',
            'files': []
        },
        {
            'message': './prompts/prompt11_future_godric.md',
            'files': []
        },
        # {
        #     'message': './prompts/prompt12_godric_skills.md',
        #     'files': []
        # },
        {
            'message': './prompts/prompt20_godric_vs_earth.md',
            'files': []
        },
        {
            'message': './prompts/prompt21_godric_vs_fiction.md',
            'files': []
        },
    ]

    # generate_deepseek_content(
    #     system_persona=system_persona,
    #     prompts=prompts_list,
    #     reasoning_effort='high',
    #     with_json_output=True,
    # )

    # generate_deepseek_file_list(
    #     prompt=prompts_list[0],
    # )

    generate_glm_content(
        system_persona=system_persona,
        prompts=prompts_list,
        reasoning_effort='high',
        with_json_output=True,
    )

    # generate_gemini_content(
    #     system_persona=system_persona,
    #     prompts=prompts_list,
    # )

    # generate_gemini_image(
    #     prompts=['./prompts/image_prompt2.md',],
    #     files=['./outputs/gemini_20260420_030607.md', './prompts/references/godric.png',],
    # )

    print("[green]-- All content generation is done. --[/green]")

if __name__ == "__main__":
    main()
