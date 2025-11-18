import streamlit as st
import gpxpy
import gpxpy.gpx
import pandas as pd

# --- BIT 1 & 2: The "Engine" ---
# Let's put all our data-parsing logic into one clean function.
# This function takes one thing (the uploaded file) and returns one thing (the data table).
def parse_gpx(gpx_file):
    """
    Parses an uploaded GPX file and returns a Pandas DataFrame.
    """
    points_list = []
    
    # gpxpy.parse() can read the uploaded file object directly
    gpx = gpxpy.parse(gpx_file)

    # Loop through all the tracks, segments, and points
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # Store each point's data in our list
                points_list.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time
                })
    
    # Finally, convert the full list into a DataFrame
    return pd.DataFrame(points_list)


# --- BIT 3 & 4: The "Web App" ---
# This is our main function that Streamlit will run.
def main():
    """
    Defines the main layout and logic for the Streamlit web app.
    """
    
    # First, set up the page title and a simple intro
    st.set_page_config(page_title="GPX File Analyzer", page_icon="🗺️")
    st.title('GPX File Analyzer 🗺️')
    st.write("Upload your GPX file, and this app will display its data and a map of the route.")

    # Create the file uploader. This is the main interactive part.
    uploaded_file = st.file_uploader("Choose a GPX file", type="gpx")

    # Now, let's check if the user has actually uploaded a file
    if uploaded_file is not None:
        
        # If they have, put a "spinner" on the screen so they know we're working
        with st.spinner('Parsing file and crunching numbers...'):
            try:
                # Call our "engine" function to do the hard work
                df = parse_gpx(uploaded_file)

                # Check if the function actually found any data
                if df.empty:
                    st.warning("No track points found in this GPX file.")
                else:
                    # If we have data, show the results!
                    st.success(f"Successfully collected {len(df)} data points!")
                    
                    st.header("Data from your file:")
                    st.dataframe(df)
                    
                    st.header("Route map:")
                    st.map(df)

            except Exception as e:
                # If anything goes wrong during parsing, tell the user
                st.error(f"An error occurred: {e}")
                st.error("This might not be a valid GPX file.")
                
    else:
        # If no file is uploaded yet, just show a helpful message
        st.info("Please upload a GPX file to get started.")

# This is the standard "entry point" for a Python script.
# It just tells the computer to run our 'main()' function.
if __name__ == "__main__":
    main()