import cv2
import requests

def identify_video(file_path):
    # extract middle frame
    cap = cv2.VideoCapture(file_path)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    middle = int(total_frames // 2)
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle)
    success, frame = cap.read()
    cap.release()
    
    if not success:
        return None
    
    cv2.imwrite("temp/frame.jpg", frame)
    
    # send to trace.moe
    with open("temp/frame.jpg", "rb") as f:
        response = requests.post("https://api.trace.moe/search", files={"image": f})
    
    data = response.json()
    
    if not data["result"]:
        return None
    
    top_result = data["result"][0]
    similarity = top_result["similarity"]
    
    if similarity < 0.8:
        return None
    
    anilist_id = top_result["anilist"]
    return get_anime_title(anilist_id)


def get_anime_title(anilist_id):
    query = """
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            title {
                english
                romaji
            }
        }
    }
    """
    
    response = requests.post(
        "https://graphql.anilist.co",
        json={"query": query, "variables": {"id": anilist_id}}
    )
    
    data = response.json()
    title = data["data"]["Media"]["title"]["english"]
    
    if not title:
        title = data["data"]["Media"]["title"]["romaji"]
    
    return title