from subprocess import Popen, PIPE
from os import getenv
import shlex
import stream_settings

### Manage the FFMpeg process that is streaming.
class FFMpegManager:

    command = "ffmpeg -f x11grab -s %(INPUT_WIDTH)dx%(INPUT_HEIGHT)d -r %(FPS)d -i %(DISPLAY)s+%(INPUT_X)d,%(INPUT_Y)d -c:v libx264 -preset fast -pix_fmt yuv420p -s %(OUTPUT_WIDTH)dx%(OUTPUT_HEIGHT)d -c:a libmp3lame -ar 44100 -threads 0 -bufsize 512k -f flv \"rtmp://live.twitch.tv/app/%(STREAM_KEY)s\""
    input_file = " -i \"%(INPUT_FILE)s\""
    video_overlay = "overlay=%(OVERLAY_X)d:%(OVERLAY_Y)d"
    audio_pulse = " -f pulse -ac 2 -i default"
    audio_custom_file = " -i \"%(AUDIO_FILE)s\""

    def __init__(self):
        self.process = None

    def get_command(self):
        config = stream_settings.get_config()
        substituted = FFMpegManager.command % { 
                                  'INPUT_WIDTH': int(config['capture_width']),
                                  'INPUT_HEIGHT': int(config['capture_height']),
                                  'FPS': int(config['frame_rate']),
                                  'DISPLAY': getenv('DISPLAY'),
                                  'INPUT_X': int(config['capture_x']),
                                  'INPUT_Y': int(config['capture_y']),
                                  'OUTPUT_WIDTH': int(config['output_width']),
                                  'OUTPUT_HEIGHT': int(config['output_height']),
                                  'STREAM_KEY': config['stream_key'] }
        if config['audio_source_id'] == 'microphone':
            substituted += FFMpegManager.audio_pulse # TODO add support for ALSA, input source selection
        elif config['audio_source_id'] == 'file':
            substituted += FFMpegManager.audio_custom_file % {'AUDIO_FILE': config['audio_file'] }

        if len(config['overlays']) > 0:
            for overlay in config['overlays']:
                substituted += FFMpegManager.input_file % { 'INPUT_FILE': overlay['file'] }

            substituted += " -filter_complex \""
            for i, overlay in enumerate(config['overlays']):
                substituted += FFMpegManager.video_overlay % {'OVERLAY_X': overlay['x'], 'OVERLAY_Y': overlay['y'] }
                if i < len(config['overlays'])-1:
                    substituted += ","
            substituted += "\""

        return substituted

    def start(self):
        ffmpeg_command = self.get_command()
        ffmpeg_split_command = shlex.split(ffmpeg_command)
        print("Running FFMpeg: " , ffmpeg_command)
        self.process = Popen(ffmpeg_split_command, stdout=PIPE, stderr=PIPE)

    def stop(self):
        if self.process is not None and self.process.returncode is None:
            self.process.kill()
            #self.process.poll()
