const videoElement = document.getElementById('videoElement');
const questionTextElement = document.getElementById('questionText');
const option1Element = document.getElementById('option1');
const option2Element = document.getElementById('option2');
const option3Element = document.getElementById('option3');
const option4Element = document.getElementById('option4');
const predictionResultElement = document.getElementById('predictionResult');
const resultElement = document.getElementById('res-div');
const result = document.getElementById('result');
const startButton = document.getElementById('start-div');
const progressBar = document.getElementById('progressBar');
const body = document.querySelector('body');
const title = document.querySelector('#title');

let stream;
let currentQuestionIndex = -1;
let selectedOption = "";
let answer;
let marks = 0;
let isQuizStarted = false;
let coin = -1;
let csi;
let k = 0;

body.style.overflowY = "hidden";

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(videoStream => {
            stream = videoStream;
            videoElement.srcObject = stream;
            csi = setInterval(captureFrame, 1500); // Capture frame every 1 seconds
        })
        .catch(error => {
            console.error('Error accessing camera:', error);
        });
}

function stopCamera() {
  if (stream && stream.getTracks) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
}

function displayQuestion() {
    currentQuestionIndex++;
    const currentQuestion = questions[currentQuestionIndex];
    questionTextElement.textContent = currentQuestion.text;
    option1Element.textContent = currentQuestion.options[0];
    option2Element.textContent = currentQuestion.options[1];
    option3Element.textContent = currentQuestion.options[2];
    option4Element.textContent = currentQuestion.options[3];
    answer = currentQuestion.answer;
    progressBar.style.width = '100%';
    selectedOption = "";
    handleNextQuestion();
}

function captureFrame() {
    if (!isQuizStarted) return; 
    // Create a canvas element
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    // Draw the current frame from the video element onto the canvas
    const context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // Get the base64-encoded image data from the canvas
    const imageData = canvas.toDataURL('image/jpeg');
    
    quiz_data = { 
      image_data: imageData,
      coins: coin
    };

    // Send the image data as a POST request to the Django backend using AJAX
    $.ajax({
        url: '',
        type: 'POST',
        data: JSON.stringify(quiz_data),
        contentType: 'application/json',
        success: function(response) {
            console.log(response.message);
            // Handle the response from the Django backend
            const prediction = response.prediction; // Assuming the prediction is returned as a property in the response

            // Clear any previous highlighting
            option1Element.classList.remove('selected');
            option2Element.classList.remove('selected');
            option3Element.classList.remove('selected');
            option4Element.classList.remove('selected');

            // Highlight the corresponding option based on the prediction
            if (prediction === 'top left') {
                option1Element.classList.add('selected');
                selectedOption = option1Element.textContent;
            } else if (prediction === 'top right') {
                option2Element.classList.add('selected');
                selectedOption = option2Element.textContent;
            } else if (prediction === 'bottom left') {
                option3Element.classList.add('selected');
                selectedOption = option3Element.textContent;
            } else if (prediction === 'bottom right') {
                option4Element.classList.add('selected');
                selectedOption = option4Element.textContent;
            }

            console.log('Response from Django:', response);
        },
        error: function(xhr, status, error) {
            console.error('Error sending image to Django:', error);
        }
    });
    console.log(k)
    if (k == 1) {
      clearInterval(csi);
    }
}

let timerInterval;
const progressBarWidth = 100;
const totalTime = 10000; // Total time in milliseconds (10 seconds)
const updateInterval = 10; // Update the progress bar every 100 milliseconds

function handleNextQuestion() {
  let startTime = Date.now();
  progressBar.style.width = '100%'; // Reset the progress bar

  timerInterval = setInterval(() => {
    const elapsed = Date.now() - startTime;
    const remaining = totalTime - elapsed;
    const progress = (remaining / totalTime) * progressBarWidth;

    progressBar.style.width = `${progress}%`;

    if (elapsed >= totalTime) {
      clearInterval(timerInterval);

      if (selectedOption === answer) {
        marks++;
        selectedOption = "";
      }

      if (currentQuestionIndex >= questions.length - 1) {
        coin = (marks / questions.length) * 100;
        body.style.overflowY = "hidden";
        title.style.position = "fixed";
        result.innerHTML = `<p>Quiz completed!</p><p>Your marks: ${marks}/${questions.length}</p><p>You received: ${coin}</p>`;
        resultElement.style.display = "flex";
        stopCamera();
        k = 1;
      } else {
        displayQuestion();
      }
    }
  }, updateInterval);
}

function scrollToBottom() {
  window.scrollTo({
    top: document.documentElement.scrollHeight,
    behavior: 'smooth'
  });
}

startButton.addEventListener('click', () => {
  body.style.overflowY = "auto";
  title.style.position = "static";
  scrollToBottom(); 
  startButton.style.display = 'none'; // Hide the start button
  isQuizStarted = true; // Set the quiz as started
  startCamera();
  displayQuestion();
});
