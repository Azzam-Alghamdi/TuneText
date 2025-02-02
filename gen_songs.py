import groq
client = groq.Client(api_key="YOUR_API_KEY")

user_description_value = ""

def set_user_description(value):
    global user_description_value
    user_description_value = value
    

def gen_songs():
    songs = []
    current_chunk = ""

    completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that specializes in creating plain lists of song titles. Based on the user’s input, generate a list of 50 song names. The output must strictly adhere to the following rules:\n\n1-Provide only the song names and the artist name, one per line, with no numbers, bullet points, or symbols.\n2-Do not add any introductory or concluding text.\nIf you understand, begin your response with the song names directly."
            },
            {
                "role": "user",
                "content": user_description_value
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            current_chunk += content  # Accumulate the content in current_chunk

    # Now, split the accumulated content based on newlines (if each song name is on a new line)
    songs_list = current_chunk.splitlines()  # Split the content by lines

    # Add each song to the list
    for song in songs_list:
        cleaned_song = song.strip()  # Remove any extra whitespace
        if cleaned_song:  # Only add non-empty song names
            songs.append(cleaned_song)

    # Print the list of songs

    length = len(songs)
    if length > 50:
        extras = length - 50
        songs = songs[extras:]
    
    return songs
