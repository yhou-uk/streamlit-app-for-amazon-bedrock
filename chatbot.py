import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import numpy as np
import utils
from argparse import ArgumentParser

def run_app():
    parser = ArgumentParser()
    parser.add_argument("--environmentName", type=str, default=None)

    args = parser.parse_args()

    environmentName = args.environmentName
    
    st.title("General Purpose Chabot")
    heading_column1, heading_column_space, heading_column2 = st.columns((6, 2, 2))

    with heading_column1:
        st.subheader(":grey[Amazon Bedrock Agents]")

    agent_id = st.text_input("Agent ID")
    agent_alias_id = st.text_input("Agent Alias ID")

    if st.button("Initialize Agent"):
        if agent_id and agent_alias_id:
            st.session_state.bedrock = utils.BedrockAgent(environmentName, agent_id, agent_alias_id)
            st.success("Agent initialized successfully!")
        else:
            st.warning("Please provide both Agent ID and Agent Alias ID.")


    st.markdown(
        """
    <style>
        .stButton button {
            background-color: white;
            width: 82px;
            border: 0px;
            padding: 0px;
        }
        .stButton button:hover {
            background-color: white;
            color: black;
        }

    </style>
    """,
        unsafe_allow_html=True,
    )

    if "chat_history" not in st.session_state or len(st.session_state["chat_history"]) == 0:
        st.session_state["chat_history"] = [
            {
                "role": "assistant",
                "prompt": "Hi, I am your assistant. How can I help you?",
            }
        ]

    for index, chat in enumerate(st.session_state["chat_history"]):
        with st.chat_message(chat["role"]):
            if index == 0:
                col1, space, col2 = st.columns((7, 1, 2))
                col1.markdown(chat["prompt"])

                if col2.button("Clear", type="secondary"):
                    st.session_state["chat_history"] = []
                    if "bedrock" in st.session_state:
                        st.session_state.bedrock.new_session()
                    st.rerun()

            elif chat["role"] == "assistant":
                col1, col2, col3 = st.columns((5, 4, 1))

                col1.markdown(chat["prompt"], unsafe_allow_html=True)

                if col3.checkbox(
                    "Trace", value=False, key=index, label_visibility="visible"
                ):
                    col2.subheader("Trace")
                    col2.markdown(chat["trace"])
            else:
                st.markdown(chat["prompt"])

    if prompt := st.chat_input("Ask the bot about an issue or incident..."):
        st.session_state["chat_history"].append({"role": "human", "prompt": prompt})

        with st.chat_message("human"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            col1, col2, col3 = st.columns((5, 4, 1))

            if col3.checkbox(
                "Trace",
                value=True,
                key=len(st.session_state["chat_history"]),
                label_visibility="visible",
            ):
                col2.subheader("Trace")

            if "bedrock" in st.session_state:
                response_text, trace_text = st.session_state.bedrock.invoke_agent(prompt, col2)
                st.session_state["chat_history"].append(
                    {"role": "assistant", "prompt": response_text, "trace": trace_text}
                )

                col1.markdown(response_text, unsafe_allow_html=True)
            else:
                col1.markdown("Please initialize the agent by providing the Agent ID and Agent Alias ID, and clicking the 'Initialize Agent' button.")