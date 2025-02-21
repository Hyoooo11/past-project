import yt_dlp

# URL of the video to be downloaded
link = "https://www.youtube.com/watch?v=dv7djU1PAsk"  # Gangnam Style

# Set up the download options
ydl_opts = {
    'outtmpl': 'C:/Users/class/Downloads/%(title)s.%(ext)s',  # Download path
    'format': 'mp4',  # You can change the format to mp4 or any other available format
}

# Download the video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download([link])
        print("Video downloaded successfully!")
    except Exception as e:
        print(f"Error downloading video: {e}")
