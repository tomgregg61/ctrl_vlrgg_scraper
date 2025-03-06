import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def scrape_past_matches(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    matches = soup.find_all('a', class_='wf-card fc-flex m-item')
    
    match_data = []
    
    for match in matches:
        team1 = match.find('span', class_='m-item-team-name').get_text(strip=True)
        team2 = match.find_all('span', class_='m-item-team-name')[1].get_text(strip=True)
        
        score = match.find('div', class_='m-item-result').get_text(strip=True)
        
        date = match.find('div', class_='m-item-date').get_text(strip=True)

        match_data.append({
            "team1": team1,
            "team2": team2,
            "score": score,
            "date": date
        })
    
    return match_data

@app.route('/', methods=['GET'])
def get_matches():
    url = "https://www.vlr.gg/team/16630/yari-x-ctrl"
    match_data = scrape_past_matches(url)
    
    if match_data is None:
        return jsonify({"error": "Failed to retrieve data"}), 500
    
    return jsonify(match_data)

if __name__ == '__main__':
    app.run(debug=True)