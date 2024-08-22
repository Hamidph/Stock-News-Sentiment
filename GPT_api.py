from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "who is mark zuck"
        }
    ]
)

print(completion.choices[0].message)
import pandas as pd
file_path = 'output_file_part_5.xlsx'
df = pd.read_excel(file_path)

# Assuming the column with the text is named 'Transcript'
transcripts = df['transcript']
from openai import OpenAI
import pandas as pd


def get_sentiment_score(transcript):
    prompt = prompt = f"Please analyze the following news transcript. First, determine if the news is related to the S&P 500 Index. If it is related, rate the sentiment on a scale from 1 to 10, where 1 is very negative and 10 is very positive. If the news is not related to the S&P 500, return a score of 0. Only provide the numerical score, with no additional text or explanation:\n\n{transcript}"

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that rates the sentiment of news transcripts."},
                {"role": "user", "content": prompt}
            ]
        )
        # Corrected access to the message content
        score = completion.choices[0].message.content.strip()
        return float(score)
    except Exception as e:
        print(f"Error: {e}")
        return None

# Apply the function to each transcript and store the results in a new column
df['Sentiment Score'] = transcripts.apply(get_sentiment_score)

# Save the results back to Excel
output_file_path = 'output_file_path5.xlsx'
df.to_excel(output_file_path, index=False)

print("Sentiment analysis completed and saved to Excel.")
