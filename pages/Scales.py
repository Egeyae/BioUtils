import streamlit as st
from scales import *
import pandas as pd
from residues_convert import to3Letters
import os

def save_scale_data(scale_id, scale_data, scales_data, is_new=False):
    if is_new and scale_id in scales_data['id'].values:
        st.error("Scale ID must be unique.")
        return False

    scale_filename = get_scale_filename(scale_id)
    scale_data[['Residues 1 Letter', 'Hydrophobic score']].to_csv(scale_filename, index=False, header=False)

    scale_info = {
        'id': scale_id,
        'name': scale_data.iloc[0].get('name', 'N/A'),
        'ref': scale_data.iloc[0].get('ref', 'N/A'),
        'desc': scale_data.iloc[0].get('desc', 'N/A')
    }

    if is_new:
        scales_data = pd.concat([scales_data, pd.DataFrame([scale_info])], ignore_index=True)
    else:
        scales_data.loc[scales_data['id'] == scale_id, ['name', 'ref', 'desc']] = scale_info['name'], scale_info['ref'], scale_info['desc']

    scales_data.to_csv('./data/scales.txt', index=False, sep='~')

    st.success("Scale data saved successfully.")
    return True

def delete_scale(scale_id, scales_data):
    if scale_id in scales_data['id'].values:
        scales_data = scales_data[scales_data['id'] != scale_id]
        scales_data.to_csv('./data/scales.txt', index=False, sep='~')
        os.remove(get_scale_filename(scale_id))
        st.success("Scale deleted successfully.")
        return True
    st.error("Scale ID not found.")
    return False


with st.sidebar:
    all_scales = get_all_scales()
    scale_options = {f"{id_} - {data['name']}": id_ for id_, data in list(all_scales.items())[1:]}
    scale_options["New scale"] = "new"
    selected_scale_label = st.selectbox("Choose a scale:", list(scale_options.keys()))
    selected_scale = scale_options[selected_scale_label]

scales_data = pd.read_csv('./data/scales.txt', delimiter='~')
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False
if 'scale_to_delete' not in st.session_state:
    st.session_state.scale_to_delete = None

if selected_scale == 'new':
    st.title("Create a New Scale")

    new_scale_data = pd.DataFrame({
        'Residues 1 Letter': list("ACDEFGHIKLMNPQRSTVWY"),
        'Hydrophobic score': [0] * 20
    })

    new_scale_id = st.text_input("Enter new scale ID:")
    new_scale_name = st.text_input("Enter new scale name:")
    new_scale_ref = st.text_input("Enter reference (optional):")
    new_scale_desc = st.text_input("Enter description (optional):")

    updated_scale = st.data_editor(new_scale_data, height=750, disabled=("Residues 1 Letter",), hide_index=True, use_container_width=True)

    if st.button("Save New Scale"):
        if new_scale_id and new_scale_name:
            updated_scale['name'] = new_scale_name
            updated_scale['ref'] = new_scale_ref if new_scale_ref else 'N/A'
            updated_scale['desc'] = new_scale_desc if new_scale_desc else 'N/A'
            save_scale_data(new_scale_id, updated_scale, scales_data, is_new=True)
            st.rerun()
        else:
            st.error("Scale ID and name must be provided.")
else:
    st.title(f"{selected_scale} - {all_scales[selected_scale]['name']}")

    scale_metadata = scales_data.loc[scales_data['id'] == selected_scale].iloc[0]
    scale_metadata_editable = pd.DataFrame(scale_metadata).T

    updated_scale_metadata = st.data_editor(scale_metadata_editable, hide_index=True)

    loaded_scale = pd.read_csv(get_scale_filename(selected_scale), names=['Residues 1 Letter', 'Hydrophobic score'])

    updated_scale = st.data_editor(loaded_scale, height=750, disabled=("Residues 1 Letter",), hide_index=True, use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Save Changes"):
            updated_scale['name'] = updated_scale_metadata.iloc[0]['name']
            updated_scale['ref'] = updated_scale_metadata.iloc[0]['ref']
            updated_scale['desc'] = updated_scale_metadata.iloc[0]['desc']
            if save_scale_data(selected_scale, updated_scale, scales_data):
                scales_data = pd.read_csv('./data/scales.txt', delimiter='~')
    with col2:
        if st.button("Delete Scale"):
            st.session_state.show_dialog = True
            st.session_state.scale_to_delete = selected_scale

if st.session_state.show_dialog:
    st.write("Are you sure you want to delete this scale?")
    if st.button("Yes", key="superkey"):
        if delete_scale(st.session_state.scale_to_delete, scales_data):
            st.session_state.show_dialog = False
            st.rerun()
    if st.button("No", key="superkeyno"):
        st.session_state.show_dialog = False