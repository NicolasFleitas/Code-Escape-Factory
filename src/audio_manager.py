import pygame
import os

class AudioManager:
    def __init__(self):
        self.victoria_sound = None
        self.derrota_sound = None
        self.alarma_sound = None
        
        # Banderas de control de audio (se mantienen aquí pero se pueden sincronizar)
        self.victoria_sound_played = False
        self.victoria_sound_start_time = None
        self.derrota_sound_played = False
        self.derrota_sound_start_time = None
        self.alarma_10s_played = False
        self.alarma_5s_played = False

    def setup(self):
        """Inicializa y carga todos los recursos de audio."""
        pygame.mixer.init()
        # Música de ambiente
        try:
            ruta_audio = os.path.join("src", "assets", "audio", "ambiente.mp3")
            pygame.mixer.music.load(ruta_audio)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"No se pudo cargar el audio de ambiente: {e}")

        # Efectos de sonido
        self.victoria_sound = self._load_sound("ganaste.mp3", 0.7)
        self.derrota_sound = self._load_sound("perdiste.mp3", 0.7)
        self.alarma_sound = self._load_sound("alarma3.mp3", 0.6)

    def _load_sound(self, filename, volume):
        """Helper para cargar sonidos de forma segura."""
        try:
            path = os.path.join("src", "assets", "audio", filename)
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"No se pudo cargar el sonido {filename}: {e}")
            return None

    def handle_alarms(self, tiempo_restante):
        """Control de sonidos de alarma."""
        if not self.alarma_sound:
            return

        # Alarma a los 10 segundos
        if 5 < tiempo_restante <= 10 and not self.alarma_10s_played:
            self.alarma_sound.play()
            self.alarma_10s_played = True
        
        # Alarma a los 5 segundos
        if 0 < tiempo_restante <= 5 and not self.alarma_5s_played:
            self.alarma_sound.play()
            self.alarma_5s_played = True

    def check_sound_completion(self, start_time, sound):
        """Helper para verificar si un sonido terminó de reproducirse."""
        if start_time is None or not sound:
            return False

        duration = sound.get_length() * 1000
        if pygame.time.get_ticks() - start_time >= duration:
            pygame.mixer.music.unpause()
            return True
        return False
