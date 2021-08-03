# 留言板

<link href="../../static/css/comments.css" rel="stylesheet">

<div class="container mt-5">
    <div class="d-flex justify-content-center row">
        <div id="comment-first" class="col-md-8">
            <div class="d-flex flex-column comment-section" id="myGroup">
                <div class="bg-white p-2">
                    <div class="d-flex flex-row user-info"><img class="rounded-circle" src="../../static/images/fastapi-logo.png" width="40">
                        <div class="d-flex flex-column justify-content-start ml-2"><span class="d-block font-weight-bold name">Adminstrator</span><span class="date text-black-50">Shared publicly - May 2021</span></div>
                    </div>
                    <div class="mt-2">
                        <p class="comment-text">
                          您好，我們非常重視您對於使用本系統的使用者體驗度，因此非常歡迎在下方留下您寶貴的建議。<br>
                          非常感謝！
                        </p>
                    </div>
                </div>
                <div class="bg-white p-2 toolbar">
                    <div class="d-flex flex-row fs-12">
                        <div id="collapseComment" class="like p-2 cursor action-collapse" data-toggle="collapse" aria-expanded="true" aria-controls="collapse-1" href="#collapse-1"><i class="fa fa-commenting-o"></i><span class="ml-1">留下一句話再走吧</span></div>
                        <!--
                        <div class="like p-2 cursor action-collapse" data-toggle="collapse" aria-expanded="true" aria-controls="collapse-2" href="#collapse-2"><i class="fa fa-share"></i><span class="ml-1">Share</span></div>
                        -->
                    </div>
                </div>
                <div id="collapse-1" class="bg-light p-2 collapse" data-parent="#myGroup">
                    <div class="d-flex flex-row align-items-start"><img id="avater" class="rounded-circle" src="" width="40"><textarea id="comment" class="form-control ml-1 shadow-none textarea" placeholder="至少 10 個字以上.."></textarea></div>
                    <div class="mt-2 text-right">
                      <input class="gender-radio" type="radio" id="male" name="gender" value="male" onclick="radioSelectEvent();">
                      <label class="gender-label" for="male">Male</label>
                      <input class="gender-radio" type="radio" id="female" name="gender" value="female" onclick="radioSelectEvent();" checked="checked">
                      <label class="gender-label" for="female">Female</label>
                      <button class="btn btn-primary btn-sm shadow-none" type="button" onclick="postComment();">
                        Post comment
                      </button>
                      <button class="btn btn-outline-primary btn-sm ml-1 shadow-none" type="button" onclick="document.getElementById('collapseComment').click();">
                        Cancel
                      </button>
                    </div>
                </div>
                <!-- <div id="collapse-2" class="bg-light p-2 collapse" data-parent="#myGroup">
                    <div class="d-flex flex-row align-items-start"><i class="fa fa-facebook border p-3 rounded mr-1"></i><i class="fa fa-twitter border p-3 rounded mr-1"></i><i class="fa fa-linkedin border p-3 rounded mr-1"></i><i class="fa fa-instagram border p-3 rounded mr-1"></i><i class="fa fa-dribbble border p-3 rounded mr-1"></i> <i class="fa fa-pinterest-p border p-3 rounded mr-1"></i> </div>
                </div> -->
            </div>
        </div>
        {% for comment in comments | sort(attribute='datetime', reverse=True) %}
        <div class="col-md-8">
            {% if comment['username'] == user['user_web_name'] %}
            <button class="delete-post" type="button"
                    data-toggle="confirmation" data-uuid="{{ comment['uuid'] }}"
                    data-title="真的要刪除留言嗎？" data-content="確認後這則留言將會永久刪除。">&times;</button>
            {% endif %}
            <div class="d-flex flex-column comment-section">
                <div class="bg-white p-2">
                    <div class="d-flex flex-row user-info"><img class="rounded-circle" src="../../static/images/unnamed_{{ comment['sex'] }}.png" width="40">
                        <div class="d-flex flex-column justify-content-start ml-2"><span class="d-block font-weight-bold name">{{ comment['username'] }}</span><span class="date text-black-50">Left a comment - {{ comment['datetag'] }}</span></div>
                    </div>
                    <div class="mt-2">
                        <p class="comment-text">
                          {{ comment['comment'] | replace('\n', '<br/>') }}
                        </p>
                    </div>
                </div>
                <div class="bg-white p-2 toolbar">
                    <div class="d-flex flex-row fs-12">
                        <div class="like p-2 cursor" onclick="likeEvent(this, '{{ comment['uuid'] }}')">
                        {% if user['user_web_name'] in comment['like_people'] %}
                          <i class="fa fa-heart"></i>
                        {% else %}
                          <i class="fa fa-heart-o"></i>
                        {% endif %}
                        {% if user['user_web_name'] in comment['like_people'] %}
                          <span class="ml-1">您已說讚</span>
                        {% else %}
                          <span class="ml-1">讚</span>
                        {% endif %}
                        </div>
                        <div class="like p-2 cursor action-collapse" data-toggle="collapse" aria-expanded="true" aria-controls="collapse-{{ comment['uuid'] }}" href="#collapse-{{ comment['uuid'] }}"><i class="fa fa-thumbs-o-up"></i><span class="ml-1">{{ comment['like'] }} 個人說讚</span></div>
                    </div>
                </div>
                <div id="collapse-{{ comment['uuid'] }}" class="bg-light p-2 collapse">
                    <div class="d-flex flex-row align-items-start">
                    {% for person in comment['like_people'] %}
                      <i class="fa fa-user border p-3 rounded mr-1 like-people"> {{ person }}</i>
                    {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<script type="text/javascript">
  const avater = document.getElementById("avater");
  console.log("{{ user }}");
  function getGenderSex() {
    var radios = document.getElementsByName('gender');
    for (var i = 0, length = radios.length; i < length; i++) {
      if (radios[i].checked) {
        return radios[i].value;
      }
    }
  }

  function radioSelectEvent() {
    avater.src = `../../static/images/unnamed_${getGenderSex()}.png`;
  }

  radioSelectEvent();

  function likeEvent(el, uuid) {
    var operate;
    var username = "{{ user['user_web_name'] }}";
    var span = el.childNodes[3];
    var heart = span.previousSibling.previousSibling;
    var nextEl = span.parentNode.nextElementSibling;
    var likeNum = parseInt(nextEl.innerText.split()[0]);
    var collapse = document.getElementById(`collapse-${uuid}`);
    var i = document.createElement("i");
    if (span.innerHTML == "讚") {
      span.innerHTML = "您已說讚";
      span.title = "收回讚";
      likeNum += 1;
      heart.className = "fa fa-heart";
      operate = "increase";
      i.className = "fa fa-user border p-3 rounded mr-1 like-people";
      i.innerText = ` ${username}`;
      collapse.childNodes[1].appendChild(i)
    } else {
      span.innerHTML = "讚";
      span.title = "按讚";
      likeNum -= 1;
      heart.className = "fa fa-heart-o";
      operate = "decrease";
      var itemStart = collapse.childNodes[1];
      var likePeople = itemStart.childNodes;
      for (var i = 0, length = likePeople.length; i < length; i++) {
        if (likePeople[i].innerText == ` ${username}`) {
          itemStart.removeChild(likePeople[i])
          break;
        }
      }
    }
    nextEl.innerText = `${likeNum} 個人說讚`;
    $.ajax({
      type: "PUT",
      url: "../../api/v1/contact/like-comment",
      data: {
        uuid: uuid,
        username: username,
        operate: operate
      },
      success: function(res){
        console.log(res);
      },
      error: function(jqXHR, textStatus, errorThrown){
        const statusCode = jqXHR.status;
        $('html,body').scrollTop(0);
        elabel.innerHTML = `錯誤碼：${statusCode}，發送 Post 請求至服務器失敗，可能是請求數據 API 例外發生。`;
        error.style.display = "block";
        setTimeout(function() {
          error.style.display = "none";
        }, 6000);
      },
    });
  }

  function postComment() {
    var comment = document.getElementById("comment");
    var sex = getGenderSex();
    $('html,body').scrollTop(0);
    if (comment.value.length <= 10) {
      comment.focus();
      wlabel.innerHTML = "請輸入至少 10 個字的留言";
      warning.style.display = "block";
      setTimeout(function() {
        warning.style.display = "none";
      }, 3000);
      return false;
    }
    $.ajax({
      type: "POST",
      url: "../../api/v1/contact/post-comment",
      data: {
        username: "{{ user['user_web_name'] }}",
        sex: sex,
        comment: comment.value
      },
      success: function(res){
        $("#comment-first").after(formatElementString(res));
        loadConfirmation();
        comment.value = '';
        document.getElementById('collapseComment').click();
        slabel.innerHTML = `${res.data.username} 剛剛新增了一筆留言。`;
        success.style.display = "block";
        setTimeout(function() {
          success.style.display = "none";
        }, 3000);
      },
      error: function(jqXHR, textStatus, errorThrown){
        const statusCode = jqXHR.status;
        elabel.innerHTML = `錯誤碼：${statusCode}，發送 Post 請求至服務器失敗，可能是請求數據 API 例外發生。`;
        error.style.display = "block";
        setTimeout(function() {
          error.style.display = "none";
        }, 6000);
      },
    });
  }

  function deleteComment(el) {
    const uuid = el.data('bs.confirmation').config.uuid;
    $('html,body').scrollTop(0);
    $.ajax({
      type: "DELETE",
      url: "../../api/v1/contact/delete-comment",
      data: {
        uuid: uuid
      },
      success: function(res){
        el.parent().fadeOut(800, function(){
          $(this).remove();
        });
        slabel.innerHTML = `一筆留言已被 ${res.data.username} 刪除了。`;
        success.style.display = "block";
        setTimeout(function() {
          success.style.display = "none";
        }, 3000);
      },
      error: function(jqXHR, textStatus, errorThrown){
        const statusCode = jqXHR.status;
        if (statusCode == 404) {
          elabel.innerHTML = `錯誤碼：${statusCode}，數據庫中找不到指定刪除的留言。`;
        } else {
          elabel.innerHTML = `錯誤碼：${statusCode}，發送 Post 請求至服務器失敗，可能是請求數據 API 例外發生。`;
        }
        error.style.display = "block";
        setTimeout(function() {
          error.style.display = "none";
        }, 6000);
      },
    });
  }

  function formatElementString(res) {
    var ncomment = res.data.comment.replace(/\n/g, "<br/>");
    return `
        <div class="col-md-8">
            <button class="delete-post" type="button"
                    data-toggle="confirmation" data-uuid="${res.data.uuid}"
                    data-title="真的要刪除留言嗎？" data-content="確認後這則留言將會永久刪除。">&times;</button>
            <div class="d-flex flex-column comment-section">
                <div class="bg-white p-2">
                    <div class="d-flex flex-row user-info"><img class="rounded-circle" src="../../static/images/unnamed_${res.data.sex}.png" width="40">
                        <div class="d-flex flex-column justify-content-start ml-2"><span class="d-block font-weight-bold name">${res.data.username}</span><span class="date text-black-50">Left a comment - ${res.data.datetag}</span></div>
                    </div>
                    <div class="mt-2">
                        <p class="comment-text">
                          ${ncomment}
                        </p>
                    </div>
                </div>
                <div class="bg-white p-2 toolbar">
                    <div class="d-flex flex-row fs-12">
                        <div class="like p-2 cursor" onclick="likeEvent(this, '${res.data.uuid}')">
                          <i class="fa fa-heart-o"></i>
                          <span class="ml-1">讚</span>
                        </div>
                        <div class="like p-2 cursor action-collapse" data-toggle="collapse" aria-expanded="true" aria-controls="collapse-${res.data.uuid}" href="#collapse-${res.data.uuid}"><i class="fa fa-thumbs-o-up"></i><span class="ml-1">${res.data.like} 個人說讚</span></div>
                    </div>
                </div>
                <div id="collapse-${res.data.uuid}" class="bg-light p-2 collapse">
                    <div class="d-flex flex-row align-items-start">
                    </div>
                </div>
            </div>
        </div>
    `
  }
</script>