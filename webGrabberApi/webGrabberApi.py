from flask import Flask, send_from_directory
from .webGrabberController import webGrabber
# from playwright.async_api import async_playwright
app = Flask(__name__)


@app.route('/api/startWebGrabber', methods=['GET'])
async def runWebGRabber():
    fileDetails = await webGrabber()
    # print(f"API File Name: {fileDetails['file_name']}\n")
    return send_from_directory(fileDetails['file_path'], fileDetails['file_name'], as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Important: host='0.0.0.0' for external access