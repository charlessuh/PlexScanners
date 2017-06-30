import re, os, os.path
import VideoFiles

SeriesScanner = __import__('Plex Series Scanner')
MovieScanner = __import__('Plex Movie Scanner')

episode_regexp = '(?P<show>.*?)' + SeriesScanner.date_regexps[0]

# Scans through files, and add to the media list.
def Scan(path, files, mediaList, subdirs, language=None, root=None):

    # Scan for video files.
    VideoFiles.Scan(path, files, mediaList, subdirs, root)

    filesToRemove = []

    for i in files:
        file = os.path.basename(i).lower()

        if re.match(episode_regexp, file):
            filesToRemove.append(i)
        else:
            for j in VideoFiles.source_dict['dtv']:
                if j in file:
                    filesToRemove.append(i)
                    break

    # Uniquify and remove.
    for i in list(set(filesToRemove)):
       files.remove(i)

    MovieScanner.Scan(path, files, mediaList, subdirs, language, root)
