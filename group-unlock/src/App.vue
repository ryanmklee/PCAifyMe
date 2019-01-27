<template>
    <div id="app">
        <h1>Group Face Detection</h1>
        <div><video ref="video" id="takePhotoCanvas" width="640" height="480" autoplay></video></div>
        <br>
        <div><button id="snap" v-on:click="capture()">Snap Photo</button></div>
        <canvas ref="canvas" id="canvas" width="640" height="480"></canvas>
        <ul>
            <li v-for="c in captures">
                <img v-bind:src="c" height="50" />
            </li>
        </ul>
    </div>
</template>

<script>
    import axios from "axios";
    import FormData from "form-data";
    var imageCapture;


    export default {
        
        name: 'app',
        data() {
            return {
                video: {},
                canvas: {},
                captures: []
            }
        },
        mounted() {
          this.video = this.$refs.video;
          if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
              navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
                this.video.srcObject = stream;
                this.video.play();
                const track = stream.getVideoTracks()[0];
                imageCapture = new ImageCapture(track);

              });
          }

    
        },
        methods: {

          capture() {
            imageCapture.takePhoto().then(blob => createImageBitmap(blob))
            .then(imageBitmap => {
            const canvas = document.getElementById("canvas").getContext("2d").getImageData(0,0,640,480);
            axios
              .post('http://127.0.0.1:5000/api/add', canvas, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            })  
            .then(res => {
                    console.log(res)
                });
            });
            

          },
        
        }
    }
</script>

<style>
    body: {
        background-color: #F0F0F0;
    }
    #app {
      font-family: 'Avenir', Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-align: center;
      color: #2c3e50;
      margin-top: 60px;
    }
    #snap {
      display:inline-block;
      border:0.1em solid #FFFFFF;
      margin:0 0.3em 0.3em 0;
      border-radius:20px;
      box-sizing: border-box;
      font-family:'Roboto',sans-serif;
      font-weight:300;
      color:#FFFFFF;
      text-align:center;
    }

    #snap:hover {
      background-color: #f2f2f2;
    }
    #video {
        background-color: #000000;
    }
    #canvas {
        display: none;
    }
    li {
        display: inline;
        padding: 5px;
    }
</style>