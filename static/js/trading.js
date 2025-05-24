let profitMargin = 0;

function generateProfitMargin() {
  profitMargin = (Math.random() * (9.2 - 7.5) + 7.5).toFixed(2);
  document.getElementById("profitMargin").innerText = profitMargin;
}

// Run immediately on page load
generateProfitMargin();

// Then update every 60,000 milliseconds (1 minute)
setInterval(() => {
  generateProfitMargin();
  console.log("Profit margin updated");
}, 20000);

function forexTrade() {
  const amount = Number(document.getElementById("amount").innerHTML);
  const amountInput = Number(document.getElementById("amountInput").value);
  const durationMins = Number(document.getElementById("durationSelect").value); // e.g. "5"
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  if (amountInput < 1) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Invalid amount!",
      footer: "Enter a valid amount",
    });
    return;
  }

  if (amountInput > amount) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Amount exceeds available balance!",
      footer: "<a href='/dashboard/deposit/'>Deposit to your account</a>",
    });
    return;
  }

  // Convert minutes to "HH:MM:SS"
  const hours = Math.floor(durationMins / 60)
    .toString()
    .padStart(2, "0");
  const minutes = (durationMins % 60).toString().padStart(2, "0");
  const duration = `${hours}:${minutes}:00`;

  // Generate profit margin between 7.5 and 9.2
  // const profitMargin = (Math.random() * (9.2 - 7.5) + 7.5).toFixed(2);

  fetch("/api/trades/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      amount: amountInput,
      duration: duration,
      profit_margin: profitMargin,
    }),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Trade creation failed");
      return response.json();
    })
    .then((data) => {
      Swal.fire({
        icon: "success",
        title: "Success!",
        text: "Trade Submitted successfully!",
      });
      if (data.balance !== undefined) {
        document.getElementById("balance").innerText = `$${data.balance.toFixed(
          2
        )}`;
      }
    })
    .catch((error) => {
      console.error(error);
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Something went wrong!",
      });
    });
}
