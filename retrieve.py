import requests

def get_all_summits_data():
    """
    This function retrieves all summits data from the SOTA API.
    
    Returns:
    list: A list of dictionaries containing summit data (lat, lon, altitude, name, points)
    """
    try:
        # Make GET request to SOTA API endpoint
        response = requests.get("https://api.sota.org.uk/api/summits")
        
        # Check if request was successful
        if response.status_code != 200:
            raise Exception("Failed to retrieve summits data")
        
        # Extract summit data from response
        summits_data = response.json()
        
        # Return list of summit data
        return summits_data
    except Exception as e:
        # Log the error
        #print(f"Error: {e}")
        print("Error: ")
        return []

summits_data = get_all_summits_data()
print(summits_data)
