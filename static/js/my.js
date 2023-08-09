// "use strict";

const orderlistDate = document.querySelectorAll(".orderlist-date");
const orderlistPrice = document.querySelectorAll(".orderlist-price");
const stats1Orderlist = document.querySelector(".stats-1");
const stats2Orderlist = document.querySelector(".stats-2");

const statusColours = function () {
  const tableStatus = document.querySelectorAll(".orderlijst-status");

  for (let index = 0; index < tableStatus.length; index++) {
    const element = tableStatus[index];
    if (element.innerText === "klaar voor verzending")
      element.classList.add("bg-primary");
    if (element.innerText === "wacht op betaling")
      element.classList.add("bg-info");
    if (element.innerText === "klaar voor afhaling")
      element.classList.add("bg-success");
    if (element.innerText === "cancelled") element.classList.add("bg-danger");
  }
};

statusColours();

// const nu = new Date();
// const nuFormat = `${nu.getDate()}-${nu.getMonth() + 1}-${nu.getFullYear()}`;

// const todayOrdersForProduction = () => {
//   let count = 0;
//   for (let index = 0; index < orderlistDate.length; index++) {
//     const element = orderlistDate[index];
//     const [datum] = element.innerText.split(" ");

//     const status = element.nextElementSibling.innerText;

//     if (
//       datum === nuFormat &&
//       (status === "klaar voor verzending" || status === "klaar voor afhaling")
//     ) {
//       count += 1;
//     }
//   }
//   stats1Orderlist.innerHTML = `Orders : ${count}`;
// };

// todayOrdersForProduction();
