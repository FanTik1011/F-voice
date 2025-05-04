fetch('/api/news')
    .then(response => response.json())
    .then(newsList => {
        let container = document.getElementById("news-container");
        newsList.forEach(news => {
            let div = document.createElement("div");
            div.className = "col-md-4";
            div.innerHTML = `
                <div class="card">
                    <img src="${news.images[0]}" class="card-img-top" alt="Новина">
                    <div class="card-body">
                        <h5 class="card-title">${news.title}</h5>
                        <p class="card-text">${news.content}</p>
                        <p><strong>Дата:</strong> ${news.date}</p>
                    </div>
                </div>
            `;
            container.appendChild(div);
        });
    });
