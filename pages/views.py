# pages/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .forms import TickerForm
from moviepy.editor import VideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import tempfile


def make_frame(t, ticker_text, font, img_size, duration):
    img = Image.new('RGBA', img_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    text_width = draw.textlength(ticker_text, font=font)
    text_height = font.size
    speed = (text_width + img_size[0]) / duration

    x = img_size[0] - (t * speed) % (text_width + img_size[0])
    y = (img_size[1] - text_height) / 2

    draw.text((x, y), ticker_text, font=font, fill='black')

    return np.array(img.convert('RGB'))


def runtext(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker_text = form.cleaned_data['text']
            form.save()

            duration = 3
            font_size = 100
            font_path = os.path.join('static', 'fonts', 'LiberationSans-Regular.ttf')
            font = ImageFont.truetype(font_path, font_size)
            img_size = (100, 100)

            clip = VideoClip(lambda t: make_frame(t, ticker_text, font, img_size, duration), duration=duration)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            clip.write_videofile(temp_file.name, fps=24)

            with open(temp_file.name, 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="ticker.mp4"'
                return response
    else:
        form = TickerForm()
    return render(request, 'pages/runtext.html', {'form': form})
