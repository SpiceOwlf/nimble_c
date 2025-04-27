Python 3.10.13
macos 13.6.1

#Requirements:
1. Create a simple web app as a client.

2. Create a server that serves the web app.

3. The client should create a WebRTC(SDP) offer, and send it to the server over WebTransport. WebRTC and WebTransport must be used.

4. The server should handle the WebTransport request from the client/browser.

5. Once received the offer from WebTransport, the server should respond and send it back.

6. The server should spawn a worker thread/process to generate a continuous 2D image/frames of a ball bouncing across the screen, the frame rate should be configurable.

7. The server should consume generated frames from the worker thread/process and send it back over WebRTC with H.264 encoding.

8. Upon receiving the frame from the server, the web app should 
- display it in browser
- invoke a function to parse the frame and determine the current location of the ball center as x,y coordinates.

9. The web app should send the coordinates back to the server via both WebTransport.

10. The server should compute the error to the actual location of the ball in real time (not against the same frame), and send the error back via WebTransport.

11. The client should display the error in the browser.

12. The server should properly handle signals to gracefully shutdown.

13. Write unit tests for all functions.

14. Document all code and design decisions.
15. Include a screen capture (mp4, mkv, avi, etc.) of your application in action.

16. Compress the project directory and include your name in the filename. Do not post solutions publicly.

17. Deployment
- Make a docker image (Dockerfile) for the server
- Kubernetes
    Create kubernetes manifest yaml files for server deployment
    Docs for deploying it (consider using minikube/kind/k3s/microk8s etc.)





#learning source: 
https://medium.com/@fengliu_367/getting-started-with-webrtc-a-practical-guide-with-example-code-b0f60efdd0a7
message channel example for data
https://webrtc.github.io/samples/src/content/datachannel/channel/

Get started with webrtc:
https://web.dev/articles/webrtc-basics#toc-rtcdatachannel

Python AioRTC example:
https://aiortc.readthedocs.io/en/latest/examples.html
https://github.com/aiortc/aiortc/blob/main/examples/server/README.rst
https://medium.com/@malieknath135/building-a-real-time-streaming-application-using-webrtc-in-python-d34694604fc4


cv2:
https://www.geeksforgeeks.org/opencv-python-tutorial/
https://www.geeksforgeeks.org/python-image-blurring-using-opencv/
https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html
https://www.geeksforgeeks.org/circle-detection-using-opencv-python/

test
https://www.geeksforgeeks.org/unit-testing-python-unittest/
https://docs.python.org/3/library/unittest.html

#To start:
with pip install requirements.txt, 
python sender.py & python receiver.py in two local terminals

I created docker files for both, but they cannot talk to each other. I assume the port/network is not shared inside of docker.
May need a docker-compose/ docker network to resolve this 


docker build -t webrtc-receiver -f Dockerfile.receiver .
docker build -t webrtc-sender -f Dockerfile.sender .
docker run -p 8080:8080 webrtc-receiver
docker run -p 8081:8080 webrtc-sender

