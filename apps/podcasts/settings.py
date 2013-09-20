

SKILL_CHOICES = (
    ('AV', 'A/V',),
    ('JO', 'Journalism',),
    ('PR', 'Programming',),
)

MEDIA_EMBED_OPTION = {
    'youtube' : '<iframe width="533" height="400" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>',
    'blip' : '<embed src="%s" type="application/x-shockwave-flash" width="533" height="400" allowscriptaccess="always" allowfullscreen="true"></embed>',
    'mp3' : '<audio controls class="resume-audio"><source src="%s" type="audio/mpeg">Get a modern browser, dum-dum.</audio>',
    'png' : '<img src="%s" height="480" width="385">',
    'jpg' : '<img src="%s" height="480" width="385">',
    'gif' : '<img src="%s" height="480" width="385">',}

