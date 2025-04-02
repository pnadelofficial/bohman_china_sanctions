import streamlit as st  
import utils

st.image("bohman cms logo.png")

utils.apply_css()

st.write("""
### Welcome to the China Sanctions Monitor
 
This beta website serves as a resource for tracking how the People’s Republic of China uses economic restrictions to achieve political and security objectives over time. The data presented here underpins the analysis featured in our [Substack newsletter](https://chinasanctionsmonitor.substack.com/), where we provide regular updates and analysis on China’s latest actions in this space.
 
The data allows users to visualize the full spectrum of PRC sanctions, ranging from informal sanctions such as state-supported consumer boycotts against foreign businesses to formal sanctions like asset freezes, entry bans, and export controls. You can read more about how we collect data in the ‘About CSM’ section.
 
Please use the tabs on the left-hand side to access specific data, generate customized graphs, and explore our searchable repository of targeted individuals and entities. We regularly update the database and will introduce additional features over time.
 
We value your feedback––please let us know if you spot any inaccuracies in the data or  issues with the visualizations. For questions or suggestions, don’t hesitate to reach out to us at chinasanctionsmonitor@gmail.com.
""".strip())

st.markdown("<footer><small>Assembed by Peter Nadel | Tufts University | Tufts Technology Services | Reserch Technology </small></footer>", unsafe_allow_html=True)