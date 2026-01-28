import streamlit as st
import os
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader


# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'XXXXXXXXXXXXXXXX'

# Define the chatbot picture
chatbot_image = "chatbot_image.jpg"  # Replace with the path to your chatbot image

@st.cache_resource(show_spinner=False)
def load_data():
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    docs = reader.load_data()
    service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.3))
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    return index


def main():

    #st.sidebar.image(chatbot_image, use_column_width=True)
    
    st.title("TMS Assistant")
    st.chat_message("assistant").markdown("Hi! I am EYSC bot, your personal assistant to help you with TMS related queries. How can I help you today?")

    index = load_data()

    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    # Add a sidebar with the chatbot image
    

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])    

    
    #question = st.text_input("Question", "")
    if question := st.chat_input("Start a Conversation"):
        question = str(question)
        st.chat_message("user").markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
    #if st.button("Submit"):
    #if question == None:
        #answer_level1 = answer_question(question, 'level1.csv')  # Use Level 1 CSV file

        with st.chat_message("assistant"):
                response = chat_engine.chat(question)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)    




        # Format the answer as if it's a chatbot response
        #st.write("Chatbot (Level 1):")
        #st.info(answer_level1)
        
    # Add radio button to ask if the user is satisfied with the answer
    #satisfaction = st.radio("Are you satisfied with the Level 1 answer?", ("Yes", "No"))
    
        

        
    #if satisfaction == "No":
        #st.write("Enter your Level 2 question below:")
        #question_level2 = st.text_input("Level 2 Question", "")
        #if st.button("Submit Level 2 Question"):
            #answer_level2 = answer_question(question_level2, 'level2.csv')  # Use Level 2 CSV file
            #st.write("Chatbot (Level 2):")
            #st.info(answer_level2)

if __name__ == "__main__":
    main()
