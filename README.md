# arvapy

REST API to implement the backend features of ARoundVision project

### Docker Image

To build the docker image download the folder from:

`https://myipleiria-my.sharepoint.com/:f:/g/personal/joao_m_carreira_ipleiria_pt/EitXZ-VgM1RGpLuFnRkcX10B4XoMnq7VhxQSoShCYDgbXQ`

and put it inside the docker folder along with the Dockerfile.

Then run inside the docker folder in order to build the docker image:

`docker build . -t arvapy`


Finally, run use the container using:

`docker-compose up`


### Documentation

A LaTeX document is presented in the `doc` folder with a description of the 
concept of this API and the relevant REST API functions to use.

Build it using:

`latexmk`
or
`pdflatex -interaction=nonstopmode --shell-escape doc.tex`
