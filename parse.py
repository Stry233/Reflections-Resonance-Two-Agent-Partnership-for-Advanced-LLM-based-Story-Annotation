import json
import os
import requests
import openai

def load_stories_from_folder(folder_path):
    """Load all the story files present in a given directory."""
    story_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    stories = {}

    for story_file in story_files:
        with open(os.path.join(folder_path, story_file), 'r') as f:
            stories[story_file] = f.read()

    return stories


def main():
    folder_path = "source/The Shmoop Corpus/stories/20,000 Leagues Under the Sea"  # Replace with your folder path
    system_prompt = """
    In this task, you are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture. 
    Your primary goal is to assist users by answering their questions, providing explanations, and helping with 
    various tasks to the best of your ability. Be informative, accurate, and concise. If you don't know the answer 
    or can't help, say so. Always aim to provide a positive and helpful user experience.
    """

    prompt = """
    Instructions for Analysis Using Predicates:
    
    Character Descriptions:
    
    Provide predicates that detail the characters and their relationships within the story.
    Story's Beginning:
    
    Describe the initial states, beliefs, and introduced characters at the start using predicates.
    Event Breakdown:
    
    Count and list the significant events in the story using predicates.
    Illustrate a chronological timeline of these events.
    Author's Techniques:
    
    Investigate the use of "forecast" and "backslash" by the author.
    Detail the events associated with each term using predicates.
    Literary Tropes:
    
    Identify and list the literary tropes present in the story.
    Offer explanations for each trope's use and significance.
    Narrative Perspective:
    
    Analyze any changes in perspectives made by the author throughout the story.
    """

    before_story = """
    Sure! Let's break down the analysis you're looking for into each of its parts. But first, I'd need the story or a summary of the story to proceed with the analysis. 
    """

    openai.organization = "rpinlp"  # @param {type:"string"}
    openai.api_key = "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"  # @param {type:"string"}
    model_name = "gpt-4"

    def parseMsg(gptJsonAns):
        json_data = json.loads(str(gptJsonAns))
        return json_data['choices'][0]['message']['content']


    stories = load_stories_from_folder(folder_path)
    for story_name, story_content in stories.items():
        print(f"Analysis for: {story_name}")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt + '\n\n' + story_content},
            # {"role": "assistant",
            #  "content": before_story},
            # {"role": "user", "content": story_content}
        ]

        analysis= parseMsg(
            openai.ChatCompletion.create(
                model=model_name,
                messages=messages
            ))

        print(analysis)
        with open(f"output/{story_name}_analyze.txt", "w") as text_file:
            text_file.write(analysis)
        print("-" * 50)


if __name__ == "__main__":
    main()
