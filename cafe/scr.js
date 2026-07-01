document.addEventListener("DOMContentLoaded", () => {

    // логин (оставил как есть)
    const form = document.getElementById("loginForm");

    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(e.target);

            try {
                const response = await fetch("http://127.0.0.1:8000/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: formData.get("username"),
                        password: formData.get("password")
                    })
                });

                if (!response.ok) throw new Error("Ошибка сервера");

                const data = await response.json();

                if (data.ok) {
                    window.location.href = "profile.html";
                } else {
                    alert("Неверный логин или пароль");
                }

            } catch (error) {
                console.error(error);
                alert("Не удалось подключиться к серверу.");
            }
        });
    }

    // корзина счётчик
    async function updateCartCount() {
        try {
            const response = await fetch("http://127.0.0.1:8000/cart/count/1");

            if (!response.ok) throw new Error("Ошибка корзины");

            const data = await response.json();

            const el = document.getElementById("cartCount");
            if (el) el.textContent = data.count;

        } catch (error) {
            console.error(error);
        }
    }

    updateCartCount();

    // добавление в корзину
    async function addToCart(productId) {
        try {
            const response = await fetch("http://127.0.0.1:8000/cart/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: 1,
                    product_id: productId
                })
            });

            if (!response.ok) throw new Error("Ошибка добавления в корзину");

            const data = await response.json();

            alert(data.message || "Добавлено в корзину");

            updateCartCount();

        } catch (error) {
            console.error(error);
            alert("Ошибка при добавлении в корзину");
        }
    }

    window.addToCart = addToCart;

    document.addEventListener("click", (e) => {
        const btn = e.target.closest(".add-to-cart");
        if (!btn) return;

        const id = btn.dataset.id;
        addToCart(id);
    });

});