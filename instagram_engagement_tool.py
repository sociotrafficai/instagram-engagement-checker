# Instagram Engagement Rate Calculator (Simple CLI version)

import requests
from bs4 import BeautifulSoup
import re

def get_instagram_post_data(username):
    url = f"https://www.picuki.com/profile/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("❌ Failed to load profile. Try a public profile only.")
        return None

    soup = BeautifulSoup(res.text, 'html.parser')

    stats = soup.find_all('span', class_='number')
    if len(stats) < 3:
        print("❌ Couldn't extract enough data. Profile may be private or blocked.")
        return None

    try:
        posts = int(stats[0].get_text().replace(',', ''))
        followers = int(stats[1].get_text().replace(',', ''))
        following = int(stats[2].get_text().replace(',', ''))

        like_tags = soup.find_all("div", class_="photo")
        total_likes = 0
        count = 0

        for tag in like_tags[:10]:  # check latest 10 posts
            like_match = re.search(r'(\d+(,\d+)*)(?= likes)', tag.text)
            if like_match:
                likes = int(like_match.group(1).replace(',', ''))
                total_likes += likes
                count += 1

        if count == 0:
            print("❌ No like data found in recent posts.")
            return None

        avg_likes = total_likes // count
        engagement_rate = (avg_likes / followers) * 100 if followers > 0 else 0

        return {
            "username": username,
            "followers": followers,
            "avg_likes": avg_likes,
            "engagement_rate": round(engagement_rate, 2)
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    username = input("Enter public Instagram username: ").strip()
    data = get_instagram_post_data(username)
    if data:
        print("\n✅ Instagram Engagement Summary")
        print("Username:", data["username"])
        print("Followers:", data["followers"])
        print("Average Likes (last 10 posts):", data["avg_likes"])
        print("Engagement Rate:", f'{data["engagement_rate"]}%')
