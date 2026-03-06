const API = "/orders";

async function fetchOrders() {
  const res = await fetch(API);
  const data = await res.json();
  const tbody = document.querySelector("#orders-list tbody");
  tbody.innerHTML = "";
  data.forEach((o) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${o.order_id}</td>
            <td>${o.student_name}</td>
            <td>${o.document_name}</td>
            <td>${o.pages}</td>
            <td>${o.print_type}</td>
            <td>${o.total_cost}</td>
            <td>${o.status}</td>
            <td>
                ${o.status === "Pending" ? `<button onclick="pay(${o.order_id})">Enter Payment</button>` : ""}
                <button onclick="del(${o.order_id})">Delete</button>
            </td>`;
    tbody.appendChild(tr);
  });
}

document.getElementById("order-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const order = {
    student_name: document.getElementById("student_name").value,
    document_name: document.getElementById("document_name").value,
    pages: parseInt(document.getElementById("pages").value),
    print_type: document.getElementById("print_type").value,
  };
  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(order),
  });
  fetchOrders();
  e.target.reset();
});

async function del(id) {
  await fetch(`${API}/${id}`, { method: "DELETE" });
  fetchOrders();
}

async function pay(id) {
  const amount = prompt("Enter payment amount:");
  if (!amount) return;
  const res = await fetch(`${API}/${id}/pay`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount: parseFloat(amount) }),
  });
  const data = await res.json();
  alert(data.message + (data.change !== undefined ? " Change: " + data.change : ""));
  fetchOrders();
}

window.onload = fetchOrders;