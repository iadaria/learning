FROM golang:alpine

RUN mkdir /files
COPY hw.go main.go /files
WORKDIR /files
#RUN go build -o /files/hw hw.go
RUN go build -o /files/hw main.go hw.go
ENTRYPOINT ["/files/hw"]