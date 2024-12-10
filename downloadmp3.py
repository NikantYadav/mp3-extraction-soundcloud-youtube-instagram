import re
import os
import requests
import subprocess


def fncdownloadmp3():
    file_path = 'playlist.m3u8' 


    with open(file_path, 'r') as file:
        input_text = file.read()


    url_pattern = r'https?://[^\s]+'


    mp3_urls = re.findall(url_pattern, input_text)


    download_dir = "./mp3"
    os.makedirs(download_dir, exist_ok=True)


    def download_mp3(url, filename):
        try:
            response = requests.get(url)
            response.raise_for_status()  
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

        
    def create_ffmpeg_input_file(mp3_files, input_filename="files.txt"):
        with open(input_filename, 'w') as file:
            for mp3_file in mp3_files:
                file.write(f"file '{mp3_file}'\n")
        print(f"Created FFMPEG input file: {input_filename}")

    
    def merge_mp3_files(input_filename="files.txt", output_filename="output.mp3"):
        try:
            subprocess.run([
                "ffmpeg","-y","-f", "concat", "-safe", "0", "-i", input_filename,
                "-c", "copy", output_filename
            ], check=True)
            print(f"Merged MP3 files into: {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"FFMPEG error: {e}")


    def cleanup_files(files):
        for file in files:
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except OSError as e:
                print(f"Error deleting file {file}: {e}")
    
        
    def main():    
        downloaded_files = []
        for i, url in enumerate(mp3_urls, 1):
            filename = os.path.join(download_dir, f"segment_{i}.mp3")
            download_mp3(url, filename)
            downloaded_files.append(filename)
        
        
        create_ffmpeg_input_file(downloaded_files)

        
        merge_mp3_files(input_filename="files.txt", output_filename="final_song.mp3")

        
        os.remove("files.txt")
        print("Cleaned up temporary files.")
    
        cleanup_files(downloaded_files)

    try:
        main()
    except Exception as e:
        print(f"An error occured: {e}")


