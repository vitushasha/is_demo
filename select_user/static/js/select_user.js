let buttonSelectUser = document.getElementById('selectuser');
let buttonGetInfo = document.getElementById('getinfo')

buttonSelectUser.onclick = function () {
    BX24.selectUser(function (res) {
        buttonSelectUser.innerHTML = res['name'];
        buttonGetInfo.disabled = false;
        buttonGetInfo.value = res['id'];
    })
}