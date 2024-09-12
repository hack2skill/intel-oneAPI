const videoElement = document.getElementById('videoElement');
const pred = document.getElementById('pred');

let stream;
let k = 0;
let csi; // Interval variable

function startCamera() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(videoStream => {
      stream = videoStream;
      videoElement.srcObject = stream;
      csi = setInterval(captureFrame, 2000); // Capture frame every 5 seconds
    })
    .catch(error => {
      console.error('Error accessing camera:', error);
    });
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

var excercise = ['Neck Rolls: Roll your head in a circular motion, clockwise and counterclockwise.',
  'Shoulder Shrugs: Lift your shoulders up toward your ears and then release them down.',
  'Seated Twist: Twist your torso to the left and right, looking over each shoulder.',
  'Seated Leg Raises: Lift one leg up, extend it straight, and hold for a few seconds. Repeat with the other leg.',
  'Ankle Circles: Rotate your ankles in a circular motion, clockwise and counterclockwise.',
  'Arm Circles: Extend your arms to the sides and make small circles with your hands.',
  'Wrist Flexes: Stretch your arms forward, palms facing up, and flex your wrists up and down.',
  'Seated Toe Taps: Lift your feet off the ground and tap your toes while keeping your heels grounded.',
  'Seated Marching: Lift one knee up, then the other, as if you were marching in place.',
  'Seated Heel Raises: Lift your heels off the floor while keeping your toes grounded.',
  'Seated Calf Stretches: Extend one leg forward, flex your foot, and gently pull your toes towards you. Repeat with the other leg.',
  'Seated Chest Stretch: Clasp your hands behind your back, straighten your arms, and lift your chest.',
  'Seated Spinal Twist: Cross one leg over the other, place your opposite hand on the outside of the crossed knee, and gently twist your torso.',
  'Seated Side Bends: Extend one arm overhead and lean to the opposite side, stretching your side. Repeat on the other side.',
  'Seated Hip Circles: Sit forward on the edge of your chair and make circular motions with your hips.',
  'Seated Cat-Cow Stretch: Arch your back and then round it, alternating between the two positions.',
  'Seated Abdominal Contractions: Tighten your abdominal muscles by pulling your belly button towards your spine.',
  'Seated Shoulder Stretch: Reach one arm across your chest, hold it with the opposite hand, and gently pull it closer to your body. Repeat with the other arm.',
  'Seated Butterfly Stretch: Bring the soles of your feet together and gently press your knees towards the floor.',
  'Seated Hamstring Stretch: Extend one leg forward, flex your foot, and reach towards your toes. Repeat with the other leg.',
  'Seated Wrist Stretches: Extend one arm forward, palm facing up, and use the other hand to gently pull your fingers back. Repeat with the other hand.',
  'Seated Hand Squeezes: Make a fist with both hands, squeeze tightly, and then release.',
  'Seated Eye Rolls: Look up, down, left, and right, and then make circular motions with your eyes.',
  'Seated Deep Breathing: Inhale deeply through your nose, hold for a few seconds, and exhale slowly through your mouth.',
 'Seated Meditation: Close your eyes, focus on your breath, and allow your mind to relax.',
  'Seated Shoulder Blade Squeezes: Squeeze your shoulder blades together, hold for a few seconds, and then release.',
  'Seated Leg Crosses: Cross one leg over the other, place your ankle on the opposite knee, and gently press down on the raised knee.',
  'Seated Side Leg Raises: Sit upright, extend one leg out to the side, and lift it up while keeping it straight. Repeat with the other leg.',
  'Seated Torso Stretch: Reach both arms overhead]'];

function captureFrame() {
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
  };

  // Send the image data as a POST request to the Django backend using AJAX
  $.ajax({
    url: '',
    type: 'POST',
    data: JSON.stringify(quiz_data),
    contentType: 'application/json',
    success: function (response) {
      console.log(response.message);
      // Handle the response from the Django backend
      const prediction = response.prediction; // Assuming the prediction is returned as a property in the response
      if (prediction == "Yes") {
        pred.innerHTML = "Drowsiness Detected";
        clearInterval(csi); // Halt the interval
        alert(excercise[getRandomInt(excercise.length)]);
        setTimeout(() => {
          pred.innerHTML = ""; // Clear the alert message after it is clicked
          csi = setInterval(captureFrame, 2000); // Resume the interval
        }, 5000); // Adjust the duration of the alert as needed
      } else {
        pred.innerHTML = "All Ok!";
      }
      console.log('Response from Django:', prediction);
    },
    error: function (xhr, status, error) {
      console.error('Error sending image to Django:', error);
    }
  });
  console.log(k);
  if (k == 1) {
    clearInterval(csi);
    stopCamera();
  }
}

function stopCamera() {
  if (stream && stream.getTracks) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
}

startCamera();

var timer = setTimeout(() => {
  k = 1;
  console.log("Finish");
  window.location.href = "/lectures/";
}, 60000);
