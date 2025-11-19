document.addEventListener("DOMContentLoaded", () => {

    /* -------------------------------------------------------------
       1) ORDER — Save last order for 1 hour
    ------------------------------------------------------------- */
    const lastOrder = localStorage.getItem("lastOrder");

    if (lastOrder) {
        const orderData = JSON.parse(lastOrder);

        const orderTime = new Date(orderData.time);
        const now = new Date();
        const diffHours = (now - orderTime) / 1000 / 60 / 60;

        if (diffHours >= 1) {
            localStorage.removeItem("lastOrder");
        }
    }

    const orderForm = document.querySelector(".order-form form");
    if (orderForm) {
        orderForm.addEventListener("submit", () => {
            const fullName = document.getElementById("full_name").value;
            const flowerName = document.querySelector(".flower-card h3").innerText;

            const orderData = {
                name: fullName,
                flowerName: flowerName,
                time: new Date().toISOString()
            };

            localStorage.setItem("lastOrder", JSON.stringify(orderData));
        });
    }


    /* -------------------------------------------------------------
       2) LIKE SYSTEM on product boxes
    ------------------------------------------------------------- */
    const likeButtons = document.querySelectorAll(".like-btn");
    let likes = JSON.parse(localStorage.getItem("likes")) || [];

    likeButtons.forEach(btn => {
        const id = btn.dataset.id;

        if (likes.includes(id)) {
            btn.classList.add("liked");
        }

        btn.addEventListener("click", () => {
            if (likes.includes(id)) {
                likes = likes.filter(x => x !== id);
                btn.classList.remove("liked");
            } else {
                likes.push(id);
                btn.classList.add("liked");
            }

            localStorage.setItem("likes", JSON.stringify(likes));
        });
    });


    /* -------------------------------------------------------------
       3) FAVORITES PAGE — Build favorites from localStorage only
    ------------------------------------------------------------- */
    const favoritesContainer = document.getElementById("favoritesContainer");

    if (favoritesContainer) {
        const likedIds = JSON.parse(localStorage.getItem("likes")) || [];
        const allBouquets = JSON.parse(localStorage.getItem("allBouquets")) || [];

        favoritesContainer.innerHTML = "";

        if (likedIds.length === 0) {
            favoritesContainer.innerHTML =
                "<p style='font-size:2rem; text-align:center;'>No favorites yet.</p>";
        } else {
            likedIds.forEach(id => {
                const html = allBouquets[id - 1];
                if (html) favoritesContainer.innerHTML += html;
            });
        }
    }


    /* -------------------------------------------------------------
       4) Save all product bouquets (only on index page)
    ------------------------------------------------------------- */
    // لو احنا على الصفحة الرئيسية بس
if (window.location.pathname === "/") {
    const productBouquets = document.querySelectorAll(".bouquet-box");

    if (productBouquets.length > 0) {
        const arr = [];
        productBouquets.forEach(box => arr.push(box.outerHTML));
        localStorage.setItem("allBouquets", JSON.stringify(arr));
    }
}
});


