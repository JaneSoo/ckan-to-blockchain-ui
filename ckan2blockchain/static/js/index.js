function getPackages() {
  var url = document.getElementById('ckan-input-url');
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
  document.getElementById('btn-store-package').disabled = true;
  document.getElementById('bth-verify-package').disabled = true;
  document.getElementById('store-loader').removeAttribute('hidden');
  var url = document.getElementById('ckan-input-url');
  var select = document.getElementById('packages');
  var packageValue = select.options[select.selectedIndex].text;
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
    document.getElementById('store-loader').hidden = true;
    document.getElementById('bth-verify-package').disabled = false;
    document.getElementById('btn-store-package').disabled = false;
    response.json().then(function(data) {
      alert('Dataset package has been stored successfully!')
    });
  })
  .catch(function(error) {
    alert("Process failed")
    console.log("Fetch error: " + error);
  });
}

function verifyPackage(event) {
  document.getElementById('bth-verify-package').disabled = true;
  document.getElementById('btn-store-package').disabled = true;
  document.getElementById('verify-loader').removeAttribute('hidden');
  var url = document.getElementById('ckan-input-url');
  var select = document.getElementById('packages');
  var packageValue = select.options[select.selectedIndex].text;
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
    document.getElementById('verify-loader').hidden = true;
    document.getElementById('bth-verify-package').disabled = false;
    document.getElementById('btn-store-package').disabled = false;
    response.json().then(function(data) {
      const loader = document.querySelector('.loader');
      loader.hidden = false;
      if(data.result == 'True') {
        setTimeout(() => {
          loader.classList.add('success');
        }, 100)
        setTimeout(() => {
          document.getElementById('spinLoader').hidden = true;
        }, 5000)
      } else if (data.result == 'Transaction not found!'){
        setTimeout(() => {
          loader.classList.add('fail');
          alert('Transaction has not pushed to blockhain yet!');
        }, 100)
        setTimeout(() => {
          document.getElementById('spinLoader').hidden = true;
        }, 5000)
      } else {
        setTimeout(() => {
          loader.classList.add('fail');
        }, 100)
        setTimeout(() => {
          document.getElementById('spinLoader').hidden = true;
        }, 5000)
      }
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
  });
}
