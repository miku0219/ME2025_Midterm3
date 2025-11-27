// 開啟與關閉Modal
function open_input_table() {
  document.getElementById("addModal").style.display = "block";
}
function close_input_table() {
  document.getElementById("addModal").style.display = "none";
}

// === 初始化：讀取所有 Category ===
function loadCategories() {
  fetch("/product?all_categories=1")
    .then((res) => res.json())
    .then((data) => {
      const sel = document.getElementById("categorySelect");
      sel.innerHTML = "<option disabled selected>請選擇</option>";

      data.categories.forEach((c) => {
        let opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c;
        sel.appendChild(opt);
      });
    });
}

// Modal 打開時載入 category
function open_input_table() {
  document.getElementById("addModal").style.display = "block";
  loadCategories();
}

// === 1. 選取商品種類：連動取得商品名稱 ===
function selectCategory() {
  let category = document.getElementById("categorySelect").value;

  fetch(`/product?category=${encodeURIComponent(category)}`)
    .then((res) => res.json())
    .then((data) => {
      const productSel = document.getElementById("productSelect");
      productSel.innerHTML = "<option disabled selected>請選擇</option>";

      data.product.forEach((p) => {
        let opt = document.createElement("option");
        opt.value = p;
        opt.textContent = p;
        productSel.appendChild(opt);
      });
    });
}

// === 2. 選取商品名稱：自動取得單價 ===
function selectProduct() {
  let product = document.getElementById("productSelect").value;

  fetch(`/product?product=${encodeURIComponent(product)}`)
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("priceInput").value = data.price;
      countTotal();
    });
}

// === 3. 計算小計 (單價 × 數量) ===
function countTotal() {
  let qty = Number(document.getElementById("qtyInput").value);
  let price = Number(document.getElementById("priceInput").value);

  if (qty <= 0) {
    qty = 1;
    document.getElementById("qtyInput").value = 1;
  }

  document.getElementById("subtotalDisplay").value = qty * price;
}

// === 送出資料 ===
function submitOrder() {
  const payload = {
    date: document.getElementById("dateInput").value,
    customer_name: document.getElementById("customerInput").value,
    product_name: document.getElementById("productSelect").value,
    qty: document.getElementById("qtyInput").value,
    subtotal: document.getElementById("subtotalDisplay").value,
    status: document.getElementById("statusSelect").value,
    remark: document.getElementById("remarkInput").value,
  };

  fetch("/product", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((res) => {
      if (!res.ok) throw new Error("新增資料失敗");
      return res.json();
    })
    .then((result) => {
      console.log(result);
      close_input_table();
      location.assign("/");
    })
    .catch((err) => console.error("送出資料錯誤：", err));
}

function delete_data(value) {
  // 發送 DELETE 請求到後端
  fetch(`/product?order_id=${value}`, {
    method: "DELETE",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("伺服器回傳錯誤");
      }
      return response.json(); // 假設後端回傳 JSON 格式資料
    })
    .then((result) => {
      console.log(result); // 在這裡處理成功的回應
      close_input_table(); // 關閉 modal
      location.assign("/"); // 重新載入頁面
    })
    .catch((error) => {
      console.error("發生錯誤：", error);
    });
}
