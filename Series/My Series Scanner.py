import re, os, os.path
import Media, VideoFiles, Utils

SeriesScanner = __import__('Plex Series Scanner')

regexp = '(?P<show>.*?)(?P<year>2[0-9]{3})[^0-9a-zA-Z]+(?P<month>[0-9]{2})[^0-9a-zA-Z]+(?P<day>[0-9]{2})([^0-9]|$)'

# Scans through files, and add to the media list.
def Scan(path, files, mediaList, subdirs, language=None, root=None):

    filesToRemove = []

    # Scan for video files.
    VideoFiles.Scan(path, files, mediaList, subdirs, root)

    # Take top two as show/season, but require at least the top one.
    paths = Utils.SplitPath(path)

    if len(paths) == 1 and len(paths[0]) == 0:

        # Run the select regexps we allow at the top level.
        for i in files:
            file = os.path.basename(i)
            match = re.search(regexp, file, re.IGNORECASE)
            if match:

                # Extract data.
                show = match.group('show')
                year = int(match.group('year'))
                month = int(match.group('month'))
                day = int(match.group('day'))

                # Clean title.
                name, _ = VideoFiles.CleanName(show)
                if len(name) > 0:

                    # Use the year as the season.
                    tv_show = Media.Episode(name, year, None, None, None)
                    tv_show.released_at = '%d-%02d-%02d' % (year, month, day)
                    tv_show.parts.append(i)
                    mediaList.append(tv_show)
    
                    filesToRemove.append(i)

    # Uniquify and remove.
    for i in list(set(filesToRemove)):
        files.remove(i)

    SeriesScanner.Scan(path, files, mediaList, subdirs, language, root)
