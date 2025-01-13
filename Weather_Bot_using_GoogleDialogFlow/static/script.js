// // state
// let currCity = "London";
// let units = "metric";

// // Selectors
// let city = document.querySelector(".weather__city");
// let datetime = document.querySelector(".weather__datetime");
// let weather__forecast = document.querySelector('.weather__forecast');
// let weather__temperature = document.querySelector(".weather__temperature");
// let weather__icon = document.querySelector(".weather__icon");
// let weather__minmax = document.querySelector(".weather__minmax");
// let weather__realfeel = document.querySelector('.weather__realfeel');
// let weather__humidity = document.querySelector('.weather__humidity');
// let weather__wind = document.querySelector('.weather__wind');
// let weather__pressure = document.querySelector('.weather__pressure');
// let weather__cloudiness = document.querySelector('.weather__cloudiness');
// let weather__visibility = document.querySelector('.weather__visibility');
// let weather__sunrise = document.querySelector('.weather__sunrise');
// let weather__sunset = document.querySelector('.weather__sunset');
// let weather__rain = document.querySelector('.weather__rain');
// let weather__snow = document.querySelector('.weather__snow');

// // search
// document.querySelector(".weather__search").addEventListener('submit', e => {
//     let search = document.querySelector(".weather__searchform");
//     // prevent default action
//     e.preventDefault();
//     // change current city
//     currCity = search.value;
//     // get weather forecast 
//     getWeather();
//     // clear form
//     search.value = ""
// })

// // units
// document.querySelector(".weather_unit_celsius").addEventListener('click', () => {
//     if(units !== "metric"){
//         // change to metric
//         units = "metric"
//         // get weather forecast 
//         getWeather()
//     }
// })

// document.querySelector(".weather_unit_farenheit").addEventListener('click', () => {
//     if(units !== "imperial"){
//         // change to imperial
//         units = "imperial"
//         // get weather forecast 
//         getWeather()
//     }
// })

// function convertTimeStamp(timestamp, timezone){
//      const convertTimezone = timezone / 3600; // convert seconds to hours 

//     const date = new Date(timestamp * 1000);
    
//     const options = {
//         weekday: "long",
//         day: "numeric",
//         month: "long",
//         year: "numeric",
//         hour: "numeric",
//         minute: "numeric",
//         timeZone: `Etc/GMT${convertTimezone >= 0 ? "-" : "+"}${Math.abs(convertTimezone)}`,
//         hour12: true,
//     }
//     return date.toLocaleString("en-US", options)
// }

// // convert country code to name
// function convertCountryCode(country){
//     let regionNames = new Intl.DisplayNames(["en"], {type: "region"});
//     return regionNames.of(country)
// }

// function getWeather(){
//     const API_KEY = '64f60853740a1ee3ba20d0fb595c97d5';

//     fetch(`https://api.openweathermap.org/data/2.5/weather?q=${currCity}&appid=${API_KEY}&units=${units}`).then(res => res.json()).then(data => {
//         console.log(data);
//         city.innerHTML = `${data.name}, ${convertCountryCode(data.sys.country)}`;
//         datetime.innerHTML = convertTimeStamp(data.dt, data.timezone); 
//         weather__forecast.innerHTML = `<p>${data.weather[0].main}`;
//         weather__temperature.innerHTML = `${data.main.temp.toFixed()}&#176`;
//         weather__minmax.innerHTML = `<p>Min: ${data.main.temp_min.toFixed()}&#176</p><p>Max: ${data.main.temp_max.toFixed()}&#176</p>`;
//         weather__realfeel.innerHTML = `${data.main.feels_like.toFixed()}&#176`;
//         weather__humidity.innerHTML = `${data.main.humidity}%`;
//         weather__wind.innerHTML = `${data.wind.speed} ${units === "imperial" ? "mph": "m/s"}`; 
//         weather__pressure.innerHTML = `${data.main.pressure} hPa`;

//         // New weather data to display
//         document.querySelector(".weather__condition").innerHTML = data.weather[0].description;
//         document.querySelector(".weather__cloudiness").innerHTML = `${data.clouds.all}%`;
//         document.querySelector(".weather__windspeed").innerHTML = `${data.wind.speed} km/h`;
//         document.querySelector(".weather__feelslike").innerHTML = `${data.main.feels_like.toFixed()}°C`;
//         document.querySelector(".weather__visibility").innerHTML = `${data.visibility / 1000} km`;
        
//         // Sunrise and Sunset (convert from UNIX timestamp)
//         let sunrise = new Date(data.sys.sunrise * 1000).toLocaleTimeString();
//         let sunset = new Date(data.sys.sunset * 1000).toLocaleTimeString();
//         document.querySelector(".weather__sunrise").innerHTML = sunrise;
//         document.querySelector(".weather__sunset").innerHTML = sunset;

//         // Rain and Snow data (may not always exist)
//         let rain = data.rain ? data.rain["1h"] : 0;
//         let snow = data.snow ? data.snow["1h"] : 0;
//         document.querySelector(".weather__rain").innerHTML = rain > 0 ? `${rain} mm` : "No rain";
//         document.querySelector(".weather__snow").innerHTML = snow > 0 ? `${snow} mm` : "No snow";
//     });
// }

// document.body.addEventListener('load', getWeather());




// Raining animated
var canvas = document.getElementById('thunder');
var ctx = canvas.getContext('2d');

var stgw = 1280;
var stgh = 720;

var loffset = 0;
var toffset = 0;

function _pexresize() {
    var cw = window.innerWidth;
    var ch = window.innerHeight;
    if (cw <= ch * stgw / stgh) {
        loffset = 0;
        toffset = Math.floor(ch - (cw * stgh / stgw)) / 2;
        canvas.style.width = cw + "px";
        canvas.style.height = Math.floor(cw * stgh / stgw) + "px";
    } else {
        loffset = Math.floor(cw - (ch * stgw / stgh)) / 2;
        toffset = 0;
        canvas.style.height = ch + "px";
        canvas.style.width = Math.floor(ch * stgw / stgh) + "px";
    }
    canvas.style.marginLeft = loffset + "px";
    canvas.style.marginTop = toffset + "px";
}
_pexresize();

var count = 100;
var lcount = 6;

var layer = [];
var layery = [];

ctx.fillStyle = "rgba(255,255,255,0.5)";
for (var l = 0; l < lcount; l++) {
    ctx.clearRect(0, 0, stgw, stgh);
    for (var i = 0; i < count * (lcount - l) / 1.5; i++) {
        var myx = Math.floor(Math.random() * stgw);
        var myy = Math.floor(Math.random() * stgh);
        var myh = l * 6 + 8;
        var myw = myh / 10;
        ctx.beginPath();
        ctx.moveTo(myx, myy);
        ctx.lineTo(myx + myw, myy + myh);
        ctx.arc(myx, myy + myh, myw, 0, 1 * Math.PI);
        ctx.lineTo(myx - myw, myy + myh);
        ctx.closePath();
        ctx.fill();
    }
    layer[l] = new Image();
    layer[l].src = canvas.toDataURL("image/png");
    layery[l] = 0;
}

var stt = 0;
var str = Date.now() + Math.random() * 4000;
var stact = false;

function animate() {
    ctx.clearRect(0, 0, stgw, stgh);

    for (var l = 0; l < lcount; l++) {
        layery[l] += (l + 1.5) * 5;
        if (layery[l] > stgh) {
            layery[l] = layery[l] - stgh;
        }
        ctx.drawImage(layer[l], 0, layery[l]);
        ctx.drawImage(layer[l], 0, layery[l] - stgh);
    }
    if (Date.now() > str) {
        stact = true;
    }
    if (stact) {
        stt++;
        if (stt < 5 + Math.random() * 10) {
            var ex = stt / 30;
        } else {
            var ex = (stt - 10) / 30;
        }
        if (stt > 20) {
            stt = 0;
            stact = false;
            str = Date.now() + Math.random() * 8000 + 2000;
        }

        ctx.fillStyle = "rgba(255,255,255," + ex + ")";
        ctx.fillRect(0, 0, stgw, stgh);
    }
    window.requestAnimationFrame(animate);
}

animate();
