import streamlit as st
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.openai import OpenAIEmbedding

#embedding_model = OpenAIEmbedding(model="text-embedding-3-small")
# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'XXXXX'

Settings.llm = OpenAI(model="gpt-4.1-nano")

# Define the chatbot picture
chatbot_image = "chatbot_image.jpg"  # Replace with the path to your chatbot image

@st.cache_resource(show_spinner="knowledge_base_loading")
def load_data():
    st.write("🔄 Starting load_data()")
    try:
        reader = SimpleDirectoryReader("data")
        st.write("📂 Reading files from data/")
        documents = reader.load_data()
        st.write(f"✅ Loaded {len(documents)} documents")
        index = VectorStoreIndex.from_documents(documents, embedding=None)
        st.write("Index created successfully")
    # reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    # docs = reader.load_data()
    # service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.3))
    # index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index
    except Exception as e:
        st.error("❌ load_data() failed")
        st.exception(e)
        return None


def main():

    st.sidebar.image(chatbot_image)
    
    st.title("Car Issues Bot")
    st.chat_message("assistant").markdown("Hi! I am a car issues troubleshooting bot. How can I help you today?")

    index = load_data()
    st.write("👇 Chat input should appear at the bottom")
    question = st.chat_input("Start a Conversation")

    if "chat_engine" not in st.session_state:
        st.session_state.chat_engine = index.as_chat_engine(chat_mode=ChatMode.CONDENSE_QUESTION, verbose=True)
    # Add a sidebar with the chatbot image


    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I am a car issues troubleshooting bot. How can I help you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])    

    
    #question = st.text_input("Question", "")


    if question:
        question = str(question)
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.messages.append({"role": "user", "content": question})
    #if st.button("Submit"):
    #if question == None:
        #answer_level1 = answer_question(question, 'level1.csv')  # Use Level 1 CSV file

        with st.chat_message("assistant"):
            response = st.session_state.chat_engine.chat(question)
            st.markdown(response.response)
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
