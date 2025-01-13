import streamlit as st
from src.helper import voice_input, llm_model, text_to_speech

def main():
    st.title("Multilingual AI Assistant 🤖")
    
    if st.button("Ask me anything"):
        with st.spinner("Listening..."):
            text = voice_input()
            response = llm_model(text)
            text_to_speech(response)
            
            
            audio_file = open("speech.mp3", "rb") # Load Generated Speech
            audio_bytes = audio_file.read()
            
            
            st.text_area(label="Response:", value=response, height=350) # Display response in a text area
            
            
            st.audio(audio_bytes, format="audio/mp3") # Play the audio response
            
            st.download_button( # Add a download button for the speech file
                label="Download Speech",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mp3",
            )


if __name__ == '__main__':
    main()
