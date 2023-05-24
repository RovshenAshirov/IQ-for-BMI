const question = document.getElementById("question");
const question_title = document.getElementById("question_title");
const choices = Array.from(document.getElementsByName("variant"));
const progressText = document.getElementById("progressText");
const scoreText = document.getElementById("score");
const progressBarFull = document.getElementById("progressBar");
const loader = document.getElementById("preloader");
const radiogroup = Array.from(document.getElementsByClassName('radiogroup'));
loader.style.display = "flex";
let acceptingAnswers = false;
let score = 0;
let questionCounter = 0;
let questions = [], dict = [];
let CORRECT_BONUS = 1;


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          } 
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');


async function postData(url = '', data = {}, json = true) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *client
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  if(!json){
    return response.data;
  }
  return await response.json(); // parses JSON response into native JavaScript objects
}


postData('/test/get/', { start: true})
  .then((data) => {
    MAX_QUESTIONS = data.total;
    startG(); // JSON data parsed by `response.json()` call
  });
startG = () =>{
  questionCounter = 0;
  score = 0;
  getQues();
}
getQues = () =>{
  loader.style.display = "flex";
  postData('/test/get/', {})
    .then(json => {
      init(json);
    });
  }
init = (data) =>{
  if (data.finish || questionCounter >= MAX_QUESTIONS) {
    localStorage.setItem('data', JSON.stringify(data));
    //go to the end page
    return window.location.assign("/test/end");
  }
  questionCounter++;
  progressText.innerText = `${questionCounter}/${MAX_QUESTIONS}`;
  //Update the progress bar
  progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;
  progressBarFull.innerText = `${parseInt(questionCounter / MAX_QUESTIONS * 100)}%`;

  question_title.innerHTML = `<img src="/static/${data.title}" alt="${data.title}">`;
  choices.forEach(choice => {
    choice.dataset['value'] = data.variant[choice.dataset['prefix']];
    choice.labels[0].innerHTML = `<img src="/static/${choice.dataset['value']}" alt="${choice.dataset['value']}">`;
    choice.checked = false;
  });

  acceptingAnswers = true;
  loader.style.display = "none";
  initClick(data);
}
initClick = (data) =>{
  radiogroup.forEach(choice => {
    choice.addEventListener("click", e => {
      if (!acceptingAnswers) return;
      acceptingAnswers = false;
      const selectedAnswer = e.target.alt;
      postData('/test/post/', {
        id: data.id,
        answer: selectedAnswer
      })
      .then(data => {
        const classToApply = data.answer;

        if (classToApply === "correct") {
          incrementScore(CORRECT_BONUS);
        }
        e.target.parentElement.classList.add(classToApply);
        setTimeout(() => {
          e.target.parentElement.classList.remove(classToApply);
          getQues();
        }, 700);
      });
    });
  });
}

incrementScore = num => {
  score += num;
  scoreText.innerText = score;
};