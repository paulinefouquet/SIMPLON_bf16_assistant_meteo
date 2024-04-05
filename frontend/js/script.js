const endpoint = 'http://pauline-mon-api-meteo-nlp.aphrgnb0aeaudgbz.westeurope.azurecontainer.io:8000/cities_herault'
const cities = [];

fetch(endpoint)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    cities.push(...data.cities);
    console.log(cities);
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });

function findMatches(wordToMatch, cities){
    const regex = new RegExp(wordToMatch, 'gi');
    return cities.filter(city => city.match(regex));
}

function displayMatches() {
  const matchArray = findMatches(this.value, cities);
  const suggestions = document.querySelector('.suggestions');
  const html = matchArray.map(city => `<div class="suggestion">${city}</div>`).join('');
  suggestions.innerHTML = html;
}

document.getElementById('forecastForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    var form = event.target;
    var formData = new FormData(form);

    var city = formData.get('city');
    var date = formData.get('date');
    var hour = formData.get('hour');

    var apiUrl = 'http://pauline-mon-api-meteo-nlp.aphrgnb0aeaudgbz.westeurope.azurecontainer.io:8000/forecast';
    var requestUrl = apiUrl + '?city=' + encodeURIComponent(city) + '&date=' + encodeURIComponent(date) + '&hour=' + encodeURIComponent(hour);

    fetch(requestUrl)
        .then(response => response.blob())
        .then(blob => {
            var audioUrl = URL.createObjectURL(blob); 
            document.getElementById("audioPlayer").src = audioUrl;
            document.getElementById("audioPlayer").style.display = "block";
        })
        .catch(error => {
            console.error('Une erreur s\'est produite:', error);
        });
});

document.getElementById('city').addEventListener('input', displayMatches);

document.querySelector('.suggestions').addEventListener('click', function(event) {
    if (event.target.classList.contains('suggestion')) {
        document.getElementById('city').value = event.target.textContent;
        document.querySelector('.suggestions').innerHTML = ''; // Effacer les suggestions après sélection
    }
});