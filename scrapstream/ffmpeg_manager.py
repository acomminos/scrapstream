import subprocess
import shlex
from stream_settings import StreamSettings

### Manage the FFMpeg process that is streaming.
class FFMpegManager:

    command = "ffmpeg -f x11grab -s %(INPUT_WIDTH)dx%(INPUT_HEIGHT)d  -r %(FPS)d -i %(DISPLAY)s+%(INPUT_X)d,%(INPUT_Y)d -c:v libx264 -preset fast -pix_fmt yuv420p -s %(OUTPUT_WIDTH)dx%(OUTPUT_HEIGHT)d -threads 0 -f flv \"rtmp://live.twitch.tv/app/%(STREAM_KEY)s\""
    
    def get_command(self):
        substituted = FFMpegManager.command % { 'INPUT_WIDTH': StreamSettings.capture_width,
                                  'INPUT_HEIGHT': StreamSettings.capture_height,
                                  'FPS': StreamSettings.frame_rate,
                                  'DISPLAY': ':0.0',
                                  'INPUT_X': StreamSettings.capture_x,
                                  'INPUT_Y': StreamSettings.capture_y,
                                  'OUTPUT_WIDTH': StreamSettings.output_width,
                                  'OUTPUT_HEIGHT': StreamSettings.output_height,
                                  'STREAM_KEY': StreamSettings.stream_key }
        return substituted

    def start(self):
        ffmpeg_command = shlex.split(self.get_command())
        self.process = subprocess.Popen(ffmpeg_command)

    def stop(self):
        if self.process is not None and self.process.returncode is None:
            self.process.terminate()
