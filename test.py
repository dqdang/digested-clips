import uploader

clip = ["LCK_fighting_game_style", "LCK_fighting_game_style.mp4"]

youtube_mirror = uploader.upload({"title":clip[0], "file":clip[1]})

print(youtube_mirror)
