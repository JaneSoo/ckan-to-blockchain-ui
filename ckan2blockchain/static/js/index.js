function getPackages() {
  document.getElementById('detail-info').style.visibility = 'hidden';
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
      $('.package-select2').select2();

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
  document.getElementById('detail-info').style.visibility = 'hidden';
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
      if (data.trx_hash == 'Error downloading package'){
        alert('Cannot download package at the moment!')
      } else {
        const returnMessage = document.createElement('p');
        const link = document.createElement('a');
        const detailInfo = document.getElementById('detail-info');
        detailInfo.innerHTML = '';
        returnMessage.innerHTML = 'Your dataset transaction has been sent.';
        link.href = `https://rinkeby.etherscan.io/tx/${data.trx_hash}`;
        link.setAttribute('target', '_blank');
        link.innerText = 'Check out your transaction.';
        detailInfo.style.visibility = 'visible';
        detailInfo.appendChild(returnMessage);
        detailInfo.appendChild(link);
      }
    });
  })
  .catch(function(error) {
    alert("Process failed")
    console.log("Fetch error: " + error);
  });
}

function verifyPackage(event) {
  document.getElementById('detail-info').style.visibility = 'hidden';
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
      loader.classList.remove('success');
      loader.classList.remove('fail');
      if(data.result == true) {
        setTimeout(() => {
          loader.classList.add('success');
        }, 100)
        setTimeout(() => {
          document.getElementById('spinLoader').hidden = true;
        }, 5000)

        const p = document.createElement('p');
        const block = document.createElement('a');
        const txn = document.createElement('a');
        const divInfo = document.getElementById("detail-info");
        p.innerHTML = `Data is identical. Hash was pushed to Ethereum on ${data.timestamp}`;
        divInfo.innerHTML = '';
        block.href = `https://rinkeby.etherscan.io/block/${data.block_num}`;
        block.setAttribute('target', '_blank');
        block.innerText = 'See block on Etherscan'
        txn.href = `https://rinkeby.etherscan.io/tx/${data.trx_hash}`
        txn.setAttribute('target', '_blank');
        txn.innerText = 'See transaction on Etherscan'
        divInfo.style.visibility = 'visible';
        divInfo.appendChild(p);
        divInfo.appendChild(block);
        divInfo.appendChild(document.createElement('br'))
        divInfo.appendChild(txn);
      } else if (data.result == 'Transaction not found!'){
        setTimeout(() => {
          loader.classList.add('fail');
          alert('Transaction has not pushed to blockhain yet!');
        }, 100)
        setTimeout(() => {
          document.getElementById('spinLoader').hidden = true;
        }, 5000)
      } else if (data.result == 'Error downloading package'){
        setTimeout(() => {
          loader.classList.add('fail');
          alert('Cannot download the package at the moment');
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
        const p = document.createElement('p');
        const block = document.createElement('a');
        const txn = document.createElement('a');
        const divInfo = document.getElementById("detail-info");
        p.innerHTML = `Data is not identical. Hash was pushed to Ethereum on ${data.timestamp}`;
        divInfo.innerHTML = '';
        block.href = `https://rinkeby.etherscan.io/block/${data.block_num}`;
        block.setAttribute('target', '_blank');
        block.innerText = 'See block on Etherscan'
        txn.href = `https://rinkeby.etherscan.io/tx/${data.trx_hash}`
        txn.setAttribute('target', '_blank');
        txn.innerText = 'See transaction on Etherscan'
        divInfo.style.visibility = 'visible';
        divInfo.appendChild(p);
        divInfo.appendChild(block);
        divInfo.appendChild(document.createElement('br'))
        divInfo.appendChild(txn);
      }
    });
  })
  .catch(function(error) {
    console.log("Fetch error: " + error);
  });
}
