const form = document.getElementById("form")

form.addEventListener("submit", function(e){
  e.preventDefault();

  let userId = e.target.id.value
  let userPw1 = e.target.pw1.value
  let userPw2 = e.target.pw2.value
  let userName = e.target.name.value
  let userPhone1 = e.target.phone1.value
  let userPhone2 = e.target.phone2.value
  let userGender = e.target.gender.value
  let userEmail = e.target.email.value

  console.log(userId, userPw1, userPw2, userName,
    userPhone1, userPhone2, userGender, userEmail)

  if(userId.length < 6){
    alert("아이디가 너무 짧습니다. 6자 이상 입력해주세요.")
    return;
  }

  if(userPw1 !== userPw2){
    alert("비밀번호가 일치하지 않습니다.")
    return;
  }

  alert(`
    ${userId}님 환영합니다
    회원 가입 시 입력하신 내역은 다음과 같습니다. 
    아이디 : ${userId}
    이름 : ${userName}
    전화번호 : 010-${userPhone1}-${userPhone2}
    `)
  location.href = "https://naver.com"
})

document.getElementById('email-domain').addEventListener('change', function(){
  const customInput = document.getElementById('custom-domain')
  if (this.value === 'custom'){
    customInput.style.display = 'inline-block'
  }else{
    customInput.style.display = 'none'
  }
})