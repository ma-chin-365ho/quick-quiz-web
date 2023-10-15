const E_PAGE_ID = {
    ROOM_CREATION: 1,
    ROOM_ENTERING: 2
};

const roomStatus = {
    CREATING: 1,
    WAITING: 2,
    ASKING: 3,
    ANSWERING: 4,
};

const answererStatus = {
    WAITING: 1,
    ANSWERING: 2,
};

const transPage = function(pageId) {
    if (pageId === E_PAGE_ID.ROOM_CREATION) {
        window.location.pathname = '/chat/room-creation/';
    } else if (pageId === E_PAGE_ID.ROOM_ENTERING) {
        window.location.pathname = '/chat/room-entering/';
    }
};

const isAnswering = function(status) {
    if (status === answererStatus.ANSWERING) {
        return "＊";
    } else {
        return "　";
    }
};

const roomCreationSubmit = function() {
    var roomId = document.querySelector('#room-id-input').value;
    var roomCreationForm = document.querySelector('#room-creation-form');
    roomCreationForm.action = '/chat/room-questioner/' + roomId + '/';
    roomCreationForm.submit();
};

const roomEnteringSubmit = function() {
    var roomId = document.querySelector('#room-id-input').value;
    var roomEnteringForm = document.querySelector('#room-entering-form');
    roomEnteringForm.action = '/chat/room-answerer/' + roomId + '/';
    roomEnteringForm.submit();
};

const questionSubmit = function(chatSocket) {
    const roomId = document.querySelector('#room-id-input').value;
    const roomPw = document.querySelector('#room-pw-input').value;
    chatSocket.send(JSON.stringify({
        'roomId' : roomId,
        'roomPw' : roomPw,
        'name': "",
        'msg': "question"
    }));
};

const correctSubmit = function(chatSocket) {
    const roomId = document.querySelector('#room-id-input').value;
    const roomPw = document.querySelector('#room-pw-input').value;
    chatSocket.send(JSON.stringify({
        'roomId' : roomId,
        'roomPw' : roomPw,
        'name': "",
        'msg': "correct"
    }));
};

const incorrectSubmit = function(chatSocket) {
    const roomId = document.querySelector('#room-id-input').value;
    const roomPw = document.querySelector('#room-pw-input').value;
    chatSocket.send(JSON.stringify({
        'roomId' : roomId,
        'roomPw' : roomPw,
        'name': "",
        'msg': "incorrect"
    }));
};

const answerSubmit = function(chatSocket) {
    const roomId = document.querySelector('#room-id-input').value;
    const roomPw = document.querySelector('#room-pw-input').value;
    const answererNm = document.querySelector('#answerer-name-input').value;
    chatSocket.send(JSON.stringify({
        'roomId' : roomId,
        'roomPw' : roomPw,
        'name': answererNm,
        'msg': "answer"
    }));
};


const updateAnswererList = function(answerers) {
    answererList = "";
    answerers.forEach(
        (answerer) => answererList += 
            isAnswering(answerer["status"]) + answerer["name"] + "  " + String(answerer["score"]) + "点" + '\n'
    );
    document.querySelector('#answerer-list').value = answererList;
};

const updateQuestionNo = function(questionNo) {
    if (questionNo !== 0) {
        document.querySelector('#question-no-input').value = questionNo;
    }
};

const msgPing = function(chatSocket) {
    const roomId = document.querySelector('#room-id-input').value;
    const roomPw = document.querySelector('#room-pw-input').value;
    const answererNmInput = document.querySelector('#answerer-name-input');
    answererNm = "";
    if (answererNmInput !== null) {
        answererNm = answererNmInput.value;
    }
    chatSocket.send(JSON.stringify({
        'roomId' : roomId,
        'roomPw' : roomPw,
        'name': answererNm,
        'msg': "ping"
    }));
};

const newChatSocket = function(roomId) {
    const ws = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomId
        + '/'
    );
    return ws;
};

const closeChatSocket = function(e) {
    console.error('Chat socket closed unexpectedly');
};