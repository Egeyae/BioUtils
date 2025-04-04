import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from seqextract.Sequence import Sequence
from hydrophob.utils import compute_profile
from scales import get_scale_name, get_scale_ids, load_scale, get_all_scales

st.set_page_config(page_title="Hydrophob", layout="wide")

# st.markdown(
#     """
#     <style>
#     .main {background-color: #f9f9f9; padding: 20px; border-radius: 8px;}
#     .sidebar .sidebar-content {background-color: #f0f2f6; padding: 20px; border-radius: 8px;}
#     </style>
#     """, unsafe_allow_html=True)

st.title("Hydrophob - Hydrophobic Profile Generator")

with st.sidebar:
    st.header("Input Options")
    all_scales = get_all_scales()
    scale_options = {f"{id_} - {data['name']}": id_ for id_, data in list(all_scales.items())[1:]}
    selected_scale_label = st.selectbox("Choose a scale:", list(scale_options.keys()))
    selected_scale = scale_options[selected_scale_label]

    sequence_file = st.file_uploader("Upload a file (FASTA, PDB, or Raw)", type=["txt", "fasta", "pdb"])
    if sequence_file is not None:
        stringio = StringIO(sequence_file.getvalue().decode("utf-8"))
        sequence_input = stringio.read()
    else:
        sequence_input = st.text_area("Or enter protein sequence:", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", height=150)

    window_size = st.slider("Select window size:", 3, 51, 7, step=2)
    generate_profile = st.button("Generate Profile")


if generate_profile:
    try:
        default_scale = load_scale(selected_scale)
        sequence = Sequence(sequence_input)
        profile = compute_profile(sequence, default_scale, window_size)

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(profile, linestyle='-', color="#1f77b4")
        ax.set_ylabel('Hydrophobicity Score', fontsize=12)
        ax.set_xlabel('Position', fontsize=12)
        ax.set_title(f"Hydrophobic Profile ({get_scale_name(selected_scale)}, Window = {window_size})", fontsize=14)
        ax.grid(True)

        st.pyplot(fig)

        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        col1, col2 = st.columns([3, 1])

        with col1:
            default_info = sequence.info if sequence.info else "noinfo"
            filename = st.text_input(
                "Download file name:", 
                value = f"hydroprofile_win{window_size}_{selected_scale}_{default_info}.png"
            )

        with col2:
            st.download_button(
                label="Download plot",
                data=buf,
                file_name=filename,
                mime="image/png"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")

