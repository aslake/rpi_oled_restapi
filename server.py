"""
REST-API server for Raspberry Pi OLED screen.
Endpoint for sending text to screen.

API documentation served from port 5000.

Aslak Einbu 2022
"""
from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from flask_cors import CORS
from PIL import Image
from PIL import ImageFont

import time

from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from luma.core.render import canvas
from luma.core.virtual import terminal

serial = spi(device=0, port=0)
device = sh1106(serial)
term = terminal(device)

font_default = ImageFont.truetype("./tiny.ttf",7)

header_text = ""
body_text = []


def show_image(filename, rotate="False", background="white"):
    img_path = f"./{filename}"
    if rotate == "True":
        rott= True
    else:
        rott= False

    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    background = Image.new("RGBA", device.size, background)
    posn = ((device.width - logo.width) // 2, 0)
    
    if rott:
        for angle in range(0, 360, 2):
            rot = logo.rotate(angle, resample=Image.BILINEAR)
            img = Image.composite(rot, fff, rot)
            background.paste(img, posn)
            device.display(background.convert(device.mode))
    
    else:
        rot = logo.rotate(0, resample=Image.BILINEAR)
        img = Image.composite(rot, fff, rot)
        background.paste(img, posn)
        device.display(background.convert(device.mode))
    

def write_oled():
    """ Updating OLED screen. """
    global body_text, header_text
    with canvas(device) as draw:
        body_start_line = 0
        if header_text != "":
            draw.text((0,0), header_text, fill="white")
            draw.text((0,5), "-"*64, fill="white")
            body_start_line = 1
        y=1 + body_start_line
        for line in body_text:
            x=0
            for letter in line:
                if x>30:
                    x=0
                draw.text((x*6,y*10), letter, fill="white")#, font=font_default)
                x=x+1
            y=y+1
            if y> 5:
                body_text=[]

term.clear()
term.println("API waiting for input")
term.println("endpoint at port 5000")
time.sleep(5)
show_image('logo.png')

app = Flask(__name__)
CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
                         'Access-Control-Allow-Headers',
                         'Access-Control-Allow-Methods'])

api = Api(app, version='0.5', title='RPI onboard LED Display control',
    description='REST API for populating Raspberry Pi OLED screen.')

ns = api.namespace('screen', description='available api endpoints')

@ns.route('/body')
@ns.param('text', 'The input text.')
class Body(Resource):
    """ Inputs screen body text line"""
    @api.doc(params={'text': {'in': 'query', 'description': 'OLED body text.', 'default': "Body text line in  ->|"}})

    def get(self):
        """ Write body text line to OLED screen"""
        global header_text, body_text
        args = reqparse.request.args
        body_text.append(args['text'])
        if len(body_text) > 5:
            del body_text[0]
        write_oled()
        return f"Message text written to screen:{args['text']}."

@ns.route('/header')
@ns.param('text', 'The input text.')
class Header(Resource):
    """ Inputs screen header text """
    @api.doc(params={'text': {'in': 'query', 'description': 'OLED header text.', 'default': "HEADER TEXT"}})

    def get(self):
        """ Write header text to OLED screen """
        global header_text, body_text
        args = reqparse.request.args
        header_text= args['text']
        write_oled()
        return f"Header text written to screen:{header_text}."


@ns.route('/message')
@ns.param('text', 'The input text.')
class Message(Resource):
    """ Enters message in middle of screen """
    @api.doc(params={'text': {'in': 'query', 'description': 'OLED message text.', 'default': "Message!"}})

    def get(self):
        """ Write message tect to OLED screen"""
        args = reqparse.request.args
        message = args['text']
        with canvas(device) as draw:    
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10,20), message, fill="white")
        return f"Message text written to screen:{message}."


@ns.route('/image')
#@ns.param('text', 'The input text.')
class Show_image(Resource):
    """ Shows image on screen """
    @api.doc(params={'filename': {'in': 'query', 'description': 'Image filename.', 'default': 'logo.png'},
                     'rotate': {'in': 'query', 'description': 'Rotate image?', 'default': "False"},
                     'background': {'in': 'query', 'description': 'Background color.', 'default': "white"}})

    def get(self):
        """ Write image to OLED screen """
        args = reqparse.request.args
        show_image(args['filename'], args['rotate'], args['background']) 
        return f"Image written to screen:'{args['filename']}'"


@ns.route('/clearscreen')
class Clearscreen(Resource):
    """ Clears the screen """

    def get(self):
        """ Clears OLED screen """
        global body_text, header_text
        body_text = []
        header_text = ""
        write_oled()
        term.clear()
        return f"Screen cleared."


@ns.route('/clearbody')
class Clearbody(Resource):
    """ Clears the body text """

    def get(self):
        """ Clears body text """
        global body_text
        body_text = []
        write_oled()
        return f"Body text cleared."



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
