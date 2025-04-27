initNimble Programming Challenge - 2025

Requirements:
1.Create a simple web app as a client.
2.Create a server that serves the web app.
3.The client should create a WebRTC(SDP) offer, and send it to the server over WebTransport. WebRTC and WebTransport must be used.
4.The server should handle the WebTransport request from the client/browser.
5.Once received the offer from WebTransport, the server should respond and send it back.
6.The server should spawn a worker thread/process to generate a continuous 2D image/frames of a ball bouncing across the screen, the frame rate should be configurable.
7.The server should consume generated frames from the worker thread/process and send it back over WebRTC with H.264 encoding.
8.Upon receiving the frame from the server, the web app should 
- display it in browser
- invoke a function to parse the frame and determine the current location of the ball center as x,y coordinates.
9.The web app should send the coordinates back to the server via both WebTransport.
10.The server should compute the error to the actual location of the ball in real time (not against the same frame), and send the error back via WebTransport.

11.The client should display the error in the browser.

12.The server should properly handle signals to gracefully shutdown.

13.Write unit tests for all functions.
14.Document all code and design decisions.
15.Include a screen capture (mp4, mkv, avi, etc.) of your application in action.
16.Compress the project directory and include your name in the filename. Do not post solutions publicly.
17.Deployment
- Make a docker image (Dockerfile) for the server
- Kubernetes
    Create kubernetes manifest yaml files for server deployment
    Docs for deploying it (consider using minikube/kind/k3s/microk8s etc.)





source: https://medium.com/@fengliu_367/getting-started-with-webrtc-a-practical-guide-with-example-code-b0f60efdd0a7
learn how this RTC works, and modify the media/text exchange process later for our ball bouncing frame

message channel for data
https://webrtc.github.io/samples/src/content/datachannel/channel/
get started with webrtc
https://web.dev/articles/webrtc-basics#toc-rtcdatachannel

example:https://github.com/aiortc/aiortc/blob/main/examples/server/README.rst