This directory stores user uploaded media.
If site migration happens, do backup of this directory from live site.
And then restore into the new deployment site.
This is manual procedure.
e.g.
- upload archive media.tar.gz to Docker host server
- un-archive it by tar xzf media.tar.gz
- docker cp media/. django-container-id:/app/ulpa/media/
