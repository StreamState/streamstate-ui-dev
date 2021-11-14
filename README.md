# Dev environment for testing spark streaming

`sudo docker build . -t dev`

`sudo docker run -p 3000:3000 dev`

# If not authenticated to gcloud:

`gcloud auth configure-docker us-central1-docker.pkg.dev`