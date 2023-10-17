let video = document.getElementById("video");
let canvas = document.getElementById("canvas");
let name_input = document.getElementById("name");
let model, detector;
let ctx = canvas.getContext("2d");

function sendJSON(data, name){
    // Assuming 'data' holds the data URL from your canvas
    var dataURL = canvas.toDataURL('image/jpeg');
    

    // Create a JavaScript object to hold the data you want to send to the server
    var requestData = {
        imageData: dataURL, // You can use any key you prefer
        name: name,
    };

    // Make an AJAX POST request to your server
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8000/api/check_image_input/',
        data: JSON.stringify(requestData), // Convert the data to a JSON string
        contentType: 'application/json', // Set the content type to JSON
        success: function(response) {
            // Handle the response from the server here
            console.log('Server response:', response);
        },
        error: function(xhr, status, error) {
            // Handle errors here
            console.error('AJAX Error:', status, error);
        }
    });       
        
        
    }

    const setupCamera = () => {
        navigator.mediaDevices
            .getUserMedia({
                video: {width: 600, height: 400},
                audio: false,
            })
            .then((stream) => {
                video.srcObject = stream;
            });
};

const detectFaces = async () => {
    const estimationConfig = {flipHorizontal: false};
    const faces = await detector.estimateFaces(video, estimationConfig);
    
    console.log(faces);

    // ctx.drawImage(video, 0, 0, 600, 400);
    if(faces.length === 1){
        

        ctx.drawImage(
            video, 
            faces[0].box.xMin, 
            faces[0].box.yMin, 
            faces[0].box.width, 
            faces[0].box.height, 
            0, 
            0,
            151,
            151
        );
        
        var data = canvas.toDataURL('image/jpeg');
        console.log(data);
        var name = name_input.value;
        console.log("the name is");
        console.log(name);

        sendJSON(data, name);
    }

    // faces.forEach(face => {
    //     console.log(face.box);
    //     console.log(face.box);
    //     ctx.beginPath();
    //     ctx.lineWidth = "4";
    //     ctx.strokeStyle = "blue";
    //     ctx.rect(
    //         face.box.xMin,
    //         face.box.yMin,
    //         face.box.height,
    //         face.box.width,
    //     );
    //     ctx.stroke();
    // });
};



setupCamera();

video.addEventListener("loadeddata", async () => {
    console.log("this runs")
    model = await faceDetection.SupportedModels.MediaPipeFaceDetector;
    const detectorConfig = {
        runtime: 'mediapipe',
        solutionPath: 'https://cdn.jsdelivr.net/npm/@mediapipe/face_detection',
                        // or 'base/node_modules/@mediapipe/face_detection' in npm.
    };
    detector = await faceDetection.createDetector(model, detectorConfig);
    
    setInterval(detectFaces, 40);

});

