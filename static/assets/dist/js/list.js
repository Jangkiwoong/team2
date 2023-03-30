$(document).ready(function () {
  listing();
  close_box(); //페이지 로딩 후 url 입력 박스가 자동으로 열려 임시 조치
});
function listing() {
  fetch('/travelDetail').then((res) => res.json()).then((data) => {
    let rows = data['result']

    $('#cards-box').empty()
    rows.forEach((a) => {
      let title = a['title']
      let desc_split = a['desc_split']
      let image = a['image']
      let temp = a['title']

      let temp_html = `<div class="col">
      <div class="card shadow-sm">
                          <img src="${image}" class="card-img-top" alt="${title}">
                          <div class="card-body">
                            <h5 class="card-title">${title}</h5>
                            <p class="card-text">${desc_split}</p>
                            <a href="list_detail/${temp}" class="btn btn-primary">상세보기</a>
                          </div>
                        </div></div>`
      $('#cards-box').append(temp_html)
    })
  })
}
//상세 페이지로 데이터 주기
function list_detail(temp) {
  location.href = '/list_detail/' + temp
  console.log(temp)
}

//여행지 url 입력
function posting() {
  let url = $('#url').val()
  let formData = new FormData();
  formData.append("url_give", url);

  fetch('/travelDetail', { method: "POST", body: formData }).then((res) => res.json()).then((data) => {
    alert(data['msg'])
    window.location.reload()
  })
}

function open_box() {
  $('#post-box').show()
}
function close_box() {
  $('#post-box').hide()
}


//검색기능
function save_bucket() {
  let title = $('#title').val()
  console.log(title)
  let formData = new FormData();
  formData.append("title_give", title);

  //검색기능
  fetch('/gyeonggi', { method: "POST", body: formData, }).then((response) => response.json()).then((data) => {
    rows = data['searches']
    console.log(rows)
    $('#cards-box').empty()
    rows.forEach((a) => {
      let title = a['title']
      let desc_split = a['desc_split']
      let image = a['image']
      let temp = a['title']

      let temp_html = `<div class="col">
                            <div class="card shadow-sm">
                            <img src="${image}" class="card-img-top" alt="${title}">
                            <div class="card-body">
                              <h5 class="card-title">${title}</h5>
                              <p class="card-text">${desc_split}</p>
                              <a href="list_detail/${temp}" class="btn btn-primary">상세보기</a>
                          </div>
                        </div></div>`
      $('#cards-box').append(temp_html)
    });


  })
}
