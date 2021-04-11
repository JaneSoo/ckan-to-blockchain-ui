function loadInputUrl() {
  document.getElementById('ckan-input-url').type = "url";
  document.getElementById('find-ckan-packages').hidden = false;
}

function searchCkanUrl() {
  document.getElementById('find-ckan-packages').on('click')
}

function getPackages() {
  var url = document.getElementById('ckan-input-url');
  console.log(url.value)
  var entry = {
    url: url.value
  };

  fetch(`${window.origin}/get-packages`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function(response) {
    if (response.status !== 200) {
      console.log(`Looks like there was a problem. Status code: ${response.status}`);
      return;
    }
    response.json().then(function(data) {
      document.getElementById('packages').innerHTML = null;
      document.getElementById('label-select').style.visibility = 'visible';
      document.getElementById('packages').style.visibility = 'visible';
      var packages = data['package_lists'];
      console.log(packages)
      packages.forEach(function(package) {
        var option = document.createElement("option");
        option.text = package;
        option.value = package;
        document.getElementById('packages').appendChild(option);
      })
      document.getElementById('btn-store-package').style.visibility = 'visible';
      document.getElementById('bth-verify-package').style.visibility = 'visible';
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
  });
}

function storePackage() {
  var url = document.getElementById('ckan-input-url');
  var select = document.getElementById('packages');
  var packageValue = select.options[select.selectedIndex].text;
  console.log(packageValue)
  var entry = {
    url: url.value,
    package: packageValue
  };

  fetch(`${window.origin}/store-package`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function(response) {
    if (response.status !== 200) {
      console.log(`Looks like there was a problem. Status code: ${response.status}`);
      return;
    }
    response.json().then(function(data) {
      // document.getElementById('packages').innerHTML = null;
      // document.getElementById('label-select').style.visibility = 'visible';
      // document.getElementById('packages').style.visibility = 'visible';
      // var packages = data['package_lists'];
      // console.log(packages)
      // packages.forEach(function(package) {
      //   var option = document.createElement("option");
      //   option.text = package;
      //   option.value = package;
      //   document.getElementById('packages').appendChild(option);
      // })
      // document.getElementById('btn-store-package').style.visibility = 'visible';
      // document.getElementById('bth-verify-package').style.visibility = 'visible';
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
  });
}

function verifyPackage() {
  var url = document.getElementById('ckan-input-url');
  var select = document.getElementById('packages');
  var packageValue = select.options[select.selectedIndex].text;
  console.log(packageValue)
  var entry = {
    url: url.value,
    package: packageValue
  };

  fetch(`${window.origin}/verify-package`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function(response) {
    if (response.status !== 200) {
      console.log(`Looks like there was a problem. Status code: ${response.status}`);
      return;
    }
    response.json().then(function(data) {
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
  });
}

$(document).ready(function() {
  setTimeout(function(){
    $("div.alert=info").remove();
  }, 5000 ); // 5 secs
});
