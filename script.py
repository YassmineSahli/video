import moviepy.editor as mp
import numpy as np
import cv2
def add_text_to_frame(frame, text, position=(50, 50), font_scale=1, font_color=(255, 255, 255), thickness=2):
    """Ajoute du texte à une frame."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = position[0]
    text_y = position[1] + text_size[1]
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)
    return frame
def process_video_with_script(video_path, script, output_path):
    """Traite la vidéo en ajoutant le script mot par mot pendant les segments audio."""
    video = mp.VideoFileClip(video_path)  # Charger la vidéo
    audio = video.audio  # Extraire l'audio

    # Diviser l'audio en segments basés sur le silence
    sound_segments = split_audio_on_silence(audio)
    
    # Diviser le script en mots
    words = script.split()

    # Calculer la durée totale des segments sonores
    total_sound_duration = sum(end - start for start, end in sound_segments)
    if total_sound_duration == 0:
        raise ValueError("Aucune partie sonore détectée dans la vidéo.")
    
    # Calculer le temps moyen par mot
    time_per_word = total_sound_duration / len(words)
    word_index = 0

    # Créer un nouveau clip vidéo avec le texte ajouté
    def make_frame(t):
        nonlocal word_index
        frame = video.get_frame(t)
        for start, end in sound_segments:
            if start <= t <= end:
                elapsed_time = t - start
                current_word_index = int(elapsed_time // time_per_word)
                if word_index + current_word_index < len(words):
                    word = words[word_index + current_word_index]
                    frame = add_text_to_frame(frame, word, (50, 50))
                if t >= end:
                    word_index += current_word_index + 1
                break
        return frame

    new_video = video.fl(make_frame)  # Appliquer la fonction make_frame sur chaque frame
    
    # Combiner avec l'audio original
    new_video = new_video.set_audio(audio)
    new_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

