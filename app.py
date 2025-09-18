import streamlit as st
import json

import database
import recommender
import utils

# Initialize database on startup
database.init_db()

# Session state for language and cart
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Language toggle
lang_toggle = st.toggle("EN/AR", value=(st.session_state.language == 'en'))
st.session_state.language = 'en' if lang_toggle else 'ar'
lang = st.session_state.language

# Title
st.title(utils.get_text('title', lang))

# User preferences inputs
user_complexity = st.slider(utils.get_text('select_complexity', lang), min_value=1, max_value=10, value=5)
user_scalability = st.slider(utils.get_text('select_scalability', lang), min_value=1, max_value=10, value=5)
user_practicality = st.slider(utils.get_text('select_practicality', lang), min_value=1, max_value=10, value=5)

user_prefs = {
    'complexity': user_complexity,
    'scalability': user_scalability,
    'practicality': user_practicality
}

# Get all projects
all_projects = database.get_all_projects()

if st.button(utils.get_text('recommend_button', lang)):
    recommended_projects = recommender.recommend_projects(user_prefs, all_projects)

    for project in recommended_projects:
        name_key = 'name_en' if lang == 'en' else 'name_ar'
        desc_key = 'description_en' if lang == 'en' else 'description_ar'

        st.subheader(project.get(name_key, project['name_en']))
        st.write(project.get(desc_key, project['description_en']))

        # Development Map
        with st.expander(utils.get_text('view_dev_map', lang)):
            st.text(utils.generate_dev_map(project))

        # Add to cart
        if st.button(utils.get_text('add_to_cart', lang), key=f"add_{project['id']}"):
            st.session_state.cart.append(project)
            st.success("Added to cart!")

        # Download project info
        project_json = json.dumps(project)
        st.download_button(
            utils.get_text('download_project', lang),
            data=project_json,
            file_name=f"{project['name_en']}.json"
        )

# Cart section in sidebar
with st.sidebar.expander(utils.get_text('development_cart', lang)):
    if st.session_state.cart:
        for idx, item in enumerate(st.session_state.cart):
            st.write(item['name_en'] if lang == 'en' else item.get('name_ar', item['name_en']))
            if st.button(utils.get_text('remove', lang), key=f"remove_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()

        # Download cart
        cart_json = json.dumps(st.session_state.cart)
        st.download_button(
            utils.get_text('download_cart', lang),
            data=cart_json,
            file_name="dev_cart.json"
        )
    else:
        st.write("Cart is empty.")