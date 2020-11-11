import os

engine = open(os.path.dirname(__file__) + '/../src/engine.py', 'r')
engine_code = ''.join(engine.readlines())
engine.close()

gui = open(os.path.dirname(__file__) + '/../src/gui.py', 'r')
gui_code = ''.join(gui.readlines())
gui.close()


# Move both codes' content into index.html
index = open('index.html', 'r')
lines = index.readlines()
index.close()

beg = lines.index('        <script type="text/python">\n')
end = lines.index('        </script>\n')

lines = lines[:beg+1] + [engine_code + '\n\n' + gui_code] + lines[end:]

with open(os.path.dirname(__file__) + '/../index.html', 'w') as f:
    f.write(''.join(lines))
