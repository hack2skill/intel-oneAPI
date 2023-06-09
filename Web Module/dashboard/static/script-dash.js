// Get the canvas element
function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}
const chartPie = document.getElementById('assignment-pie');
percentage = 4/6 *100;
// Calculate the remaining percentage
const remainingPercentage = 100 - percentage;
// Create the chart
const chart = new Chart(chartPie, {
  type: 'doughnut',
  data: {
    datasets: [
      {
        data: [percentage, remainingPercentage],
        backgroundColor: ['#C4B0FF', '#eaeaea'],
        hoverBackgroundColor: ['#9376E0', '#eaeaea'],
        borderWidth: 0,
        weight: 1
      }
    ]
  },
  options: {
    cutout: '60%', // Adjust the size of the hole in the center of the chart
    responsive: true,
    maintainAspectRatio: true,
    animation: {
      animateRotate: true, // Enable rotation animation
      animateScale: true // Enable scale animation
    },
    legend: {
      display: false
    }
  }
});

var chartData1 = {
  labels: ['Chetanya', 'Shivam', 'You', 'Snigdha', 'Sparsh'], 
  datasets: [{
    data: [ 96, 97, 98, 99, 100],
    backgroundColor: '#C4B0FF'
  }]
};

var chartData2 = {
  labels: ['Shekhar', 'Shivam', 'You', 'Sumit', 'Tina'], 
  datasets: [{
    data: [43, 44, 45, 46, 47],
    backgroundColor: '#C4B0FF'
  }]
};

var chartData4 = {
  labels: ['Dino', 'Trio', 'Alex', 'Dobi', 'Smurfs'],
  datasets: [{
    data: [92, 93, 94, 95, 96],
    backgroundColor: '#C4B0FF'
  }]
};

var chartData3 = {
  labels: ['Saumya', 'Tanya', 'You', 'Saumya', 'Gaurang'], 
  datasets: [{
    label: 'Revenue',
    data: [125, 126, 127, 128, 129],
    backgroundColor: '#C4B0FF'
  }]
};

var chartOptions = {
  scales: {
    y: {
      beginAtZero: false
    }
  },
  plugins: {
    legend: {
        display: false,
    }
}
};

// Create and render each chart
var ctx1 = document.getElementById('bar_class').getContext('2d');
new Chart(ctx1, {
  type: 'bar',
  data: chartData1,
  options: chartOptions
});

var ctx2 = document.getElementById('bar_section').getContext('2d');
new Chart(ctx2, {
  type: 'bar',
  data: chartData2,
  options: chartOptions
});

var ctx3 = document.getElementById('bar_school').getContext('2d');
new Chart(ctx3, {
  type: 'bar',
  data: chartData3,
  options: chartOptions
});

var ctx4 = document.getElementById('pet_canvas').getContext('2d');
new Chart(ctx4, {
  type: 'bar',
  data: chartData4,
  options: chartOptions
});


// location

if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(showPosition);
} else {
  console.error('Geolocation is not supported by this browser.');
}

function showPosition(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;

  const apiKey = '78d227ce14e14cb0e3c1d207c8520e83';
  const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&units=metric&appid=${apiKey}`;

  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      const location = data.name;
      const temperature = data.main.temp;
      const description = data.weather[0].description;

      document.querySelector('.location').textContent = location;
      document.querySelector('.temperature').textContent = temperature + '°C';
      document.querySelector('.description').textContent = description;
    })
    .catch(error => console.error('Error:', error));
}

var studname = document.getElementById('studname');

// counter
$(document).ready(function() {
  
  $('.countr').counterUp({
      delay: 10,
      time: 1000
  });

  setTimeout(() => {
    studname.style.transform = 'translateX(6rem) scale(1.25)';
  }, 1000);
  setTimeout(() => {
    studname.style.transform = 'translateX(0) scale(1)';
  }, 3000);
});
  
studname.addEventListener('mouseover', () => {
  studname.style.transform = 'translateX(6rem) scale(1.25)';
  studname.style.transitionDuration = '200ms';
})

studname.addEventListener('mouseout', () => {
  studname.style.transform = 'translateX(0) scale(1)';
  studname.style.transitionDuration = '200ms';
})

// // Get the progress element
// const progress = document.querySelector('#progress-bar > span');

// // Set the target width (e.g., 75%)
// const targetWidth = '60%';

// // Animate the progress bar
// progress.style.width = targetWidth;

// Youtube Fetch
// Function to fetch videos for a specific topic
async function fetchVideosByTopic(topic, maxResults) {
  const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(topic)}&maxResults=${maxResults}&key=AIzaSyB8qJGXTu_kruSssOpyu0OsRS4gr1jgCIU`);
  const data = await response.json();
  return data.items;
}

// Function to fetch shuffled videos from all topics
async function fetchShuffledVideos() {
  const topics = ['Coding Lecture Videos', 'Web Development Tutorials', 'Maths for Undergrades', 'Power of Artificial Intelligence', 'Computer Vision Project', 'New Invention in Technology']; // Add your desired topics here
  const maxResults = 2; // Adjust the number of results as desired

  const videos = [];

  for (const topic of topics) {
    const topicVideos = await fetchVideosByTopic(topic, maxResults);
    if (Array.isArray(topicVideos)) {
      videos.push(...topicVideos);
    }
  }

  // Shuffle the videos array
  const shuffledVideos = shuffleArray(videos);

  return shuffledVideos;
}

// Function to shuffle an array
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

// Function to create a video element with title and description
function createVideoElement(videoId, title, description) {
  const videoElement = document.createElement('div');
  videoElement.classList.add('video');

  const iframe = document.createElement('iframe');
  iframe.src = `https://www.youtube.com/embed/${videoId}`;
  iframe.allowFullscreen = true;
  iframe.loading = 'lazy';
  videoElement.appendChild(iframe);

  const infoContainer = document.createElement('div');
  infoContainer.classList.add('video-info');

  const titleElement = document.createElement('h3');
  titleElement.classList.add('video-title');
  titleElement.textContent = title;
  infoContainer.appendChild(titleElement);

  const descriptionElement = document.createElement('p');
  descriptionElement.classList.add('video-description');
  descriptionElement.textContent = description;
  infoContainer.appendChild(descriptionElement);

  videoElement.appendChild(infoContainer);

  return videoElement;
}

// Add videos to the container
const videoContainer = document.querySelector('.video-wrapper');
const loadingAnimation = document.getElementById('loading-animation');

// Show loading animation
loadingAnimation.style.display = 'block';

// Fetch shuffled videos and create video elements
fetchShuffledVideos()
  .then(videos => {
    // Hide loading animation
    loadingAnimation.style.display = 'none';
    if (videos && videos.length > 0) {
      videos.forEach(video => {
        const videoId = video.id.videoId;
        const title = video.snippet.title;
        const description = video.snippet.description;

        const videoElement = createVideoElement(videoId, title, description);
        if (videoContainer) {
          videoContainer.appendChild(videoElement);
        }
      });

      // Save videos to local storage
      localStorage.setItem('shuffledVideos', JSON.stringify(videos));

    } else {
      // Check if videos are stored in local storage
      const storedVideos = localStorage.getItem('shuffledVideos');
      if (storedVideos) {
        // Use stored videos
        const videos = JSON.parse(storedVideos);

        videos.forEach(video => {
          const videoId = video.id.videoId;
          const title = video.snippet.title;
          const description = video.snippet.description;

          const videoElement = createVideoElement(videoId, title, description);
          videoContainer.appendChild(videoElement);
        });
      }
      else {
        // Display error message if no videos found
        const errorMessage = document.createElement('p');
        errorMessage.style.textAlign = 'center';
        errorMessage.style.width = '80%';
        errorMessage.style.marginLeft = 'auto';
        errorMessage.style.marginRight = 'auto';
        errorMessage.style.borderRadius = '50px';
        errorMessage.style.marginTop = '10px';
        errorMessage.style.border = '10px solid black';
        errorMessage.style.fontWeight = 'bold';
        errorMessage.style.fontSize = '32px';
        errorMessage.style.backgroundColor = 'white';
        errorMessage.style.padding = '50px 0';
        errorMessage.textContent = 'No videos found.';
        errorMessage.style.boxShadow = '0 0 10px 2px gray';
        videoContainer.innerHTML = ''; // Clear the container
        videoContainer.appendChild(errorMessage);
      }
    }
    })
    
    .catch(error => {
      // Hide loading animation
      loadingAnimation.style.display = 'none';
  
      // Check if videos are stored in local storage
      const storedVideos = localStorage.getItem('shuffledVideos');
      if (storedVideos) {
        // Use stored videos
        const videos = JSON.parse(storedVideos);
  
        videos.forEach(video => {
          const videoId = video.id.videoId;
          const title = video.snippet.title;
          const description = video.snippet.description;
  
          const videoElement = createVideoElement(videoId, title, description);
          videoContainer.appendChild(videoElement);
        });
      } else {

    // Display error message
    const errorMessage = document.createElement('p');
      errorMessage.style.textAlign = 'center';
      errorMessage.style.width = '80%';
      errorMessage.style.marginLeft = 'auto';
      errorMessage.style.marginRight = 'auto';
      errorMessage.style.borderRadius = '50px';
      errorMessage.style.marginTop = '10px';
      errorMessage.style.border = '10px solid black';
      errorMessage.style.fontWeight = 'bold';
      errorMessage.style.fontSize = '32px';
      errorMessage.style.backgroundColor = 'white';
      errorMessage.style.padding = '50px 0';
      errorMessage.textContent = 'An error occurred while fetching the videos.';
      errorMessage.style.boxShadow = '0 0 10px 2px gray';
      videoContainer.innerHTML = ''; // Clear the container
      videoContainer.appendChild(errorMessage);
    }
  });



