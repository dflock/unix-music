#!/usr/bin/env python

""" Extracts album art from an MP3 file.

    Album art is assumed to be in JPEG format.

    Usage: apic-extract mp3-filename [jpg-filename]
    (the default value for jpg-filename is "albumart.jpg")

    Dependencies: mutagen.mp3

    You can also import this as a module (rename it first?) and call
    apic_extract yourself.
"""

import os
import sys
import mutagen.mp3


def apic_extract(mp3, jpg=None):
    """Extracts album art from a given MP3 file.  Output is raw JPEG data.

    jpg (optional) specifies a filename to write the image to instead of returning
    it.  Returns True if this is specified.

    If more than one artwork frame exists, each will br output to a separate file.

    Returns False if mp3 can't be opened, and None if no art was found.
    """
    try:
        tags = mutagen.mp3.Open(mp3)
    except:
        return False

    data = []
    for i in tags:
        if i.startswith("APIC"):
            data.append(tags[i].data)

    print '{} images found.'.format(len(data))

    if not data:
        return None
    if jpg is not None:
        count = 1
        jpg_basename = os.path.splitext(jpg)[0]
        mp3_basename = os.path.splitext(mp3)[0]
        for pic in data:
            out = open('{}-{}-{}.jpg'.format(mp3_basename, jpg_basename, count), "w")
            out.write(pic)
            out.close()
            print '{}'.format(out.name)
            count += 1
        return True
    return data


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: %s mp3-filename [jpg-filename]" % os.path.basename(sys.argv[0])
        print "(the default value for jpg-filename is \"[mp3-filename]-albumart.jpg\")"
        sys.exit(2)
    mp3_filename = sys.argv[1]
    jpg_filename = "albumart.jpg"
    if len(sys.argv) == 3:
        jpg_filename = sys.argv[2]
    status = apic_extract(mp3_filename, jpg_filename)
    if status is False:
        print "\"%s\" could not be opened or is not a valid MP3 file" % mp3_filename
    elif status is None:
        print "\"%s\" does not contain artwork" % mp3_filename
