function updateClock() {
    const now = new Date()
    const m1 = String(now.getMonth()+1)
    const d = String(now.getDate())
    const h = String(now.getHours()).padStart(2, '0')
    const m2 = String(now.getMinutes()).padStart(2, '0')
    document.getElementById('time').textContent = `현재시간 : ${m1}월 ${d}일 ${h}시${m2}분`
  }

  setInterval(updateClock, 100)
  updateClock()

function darkmode() {
  document.getElementById('page').classList.toggle('dark')
}
