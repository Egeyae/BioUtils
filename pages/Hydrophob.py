import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins, utils
from io import StringIO, BytesIO
from seqextract.Sequence import Sequence
from hydrophob.utils import compute_profile
from scales import get_scale_name, get_scale_ids, load_scale, get_all_scales

st.set_page_config(page_title="Hydrophob", layout="wide")

st.markdown(
    """
    <style>
    .main {background-color: #f0f2f6; padding: 20px; border-radius: 8px;}
    .sidebar .sidebar-content {background-color: #ffffff; padding: 20px; border-radius: 8px;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px;}
    .stTextInput>div>div>input {border-radius: 8px;}
    .stSelectbox>div>div>select {border-radius: 8px;}
    .stSlider>div>div>div>div {border-radius: 8px;}
    </style>
    """, unsafe_allow_html=True)

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
    with st.spinner('Generating profile...'):
        try:
            default_scale = load_scale(selected_scale)
            sequence = Sequence(sequence_input)
            profile = compute_profile(sequence, default_scale, window_size)

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(profile, linestyle='-', color="#1f77b4", linewidth=2)
            ax.set_ylabel('Hydrophobicity Score', fontsize=14, fontweight='bold')
            ax.set_xlabel('Position', fontsize=14, fontweight='bold')
            ax.set_title(f"Hydrophobic Profile ({get_scale_name(selected_scale)}, Window = {window_size})", fontsize=16, fontweight='bold')
            ax.grid(True, which='both', linestyle='--', linewidth=0.8, color='#cccccc')
            ax.tick_params(axis='both', which='major', labelsize=12)

            scatter = ax.scatter(range(len(profile)), profile, color=(0, 0, 0, 0), s=100)
            labels = []
            for i in range(window_size//2, len(profile)-window_size//2):
                residues = sequence.get_sequence()[i-window_size//2:i+window_size//2 + 1]
                label = f"{profile[i]:.2f} | {residues[:window_size//2]}<span style='color:red;'>{residues[window_size//2]}</span>{residues[window_size//2+1:]}"
                labels.append(label)
            # print(len(profile), len(labels))
            # for p, l in zip(profile, labels):
            #     print(p, l)
            tooltip = plugins.PointHTMLTooltip(scatter, labels)
            plugins.connect(fig, tooltip)

            fig.tight_layout(pad=2)

            fig_html = mpld3.fig_to_html(fig)
            components.html(fig_html, height=700)

            st.success('Profile generated successfully!')

            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=300)
            buf.seek(0)

            col1, col2 = st.columns([3, 1])

            with col1:
                default_info = sequence.info if sequence.info else "noinfo"
                filename = st.text_input(
                    "Download file name:",
                    value=f"hydroprofile_win{window_size}_{selected_scale}_{default_info}.png"
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
