function call(action) {
  var request = new XMLHttpRequest();
  var successCallback = function() {
    document.getElementById('state').innerHTML = request.responseText;
  }
  request.onreadystatechange = function() {
    if(request.readyState < 4) {
        return;
    }
    if(request.status !== 200) {
      console.log("ERROR");
      return;
    }
    if(request.readyState === 4) {
        successCallback();
    }
  };

  request.onreadystatechange = function() {
      if(request.readyState < 4) {
          // handle preload
          return;
      }
      if(request.status !== 200) {
          // handle error
          return;
      }
      if(request.readyState === 4) {
          // handle successful request
          successCallback();
      }
  };

  var path = '/api/v1/'+action;
  request.open('GET',path, true);
  request.send('');
}
