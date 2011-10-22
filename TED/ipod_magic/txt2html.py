import os, glob

html = u"""\
<!DOCTYPE html>
<html>
<head><title>%(title)s</title>
<link type="text/css" href="../../css/ted.css" rel="stylesheet"></link>
</head>
<body>
<div class="title">
    <h1>%(title)s</h1>
</div>
%(sentence_list)s
<div class="ref">
<p><a href="%(video)s" target="_new">여기</a>에서 내용을 보면서 들을 수 있습니다.</p>
</div>
</body>
</html>
"""

sentence_div = u"""\
<div class="sentence">
    <audio src="%(mp3)s" controls="controls" loop="true"></audio>
    <p class="english">%(eng)s</p>
    <p class="korean">%(kor)s</p>
</div>"""

def readline(f):
    line = f.readline()
    if not line:
        return None
    return line.decode("euc-kr").strip()

def _txt2html():
    mp3s = glob.glob("*.mp3")
    sentences = []
    with open("script.txt") as f:
        title = readline(f)
        output = readline(f)
        video = readline(f)
        while True:
            eng = readline(f)
            if eng == None:
                break
            if not eng:
                continue
            kor = readline(f)
            sentences.append((eng, kor))
            
    sentence_list = []
    for mp3, (eng, kor) in zip(mp3s, sentences):
        sentence_list.append(sentence_div % {"mp3": mp3, "eng": eng, "kor": kor})
        
    with open(output, "wb") as f:
        s = html % {
            "title": title,
            "sentence_list": u"\n".join(sentence_list),
            "video": video}
        f.write(s.encode("euc-kr"))
        
def txt2html(path):
    try:
        cwd = os.getcwd()
        os.chdir(path)
        _txt2html()
    finally:
        os.chdir(cwd)
        
if __name__ == "__main__":
    import sys
    if 1 < len(sys.argv):
        path = sys.argv[1]
        print path
        txt2html(path)
    else:
        print "Usage: txt2html.py <dir>"