// Get the canvas element
function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

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

videos = document.querySelectorAll('.video-info');

videos.forEach(element => {
  element.addEventListener('mouseover', () => {
    info.style.display = 'none';
  });
  element.addEventListener('mouseout', () => {
    info.style.display = 'block';
  });
});




