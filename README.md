This is very much a "works on my machine" implementation, to be used as an example.

It works on OSX, you just install requirements.

    pip install -r requirements.txt

However, let's remember the free python binding basically just interfaces with chatgpt in a headless browser
That means, installing that part is going to be a pain

Make sure to run:


    chatgpt install

(More details here)[https://github.com/mmabrouk/chatgpt-wrapper]

To run the script:

     python lulz.py

It's slow. If you want a fast one I suggest writing an OpenAI GPT model
