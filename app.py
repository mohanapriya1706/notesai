import streamlit as st
import requests

# URL of the backend API
API_URL = "http://127.0.0.1:5000/generate"

# Function to generate detailed notes for a specific key point
def generate_detailed_notes(key_points):
    response = requests.post(API_URL, json={"key_points": key_points})
    if response.status_code == 200:
        data = response.json()
        return data.get("response", "No notes generated.")
    else:
        return "Error generating notes."

# Function to apply custom styles for simplicity and modern look
def set_page_style():
    st.markdown("""
        <style>
            /* Global Styles */
            body {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Helvetica', sans-serif;
            }

            .stTitle {
                font-size: 32px;
                font-weight: 600;
                color: #e0e0e0;
            }

            .stMarkdown {
                font-size: 16px;
                color: #b3b3b3;
            }

            /* Input Fields */
            .stTextInput>div>div>input {
                background-color: #333333;
                color: #ffffff;
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
            }

            .stTextArea>div>textarea {
                background-color: #333333;
                color: #ffffff;
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
            }

            /* Buttons */
            .stButton>button {
                background-color: #565656;
                color: #ffffff;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.2s ease;
            }

            .stButton>button:hover {
                background-color: #787878;
            }

            /* Detailed Notes Styling */
            .detailed-notes {
                background-color: #2c2c2c;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
                color: #d1d1d1;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)

# Streamlit UI
def main():
    set_page_style()

    tab1, tab2 = st.tabs(["Generate Notes", "All Notes"])

    with tab1:
        st.title("NotesAI")

        st.markdown("""
        Enter key points, and NotesAI will expand them into detailed notes.
        """)

        # Create a session state to manage multiple notes
        if 'notes' not in st.session_state:
            st.session_state.notes = [{"key_points": "", "detailed_notes": ""}]

        # Display all the notes
        for i, note in enumerate(st.session_state.notes):
            with st.expander(f"Note {i+1}"):
                note["key_points"] = st.text_area("Key Points:", note["key_points"], key=f"note_{i}_key_points", height=100)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Generate Notes", key=f"generate_{i}"):
                        with st.spinner("Generating notes..."):
                            note["detailed_notes"] = generate_detailed_notes(note["key_points"])
                with col2:
                    if st.button("Save Notes", key=f"save_{i}"):
                        # Add code to save notes to file or database
                        st.success("Notes saved successfully!")
                if note["detailed_notes"]:
                    st.markdown(f'<div class="detailed-notes">{note["detailed_notes"]}</div>', unsafe_allow_html=True)
                    note["detailed_notes"] = st.text_area("Edit Notes:", note["detailed_notes"], key=f"edit_{i}_notes", height=200)

        # Add new note button
        if st.button("Add Note"):
            st.session_state.notes.append({"key_points": "", "detailed_notes": ""})

    with tab2:
        st.title("All Notes")
        for i, note in enumerate(st.session_state.notes):
            with st.expander(f"Note {i+1}"):
                st.markdown(f"**Key Points:** {note['key_points']}")
                if note["detailed_notes"]:
                    st.markdown(f"**Detailed Notes:**")
                    st.markdown(f'<div class="detailed-notes">{note["detailed_notes"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"**Detailed Notes:** No notes generated yet.")

if __name__ == "__main__":
    main()