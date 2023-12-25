import requests, base64, os, re, textwrap

# Code from https://github.com/oscie57/tiktok-voice

voices = [
    # ENGLISH VOICES
    "en_au_001",  # English AU - Female
    "en_au_002",  # English AU - Male
    "en_uk_001",  # English UK - Male 1
    "en_uk_003",  # English UK - Male 2
    "en_us_001",  # English US - Female (Int. 1)
    "en_us_002",  # English US - Female (Int. 2)
    "en_us_006",  # English US - Male 1
    "en_us_007",  # English US - Male 2
    "en_us_009",  # English US - Male 3
    "en_us_010",  # English US - Male 4
    # AMERICA VOICES
    "es_mx_002",  # Spanish MX - Male
    "br_001",  # Portuguese BR - Female 1
    "br_003",  # Portuguese BR - Female 2
    "br_004",  # Portuguese BR - Female 3
    "br_005",  # Portuguese BR - Male
    # ASIA VOICES
    "id_001",  # Indonesian - Female
    "jp_001",  # Japanese - Female 1
    "jp_003",  # Japanese - Female 2
    "jp_005",  # Japanese - Female 3
    "jp_006",  # Japanese - Male
    "kr_002",  # Korean - Male 1
    "kr_003",  # Korean - Female
    "kr_004",  # Korean - Male 2
    # OTHER
    "en_male_narration"  # narrator
    "en_male_funny"  # wacky
    "en_female_emotional",  # peaceful
]


def tts(
    session_id: str,
    text_speaker: str = "en_us_002",
    req_text: str = "TikTok Text To Speech",
    filename: str = "voice.mp3",
):
    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        "User-Agent": "com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)",
        "Cookie": f"sessionid={session_id}",
    }
    url = f"https://api16-normal-c-useast2a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers=headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]

    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log,
    }

    print(output_data)
    return output_data


def batch_create(filename: str = "voice.mp3"):
    out = open(filename, "wb")

    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
        return sorted(data, key=alphanum_key)

    for item in sorted_alphanumeric(os.listdir("./TTS/batch/")):
        filestuff = open("./TTS/batch/" + item, "rb").read()
        out.write(filestuff)

    out.close()


def long_tts(session, text_speaker, textfile, filename):
    req_text = open(textfile, "r", errors="ignore", encoding="utf-8").read()
    chunk_size = 200
    textlist = textwrap.wrap(
        req_text, width=chunk_size, break_long_words=True, break_on_hyphens=False
    )

    os.makedirs("./TTS/batch/")

    for i, item in enumerate(textlist):
        tts(session, text_speaker, item, f"./TTS/batch/{i}.mp3")

    batch_create(filename)

    for item in os.listdir("./TTS/batch/"):
        os.remove("./TTS/batch/" + item)

    os.removedirs("./TTS/batch/")

    return
