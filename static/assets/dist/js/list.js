$(document).ready(function () {
    listing();
  });
  function listing() {
    fetch('/gyeonggi').then((res) => res.json()).then((data) => {
      let rows = data['result']
      $('#cards-box').empty()
      rows.forEach((a) => {
        let name = a['name']
        let trable_info = a['trable_info']
        let star = a['star']
        let img = a['img']
        let title = a['title']
        let temp = a['title']
        let star_repeat = '⭐'.repeat(star)

        temp_html = `<div class="col">
                                      <div class="card shadow-sm">
                                          <img src="${img}">
                                          <div class="card-body">
                                          <p class="card-text">${title}</p>
                                          <p>${trable_info}</p>
                                          <p>${name}</p>
                                          <p>${star_repeat}</p>
                                          <div class="d-flex justify-content-between align-items-center">
                                              <div class="btn-group">
                                              <button class="btn btn-sm btn-outline-secondary" onclick="list_detail('${temp}')">View</button>
                                              
                                              </div>
                                              
                                          </div>
                                          </div>
                                      </div>
                                  </div>`
        $('#cards-box').append(temp_html)
      });
    })
  }
  //상세페이지로 데이터 주기
  function list_detail(temp) {
    location.href='/list_det/'+temp

    
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
        let name = a['name']
        let trable_info = a['trable_info']
        let star = a['star']
        let img = a['img']
        let title = a['title']
        let temp = a['title']
        let star_repeat = '⭐'.repeat(star)

        temp_html = `<div class="col">
                                      <div class="card shadow-sm">
                                          <img src="${img}">
                                          <div class="card-body">
                                          <p class="card-text">${title}</p>
                                          <p>${trable_info}</p>
                                          <p>${name}</p>
                                          <p>${star_repeat}</p>
                                          <div class="d-flex justify-content-between align-items-center">
                                              <div class="btn-group">
                                                <button class="btn btn-sm btn-outline-secondary" onclick="list_detail('${temp}')">View</button>
                                              
                                              </div>
                                              
                                          </div>
                                          </div>
                                      </div>
                                  </div>`
        $('#cards-box').append(temp_html)
      });


    })
  }
