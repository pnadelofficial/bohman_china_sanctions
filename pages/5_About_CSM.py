import streamlit as st
import utils

st.title('About the China Sanctions Monitor')
utils.apply_css()

st.write("""CSM is managed by [Victor Ferguson](https://www.victoraferguson.com/). The database is part of an ongoing joint research project together with Viking Bohman and [Audrye Wong](https://www.audryewong.com/). 

While we regularly update the database with a view to maintaining a comprehensive record of PRC sanctions, we cannot guarantee – nor do we claim – it is exhaustive. This is particularly true for earlier years when China’s actions in this space were less closely monitored, and for ‘informal’ sanctions, which are rarely announced publicly and sometimes contested.
 
We collect data from a combination of official Chinese sources and international reporting. Publicly announced sanctions, such as those published by the Ministry of Commerce or Ministry of Foreign Affairs, are straightforward to track. Unacknowledged sanctions, including state-encouraged consumer boycotts, opaque trade restrictions, or selective regulatory enforcement, are more difficult to identify. To capture these, we rely on media reporting, enforcement patterns, and how China’s actions have been  interpreted internationally. If multiple, credible sources conclude that a government-initiated or -encouraged economic restriction is plausibly motivated by political or security objectives, we include it.
         
Rather than structuring the database around observations of sanctions ‘[episodes](https://journals.sagepub.com/doi/full/10.1177/07388942241248274)’ (e.g. China–Japan 2010; China–South Korea 2016), our unit of analysis is individual restrictions. The advantage of this approach is that it allows us to present a more granular picture of how China’s practical use of sanctions varies over time and space.

For his exceptional work in structuring the data and developing the visualizations that power this platform, we are extremely grateful to Peter Nadel.       
""")

st.markdown("<footer><small>Assembed by Peter Nadel | Tufts University | Tufts Technology Services | Research Technology </small></footer>", unsafe_allow_html=True)
