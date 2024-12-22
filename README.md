This code is solely for implementing captions, input ipnutvideo.mp4 containing script as background audio MUST be provided.
Current Version of code serves to provide us control over how many words are displayed in a frame.
If you want to see the highlighting captions please use module from : https://github.com/unconv/captacity

What code does:
Input:
- Takes Video input that already contains the script text as audio
Output:
- Generates a video with captions, includes user controlled word limit transcribed directly from the audio embedded in the input video

PRE-REQ:
- Install required modules from requirement.txt in a venv
- Reduce python to 3.10
    ```python 
    python -m virtualenv -p path-to-python3.10-on-local-system venv
    ```
- Install ImageMagick from https://imagemagick.org/script/download.php#windows
- Copy the path to ImageMagick (wherever you installed it): 
    ```python
    r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"
    ```
- Go to the venv where you unstalled the modules
- Go to ```venv/Lib/site-packages/moviepy/config_defaults.py``` and hardcode the IMAGEMAGIC_BINARY
    ```python
    IMAGEMAGICK_BINARY = r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe" # earlier: os.getenv('IMAGEMAGICK_BINARY', 'auto-detect')
    ```
- Limit the number of words in the "__init__.py" --> captions = segment_parser.parse(......max_words_per_frame = "input number") --> line 129 in RAW code
- Change input, output and font paths
- Run "main.py"

TODO: 
- Try to implement highlighting of captions along with word limits.
- Word limit input in "generator.py" is being overwritten by word limit input in "__init__.py", try to fix
