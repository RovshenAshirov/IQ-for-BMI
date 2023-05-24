const iq_score = document.getElementById('iq_score');
const iq_ability = document.getElementById('iq_ability');
const result = JSON.parse(localStorage.getItem('data'));

iq_score.innerText = `Sizning IQ darajangiz: ${result.iq}`;
iq_ability.innerText = result.ability;