import streamlit as st  
import utils

st.image("bohman cms logo.png")

utils.apply_css()

st.write("""
### Welcome to the China Sanctions Monitor.

This beta website serves as a resource for tracking how the People’s Republic of China’s uses economic restrictions to achieve foreign policy objectives. The data presented here underpins the analysis featured in our Substack newsletter, where we provide regular updates and analysis on China’s latest actions in this space. 

The database is designed to visualize the full spectrum of PRC sanctions, ranging from informal sanctions such as state-supported consumer boycotts against foreign businesses to formal sanctions like asset freezes, entry bans, and export controls. You can read more about how we collect data in the about section.

Please use the tabs on the left-hand side to access specific data, generate customized graphs, and explore our searchable repository of targeted individuals and entities. We regularly update the database and will introduce additional features over time.

We value your feedback––please let us know if you spot any inaccuracies or errors in the data or issues with the vizualisations. For questions or suggestions, don’t hesitate to reach out to us at chinasanctionsmonitor@gmail.com. 

If you use this data, please cite it accordingly: [China Sanctions Monitor](www.chinasanctionsmonitor.com). 

We are grateful to Peter Nadel for his exceptional work in structuring the data and developing the visualizations that power this platform.
""".strip())